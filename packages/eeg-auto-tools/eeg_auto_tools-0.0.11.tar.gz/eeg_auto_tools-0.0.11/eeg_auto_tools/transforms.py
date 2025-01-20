# Copyright 2025 Sear Gamemode
import os 
import mne
import time
import scipy
import numpy as np 

import matplotlib.pyplot as plt 

from tqdm import tqdm
from mne.preprocessing import ICA
from collections import Counter
from scipy.signal import savgol_filter
from mne_icalabel import label_components
import typing 

from .savers import compared_snr
from .quality_check import detect_bad_channels, compared_spectrum, compute_bad_epochs, set_montage, preprocessing_events
from .scenarious import get_stim
from .metrics import calculate_SN_ratio
from .craft_events import make_ANT_events, make_RiTi_events, make_CB_events


class Transform:
    def __init__(self):
        self.repo_images = {}
        self.repo_data = {}
        self.report = None
        self.pref = None

    def __call__(self, inst):
        return self.forward(inst.copy())

    def forward(self, inst):
        raise NotImplementedError("Each transform must implement the forward method.")
    
    def get_transform_report(self,):
        return self.repo_data, self.repo_images
    
    def plot_images(self):
        for fig in self.repo_images.values():
            fig.show()

    def save_report(self, path, pref=''):
        pathes = []
        for key, fig in self.repo_images.items():
            path_image = os.path.join(path, pref+key+'.png')
            fig.savefig(path_image, bbox_inches='tight')
            pathes.append(path_image)
        return pathes
    

class Sequence:
    def __init__(self, **transforms):
        self.transforms = transforms
        self.seq_report = []
        self.insts = []

        #        
        for name, transform in transforms.items():
            setattr(self, name, transform)

    def __call__(self, raw, progress_bar=None, cash=False):
        for name, transform in self.transforms.items():
            if progress_bar:
                progress_bar.set_postfix(status=f'{name}')
            raw = transform(raw)
            if cash:
                self.insts.append(raw)
            self.seq_report.append(transform.get_transform_report())
        return raw
    
    def get_transform_report(self,):
        return self.seq_report
    
    def plot_images(self):
        for name, transform in self.transforms.items():
            transform.plot_images()


class ChannelSelector(Transform):
    def __init__(self, exclude=None, report=True):
        self.exclude = exclude
        self.repo_data = {}
        self.repo_images = {}
        self.report = report 

    def forward(self, raw):
        dropped_name = set([ch for ch in self.exclude if ch in raw.ch_names])
        bip_channels = set([ch for ch in raw.ch_names if 'BIP' in ch])
        dropped = list(dropped_name | bip_channels)
        print(f'CHANNELS DROPPED: {dropped}')
        return raw.drop_channels(dropped)


class DetrendEpochs(Transform):
    def __init__(self, detrend_type, report=True):
        self.detrend_type=detrend_type 
        self.report = report
        self.repo_data = {}
        self.repo_images = {}

    def forward(self, epochs):
        detrended_epochs = epochs.copy().apply_function(scipy.signal.detrend, type=self.detrend_type)
        if self.report:
            self.repo_data = {}
            snr_matrix = calculate_SN_ratio(epochs.copy(), option='mean_epochs', mode='log')
            snr_matrix_after = calculate_SN_ratio(detrended_epochs.copy(), option='mean_epochs', mode='log')
            snr_dist_fig = compared_snr([snr_matrix, snr_matrix_after], ['Before detrend', 'After detrend'])
            spectrum_fig = compared_spectrum(epochs, detrended_epochs, fmin=0, fmax=min(100, epochs.info['sfreq']))
            self.repo_images = {'SNR_dist': snr_dist_fig, 'Spectrum': spectrum_fig}
        return detrended_epochs

class BaselineEpochs(Transform):
    def __init__(self, baseline, report=True):
        self.baseline=baseline
        self.report = report
        self.repo_data = {}
        self.repo_images = {}

    def forward(self, epochs):
        baselined_epochs = epochs.copy().apply_baseline(self.baseline, verbose=False)

        if self.report:
            self.repo_data = {}
            snr_matrix = calculate_SN_ratio(epochs.copy(), option='mean_epochs', mode='log')
            snr_matrix_after = calculate_SN_ratio(baselined_epochs.copy(), option='mean_epochs', mode='log')
            snr_dist_fig = compared_snr([snr_matrix, snr_matrix_after], ['Before baseline', 'After baseline'])
            spectrum_fig = compared_spectrum(epochs, baselined_epochs, fmin=0, fmax=min(100, epochs.info['sfreq']/2))
            self.repo_images = {'SNR_dist': snr_dist_fig, 'Spectrum': spectrum_fig}
        return baselined_epochs
    

