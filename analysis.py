import mne
from pathlib import Path
import matplotlib
from preprocessing import read_raw, epoch_data
from tf_analysis import tf_analysis, plot_tf_data
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

DIR = Path.cwd()
eeg_DIR = DIR / "data"
subdir = '180 bpm'
filename = 'record-[2022.11.04-17.27.07].vhdr'
filepath = eeg_DIR / subdir / filename

# read raw
raw, events = read_raw(filepath)
raw.filter(l_freq=1, h_freq=None)  # filter

# raw.plot()
raw.info['bads'] += ['P4']  # drop bad channels
raw.interpolate_bads  # interpolate bad channels

# ICA
ica = mne.preprocessing.ICA(n_components=0.99, method="fastica")
ica.fit(raw)
ica.plot_components()  # plot components
# ica_sources = ica.get_sources(epochs)
# ica_sources.plot(picks="all")  # plot time trace of components
# ica.plot_properties(epochs, picks=[0])  # take a closer look
ica.exclude = [0, 1, 2]  # remove selected components
ica.apply(raw)  # apply ICA

# plot topomap
# raw.plot_psd_topomap()

# tf analysis
# data = raw.pick_channels(['Fz'])._data[0]
# min_freq = 2
# max_freq = 30
# tf_data = tf_analysis(data, min_freq=min_freq, max_freq=max_freq, fs=500, n_cycles=30)
# plot_tf_data(tf_data, min_freq=min_freq, max_freq=max_freq, fs=500)

# epoch, trial_rejection, re-reference and baseline
epochs = epoch_data(raw, events, baseline=True, reference=None, tmin=-0.2, tmax=0.5,
        reject_criteria=dict(eeg=800e-6), flat_criteria=None, event_id={'snare': 10003, 'base': 10002})

# evoked_snare = epochs['snare'].average()
# evoked_base = epochs['base'].average()
# mne.viz.plot_compare_evokeds([evoked_snare, evoked_base], title='ERP')

# compare temporal electrodes left v right
evoked_snare = epochs['snare'].pick_channels(['T7']).average()
evoked_base = epochs['base'].pick_channels(['T7']).average()
mne.viz.plot_compare_evokeds([evoked_snare, evoked_base], title='ERP')

