import numpy
import scipy
import mne
from pathlib import Path
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

DIR = Path.cwd()
eeg_DIR = DIR / "data"
subdir = '100 bpm'
filename = 'record-[2022.11.04-17.23.44].vhdr'
filepath = eeg_DIR / subdir / filename

def read_raw(filepath):
    # read raw, get montage and events
    raw = mne.io.read_raw_brainvision(filepath, preload=True)
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
    return raw, events

def epoch_data(raw, events, baseline=True, reference=['Fz'], tmin=-0.2, tmax=0.5,
               reject_criteria=dict(eeg=800e-6), flat_criteria=None, event_id={'snare': 10003, 'base': 10002}):
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, reject=reject_criteria, flat=flat_criteria,
                        reject_by_annotation=True, preload=True, baseline=None, event_repeated='error')
    if baseline:
        baseline = (tmin, 0)
        epochs.apply_baseline(baseline)
        # epochs.average().plot()
    # rereference
    # epochs.plot_sensors(kind="topomap", ch_type='all')
    if reference is not None:
        epochs.set_eeg_reference(ref_channels=['Fz'])
    return epochs


"""
# compare gfp for both conditions
evoked_snare = epochs['snare'].average()
evoked_base = epochs['base'].average()
mne.viz.plot_compare_evokeds([evoked_snare, evoked_base], title='ERP')

# compare temporal electrodes left v right
evoked_snare_left = epochs['snare'].pick_channels(['T7']).average()
evoked_snare_right = epochs['snare'].pick_channels(['T8']).average()
evoked_base_left = epochs['base'].pick_channels(['T7']).average()
evoked_base_right = epochs['base'].pick_channels(['T8']).average()
mne.viz.plot_compare_evokeds([evoked_snare_left,
                              evoked_base_left], title='ERP left')
mne.viz.plot_compare_evokeds([evoked_snare_right,
                              evoked_base_right], title='ERP right')
"""