class BadEpochsDetector(Transform):
    def __init__(self, roi_channels=None, apply=True, report=True):
        self.roi_channels = roi_channels
        self.report = report
        self.repo_data = {}
        self.repo_images = {}
        self.apply = apply

    def forward(self, epochs):
        snr_matrix = calculate_SN_ratio(epochs.copy(), option='mean_epochs', mode='log')
        rej_dict = compute_bad_epochs(epochs, snr_matrix, roi_channels=self.roi_channels)
        cleaned_epochs = epochs.copy().drop(rej_dict['FINAL'], verbose=False)
        if self.report:
            self.repo_data = rej_dict 
            snr_matrix_after = calculate_SN_ratio(cleaned_epochs, option='mean_epochs', mode='log')
            snr_dist_fig = compared_snr([snr_matrix, snr_matrix_after], ['Before detector', 'After Detector'])
            spectrum_fig = compared_spectrum(epochs, cleaned_epochs, fmin=0, fmax=min(100, epochs.info['sfreq']/2))
            self.repo_images = {'SNR_dist': snr_dist_fig, 'Spectrum': spectrum_fig}

        if self.apply:
            return cleaned_epochs
        else:
            return epochs

class CheckEvents(Transform):
    def __init__(self, scenarious_name, report=True):
        self.scenarious_name = scenarious_name
        self.report = report

    def forward(self, raw):
        new_events, reverse_event_id, repo_data = preprocessing_events(raw, scenarious=self.scenarious_name)
        if self.report:
            self.repo_data = repo_data
            self.repo_images = {}
        event_times = new_events[:, 0] / raw.info['sfreq']
        event_times -= raw.first_time
        event_codes = new_events[:, 2].astype(int)
        event_descriptions = [reverse_event_id[code] for code in event_codes]
        durations = [0] * len(event_times)
        new_annotations = mne.Annotations(onset=event_times,
                                        duration=durations,
                                        description=event_descriptions,
                                        )
        raw.set_annotations(new_annotations)
        return raw


class Cropping(Transform):
    def __init__(self, scenarious_name, report=True):
        self.stimulus = get_stim(scenarious_name)
        self.report = report
        self.repo_images = {}
        self.repo_data = {}

    def forward(self, raw):
        events, event_id = mne.events_from_annotations(raw)
        if event_id is None or not self.stimulus:
            return raw
        stimulus_codes = [event_id[stim] for stim in self.stimulus if stim in event_id]
        desired_event_ids = dict(zip(self.stimulus, stimulus_codes))
        reverse_desired_event_ids = dict(zip(stimulus_codes, self.stimulus))
        desired_event_values = list(desired_event_ids.values())
        filtered_events = events[np.isin(events[:, 2], desired_event_values)]
        filtered_events = np.array(filtered_events)
        annotations = mne.annotations_from_events(
            events=filtered_events,
            sfreq=raw.info['sfreq'],
            event_desc=reverse_desired_event_ids,
            first_samp=raw.first_samp
        )
        raw.set_annotations(annotations)
        first_stimulus_time = filtered_events[0, 0] / raw.info['sfreq']
        last_stimulus_time = filtered_events[-1, 0] / raw.info['sfreq']
        tmin = max(0, first_stimulus_time - 1.0)
        tmax = min(raw.times[-1], last_stimulus_time + 1.0)
        raw = raw.crop(tmin=tmin, tmax=tmax)
        if self.report:
            missing_labels = set(self.stimulus) - set(event_id.keys())
            self.repo_data = {'Deleted events': missing_labels, 'New_duration': tmax-tmin}
            self.repo_images = {}
        return raw

