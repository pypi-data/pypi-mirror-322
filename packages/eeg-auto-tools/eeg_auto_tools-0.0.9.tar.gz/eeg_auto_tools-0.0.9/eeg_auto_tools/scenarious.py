# Copyright 2025 Sear Gamemode
import re 
from datetime import datetime
import os 
import mne 
import numpy as np 

electrodesofmontages = [
    'Fp1', 'Fpz', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'FC5', 'FC1', 'FC2', 'FC6',
    'M1', 'T7', 'C3', 'Cz', 'C4', 'T8', 'M2', 'CP5', 'CP1', 'CP2', 'CP6', 'P7',
    'P3', 'Pz', 'P4', 'P8', 'POz', 'O1', 'Oz', 'O2', 'AF7', 'AF3', 'AF4', 'AF8',
    'F5', 'F1', 'F2', 'F6', 'FC3', 'FCz', 'FC4', 'C5', 'C1', 'C2', 'C6', 'CP3',
    'CP4', 'P5', 'P1', 'P2', 'P6', 'PO5', 'PO3', 'PO4', 'PO6', 'FT7', 'FT8',
    'TP7', 'TP8', 'PO7', 'PO8']

def get_riti_seq():
    sequence_file = 'RiTi_seq.txt'
    seq_list = []
    transform = {'Stimulus/s115':1, 'Stimulus/s120':4, 'Stimulus/s130':2, 'Stimulus/s160':3, 'Stimulus/s240':5}
    reverse_transform = dict(zip(transform.values(), transform.keys()))
    with open(sequence_file, 'r') as file:
        for line in file:
            seq_list.append(reverse_transform[int(line)])
    return seq_list

def get_stim(scenarious_name):
    list_stim = None 
    if scenarious_name == 'ANT':
        list_stim = ['Stimulus/s143', 'Stimulus/s145', 'Stimulus/s149', 'Stimulus/s151', 
                     'Stimulus/s141', 'Stimulus/s147', 'Stimulus/s153', 'Stimulus/s155']
    elif scenarious_name == 'RiTi':
        list_stim = ['Stimulus/s115', 'Stimulus/s120', 'Stimulus/s130', 'Stimulus/s160', 'Stimulus/s240']
    return list_stim

def get_meta(file_name):
    file_pattern = re.compile(
        r'INP(?P<id>\d{4})_v1\.(?P<visit_num>\d)_(?P<experiment>[^_]+)_'
        r'(?P<operator_code>[A-Za-z0-9_]+)_(?P<date>\d{2}\.\d{2}\.\d{2,4})'
        r'\.(?P<format>vhdr|vmrk|eeg)')
    match = file_pattern.match(file_name)
    return match.groupdict() if match else None

def get_brainvision_files(vhdr_path):
    with open(vhdr_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    #  
    eeg_fname = None
    vmrk_fname = None
    #     
    for line in lines:
        line = line.strip()
        if line.startswith('DataFile='):
            eeg_fname = line.split('=')[1].strip()
        elif line.startswith('MarkerFile='):
            vmrk_fname = line.split('=')[1].strip()
    return (eeg_fname, vmrk_fname)


def get_file_info(file_path, elc_path):
    #   EEG
    raw = mne.io.read_raw_brainvision(file_path, 
                                      preload=False, verbose=False)
    #  -
    eeg_files = (file_path,) + get_brainvision_files(file_path)
    eeg_files = list(map(os.path.basename, eeg_files))
    meta = get_meta(eeg_files[0])
    #   EEG
    meas_date = raw.info['meas_date']
    if meas_date is not None:
        if isinstance(meas_date, datetime):
            measurement_datetime = meas_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        measurement_datetime = 'Unknown'
    #    
    data = {
        "id": meta.get('id', 'N/A'),
        "visit_num": meta.get('visit_num', 'N/A'),
        "scenario": meta.get('experiment', 'N/A'),
        "operator_code": ', '.join(meta.get('operator_code', 'N/A').split('_')),
        "eeg_files": ' '.join(eeg_files),
        "elc_file": os.path.basename(elc_path) if elc_path else 'Not found',
        "raw_type": type(raw).__name__,
        "duration": f"{raw.times[-1]:.2f}",
        "nchan": raw.info['nchan'],
        "electrodes_of_montages" : set(electrodesofmontages).issubset(set(raw.ch_names)),
        "ecg_channel": 'BIP1' in raw.ch_names,
        "eog_channel": 'EOG' in raw.ch_names,
        "sfreq": raw.info['sfreq'],
        "measurement_datetime": measurement_datetime,
        "highpass": raw.info['highpass'],
        "lowpass": raw.info['lowpass'],
        "custom_ref_applied": raw.info.get('custom_ref_applied', 'Not available'),
    }
    return data


def is_subsequence(subseq, seq):
    subseq_index = 0
    subseq_len = len(subseq)
    flag = 0
    transitions = 0
    for elem in seq:
        copy_flag = flag
        if subseq_index < subseq_len and elem == subseq[subseq_index]:
            subseq_index += 1
            flag = 1
        else:
            flag = 0
        if flag != copy_flag:
            transitions += 1
    return subseq_index == subseq_len, subseq_index, transitions

def verificate_events(raw, seq_list, shift=1.85, var=0.35):
    events, event_id = mne.events_from_annotations(raw, verbose=False)
    reverse_event_id = dict(zip(event_id.values(), event_id.keys()))
    
    tar_idx = 0
    new_events = []
    
    n_events = len(events)
    n_seq = len(seq_list)
    events_times = events[:, 0]/raw.info['sfreq']
    events_seq = np.array([reverse_event_id[events[i, 2]] for i in range(len(events))])
    current_time = events_times[0] - shift

    #new_events.append(events[0])
    while not (tar_idx > n_seq - 1 or current_time > events_times[-1]):
        
        next_time_l = current_time + shift - var
        next_time_r = current_time + shift + var

        mask = (events_times >= next_time_l) & (events_times <= next_time_r)
        filtered_seq = events_seq[mask]
        filtered_events = events[mask]
        filtered_times = events_times[mask]
        if filtered_seq.size > 0:
            unique_elements = np.unique(filtered_seq)
            if len(unique_elements) == 1:
                new_events.append(filtered_events[0])
                tar_idx += 1
                current_time = filtered_times[0]
            else:
                matches = seq_list[tar_idx] == filtered_seq
                if matches.all():
                    new_events.append(filtered_events[matches[0]])
                    tar_idx += 1
                    current_time = filtered_times[matches[0]]
                else:    
                    tar_idx += 1
                    current_time += shift
        else:
            tar_idx += 1
            current_time += var
    
    return np.array(new_events)
