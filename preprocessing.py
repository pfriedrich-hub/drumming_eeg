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

mapping = {"1": "Fp1", "2": "Fp2", "3": "F7", "4": "F3", "5": "Fz", "6": "F4",
           "7": "F8", "8": "FC5", "9": "FC1", "10": "FC2", "11": "FC6",
           "12": "T7", "13": "C3", "14": "Cz", "15": "C4", "16": "T8", "17": "TP9",
           "18": "CP5", "19": "CP1", "20": "CP2", "21": "CP6", "22": "TP10",
           "23": "P7", "24": "P3", "25": "Pz", "26": "P4", "27": "P8", "28": "PO9",
           "29": "O1", "30": "Oz", "31": "O2", "32": "PO10", "33": "AF7", "34": "AF3",
           "35": "AF4", "36": "AF8", "37": "F5", "38": "F1", "39": "F2", "40": "F6",
           "41": "FT9", "42": "FT7", "43": "FC3", "44": "FC4", "45": "FT8", "46": "FT10",
           "47": "C5", "48": "C1", "49": "C2", "50": "C6", "51": "TP7", "52": "CP3",
           "53": "CPz", "54": "CP4", "55": "TP8", "56": "P5", "57": "P1", "58": "P2",
           "59": "P6", "60": "PO7", "61": "PO3", "62": "POz", "63": "PO4", "64": "PO8"}
raw.rename_channels(mapping)

montage = mne.channels.make_standard_montage('easycap-M10')
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