class FilterBandpass(Transform):
    def __init__(self, l_freq:float, h_freq:float, notch_freq:float=None, 
                 method:str='fir', fir_design:str='firwin', report:bool=True):
        self.l_freq = l_freq
        self.h_freq = h_freq
        self.notch_freq = notch_freq
        self.method = method
        self.fir_design = fir_design
        self.report = report
        self.repo_images = {}
        self.repo_data = {}

    def forward(self, raw:mne.io.Raw) -> mne.io.Raw:
        raw_filtered = raw.copy()
        if self.notch_freq:
            raw_filtered = raw_filtered.notch_filter(freqs=self.notch_freq, method=self.method, fir_design=self.fir_design, 
                                pad='reflect_limited', phase='zero-double', verbose=False, n_jobs='cuda' if mne.cuda.get_config()['MNE_USE_CUDA']=='true' else -1)
        raw_filtered = raw_filtered.filter(l_freq=self.l_freq, h_freq=self.h_freq, method=self.method, fir_design=self.fir_design, 
                        pad='reflect_limited', phase='zero-double', verbose=False, n_jobs='cuda' if mne.cuda.get_config()['MNE_USE_CUDA']=='true' else -1)
        if self.report:
            fig = compared_spectrum(raw, raw_filtered, self.l_freq, self.h_freq, fmin=0, fmax=min(100, raw.info['sfreq']/2))
            self.repo_images = {'Spectrum': fig}
            self.repo_data = {}
        return raw_filtered


class StatisticFilter(Transform):
    def __init__(self, method, report=True):
        self.method = method
        self.report = report
    def forward(self, raw, method, save, vis):
        raw_filtered = raw.copy()
        if method=='savgol':
            data = raw.get_data()
            for idx, ch in tqdm(enumerate(raw.ch_names), total=len(raw.ch_names)):
                data[idx] = savgol_filter(data[idx], window_length=20, polyorder=4)
            raw_filtered._data = data
        
        if self.report:
            fig = compared_spectrum(raw, raw_filtered, fmin=0, fmax=100)
            self.repo_images = {'Spectrum': fig}
            self.repo_data = {}
        return raw_filtered
    
class Interpolate(Transform):
    def __init__(self, reset_bads=True, report=True):
        self.reset_bads = reset_bads
        self.report = report
        self.repo_data = {}
        self.repo_images = {}
        
    def forward(self, raw):
        cleaned_raw = raw.copy().interpolate_bads(reset_bads=self.reset_bads, method=dict(eeg="spline"), verbose=False)
        if self.report:
            fig = compared_spectrum(raw, cleaned_raw, fmin=0, fmax=100)
            self.repo_images = {'Spectrum': fig}
            self.repo_data = {}
        return cleaned_raw


class BadChannelsDetector(Transform):
    def __init__(self, method, report=True, mark=True):
        self.method = method
        self.bad_channels = []
        self.electrodesD = {}
        self.report = report
        self.mark = mark

    def forward(self, raw):
        self.electrodesD, clusters, bridge_figs, noised_fig = detect_bad_channels(raw, self.method)
        bad_channels = [ch for sublist in self.electrodesD.values() for ch in sublist]
        united_bad_channels = list(set(bad_channels) | set(raw.info['bads']))
        if self.mark:
            raw.info['bads'] = united_bad_channels

        if self.report:
            self.repo_images = {'Bridged_channels': bridge_figs[0], 'Bridged_hist': bridge_figs[1], 
                                'Noised_channels': noised_fig}
            self.repo_data = {**{'Clusters': clusters}, **self.electrodesD, **{'FINAL': united_bad_channels}}
        return raw


class AutoICA(Transform):
    def __init__(self, n_components='auto', method='picard', report=True):
        self.n_components = n_components
        self.method = method
        self.report = report
        self.repo_data = {}
        self.repo_images = {}

    def forward(self, raw):
        #       ICA
        if self.n_components == 'auto':
            rank = len(raw.ch_names) - len(raw.info['bads'])
            self.n_components=rank//3
        MAX_DELETED_COMP = self.n_components//2

        #  ICA
        ica = ICA(n_components=self.n_components, fit_params=dict(ortho=False, extended=True),
                method=self.method, random_state=97, verbose=False)
        picks = mne.pick_channels(ch_names=raw.info['ch_names'], include=[], exclude=raw.info["bads"])
        ica.fit(raw, picks=picks, verbose=False)
        
        #   
        mne.set_log_level('ERROR')
        ica_labels = label_components(raw, ica, method='iclabel')
        mne.set_log_level('INFO')
        labels = ica_labels["labels"]
        probas = ica_labels['y_pred_proba']
        exclude_idx = [idx for idx, label in enumerate(labels) if label not in ['brain']][:MAX_DELETED_COMP]
        exclude_labels = [label for idx, label in enumerate(labels) if label not in ['brain']][:MAX_DELETED_COMP]

        #  bad 
        raw_filtered = ica.apply(raw.copy(), exclude=exclude_idx, verbose=False)
        self.repo_images = {}
        #     
        if self.report:
            all_components_fig = ica.plot_components(inst=raw, show=False, verbose=False)
            plt.close(all_components_fig)
            for idx, label in zip(exclude_idx, exclude_labels):
                fig = ica.plot_properties(raw, picks=idx, show=False, verbose=False)[0]
                self.repo_images[f'comp_{idx}_label_{label}'] = fig
                plt.close(fig)
                
            self.repo_images['all_comp'] = all_components_fig 
            spec_fig = compared_spectrum(raw.copy().pick(picks), raw_filtered.copy().pick(picks), fmin=0, fmax=min(100, raw.info['sfreq']/2))
            self.repo_images['Spectrum'] = spec_fig
            self.repo_data = {'exclude_idx': exclude_idx, 'exclude_labels': exclude_labels}
        
        return raw_filtered

