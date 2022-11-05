import numpy
import scipy
import mne
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')

DIR = Path.cwd()
eeg_DIR = DIR / "data"
subdir = '100 bpm'
filename = 'record-[2022.11.04-17.23.44].vhdr'

raw = mne.io.read_raw_brainvision(eeg_DIR / subdir / filename, preload=True)

mapping = {"Channel 1": "Fp1", "Channel 2": "Fp2", "Channel 3": "F3", "Channel 4": "F4",
           "Channel 5": "C3", "Channel 6": "C4", "Channel 7": "P3", "Channel 8": "P4",
           "Channel 9": "O1", "Channel 10": "O2", "Channel 11": "F7", "Channel 12": "F8",
           "Channel 13": "T7", "Channel 14": "T8", "Channel 15": "P7", "Channel 16": "P8",
           "Channel 17": "Fz", "Channel 18": "Cz", "Channel 19": "Pz", "Channel 20": "M1",
           "Channel 21": "M2", "Channel 22": "AFz", "Channel 23": "CPz", "Channel 24": "POz"}
raw.rename_channels(mapping)
raw.drop_channels(['M1', 'M2', 'Gyro 1', 'Gyro 2', 'Gyro 3'])
montage = mne.channels.make_standard_montage('easycap-M1')
raw.set_montage(montage)


events = mne.events_from_annotations(raw)[0]
# mne.viz.plot_events(events)

# raw.plot_psd()
raw.filter(l_freq=0.1, h_freq=None)

tmin = -0.2
tmax = 0.5
reject_criteria = dict(eeg=800e-6)
flat_criteria = None
event_id = {
    'snare': 10003,
    'base': 10002,
    # 'hi-hat': 10001
}
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, reject=reject_criteria, flat=flat_criteria,
                    reject_by_annotation=True, preload=True, baseline=None, event_repeated='error')

baseline = (-0.2, 0)
epochs.apply_baseline(baseline)
epochs.average().plot()

##