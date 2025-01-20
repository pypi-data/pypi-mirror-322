# Example Code

file = "your_file_path"
raw = mne.io.read_raw(file, preload=True)

pipeline = Sequence(
    ch_selector = ChannelSelector(exclude=['ECG', 'EOG']),
    ffilter = FilterBandpass(l_freq=0.1, h_freq=40, notch_freq=50),
    montager = SetMontage('waveguard64'),
    detector = BadChannelsDetector(method="auto"),
    rerefer = Rereference(exclude='bads'),
    ica = AutoICA(),
    interp = Interpolate(),
    r2e = Raw2Epoch(tmin=-0.15, tmax=0.6),
    bed = BadEpochsDetector(apply=True),
    baseliner = BaselineEpochs(baseline=(-0.1, 0)),
    detrender = DetrendEpochs(detrend_type="linear"),
)

epochs = pipeline(raw, cash=False)


# Other Info

This is an eeg-processing package. You can visit
[GitHub-flavored Markdown](https://github.com/MegaSear)
to read other content.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