class Rereference(Transform):   
    def __init__(self, method='average', exclude='bads', report=True):
        self.method = method
        self.exclude = exclude
        self.report = report
        self.repo_data = {}
        self.repo_images = {}
        
    def forward(self, raw):
        raw_filtered = raw.copy()
 
        picks = mne.pick_channels(ch_names=raw.info['ch_names'], include=[], exclude=raw.info["bads"])
        if self.method=='average' and self.exclude=='bads':
            include_channels = [ch for ch in raw.ch_names if ch not in raw.info['bads']]
            raw_filtered.set_eeg_reference(ref_channels=include_channels, verbose=False)
        else:
            raw_filtered.set_eeg_reference(self.method, verbose=False)
        if self.method == 'laplas':
            raw_filtered = mne.preprocessing.compute_current_source_density(raw_filtered, verbose=False)

        #     
        if self.report:
            figs = compared_spectrum(raw.copy().pick(picks), raw_filtered.copy().pick(picks), fmin=0, fmax=100)
            self.repo_data = {}
            self.repo_images = {'Spectrum': figs}

        return raw_filtered

class Resample(Transform):
    def __init__(self, sfreq, report=True):
        self.sfreq = sfreq
        self.report = report
        self.repo_data = {}
        self.repo_images = {}

    def forward(self, raw):
        resampled_raw = raw.copy().resample(sfreq=self.sfreq, npad="auto")
        if self.report:
            self.repo_data = {}
            self.repo_images = {}
        return resampled_raw
    
class BridgeInterpolate(Transform):
    def __init__(self, bridged_idx):
        self.bridged_idx = bridged_idx
    def forward(self, raw):
        raw = mne.preprocessing.interpolate_bridged_electrodes(raw, self.bridged_idx, bad_limit=4)
        return raw


class Raw2Epoch(Transform):
    def __init__(self, tmin=-0.15, tmax=0.75, baseline=(None, 0), stimulus_list=None, scenarious_name=None, report=True):
        self.tmin=tmin 
        self.tmax=tmax 
        self.baseline=baseline
        self.stimulus_list=stimulus_list
        self.scenarious_name = scenarious_name
        self.report = report
        self.repo_data = {}
        self.repo_images = {}

    def forward(self, raw):
        if self.scenarious_name == 'RiTi':
            events, event_id = make_RiTi_events(raw, self.stimulus_list)
        elif self.scenarious_name == 'ANT':
            events, event_id = make_ANT_events(raw, self.tmin, self.tmax, self.baseline)
        elif self.scenarious_name == 'Rest-IAT' or self.scenarious_name=="MAIN":
            events, event_id = make_CB_events(raw, self.scenarious_name)
        else:
            events, event_id = mne.events_from_annotations(raw, verbose=False)
        epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=self.tmin, tmax=self.tmax, 
                        baseline=self.baseline, preload=True, verbose=False, event_repeated="merge")
        print(f"Num of trials in events/epochs {self.scenarious_name}: {len(events)}/{len(epochs)}")
        if self.report:
            events = epochs.events
            event_id = epochs.event_id
            event_counts = Counter(events[:, 2])
            event_id_reverse = {v: k for k, v in event_id.items()}
            dict_event_count = {}

            for event_code, count in event_counts.items():
                dict_event_count[event_id_reverse[event_code]] = count
            self.repo_data = {'events_count': dict_event_count}
        return epochs

class SetMontage(Transform):
    def __init__(self, montage, elc_file=None, mode='Cz', vis=False, threshold=0.08, interpolate=True):
        self.montage = montage
        self.elc_file = elc_file
        self.vis = vis
        self.mode = mode
        self.threshold = threshold
        self.interpolate = interpolate
        self.repo_data = {}
        self.repo_images = {}
    def forward(self, raw):
        return set_montage(raw, self.montage, self.elc_file, self.mode, self.threshold, self.interpolate, self.vis)


