import numpy as np
import scipy
import mne
from pathlib import Path
import matplotlib
from preprocessing import read_raw
matplotlib.use('TkAgg')
import matplotlib.colors as colors
from matplotlib import pyplot as plt
import math

def tf_analysis(data, min_freq = 2, max_freq = 20, fs=500, n_cycles=None):
    # define frequency range
    num_frex = int(max_freq - min_freq / 2)
    # define wavelet parameters
    time = np.arange(-1, 1, 1 / fs)
    frex = np.logspace(np.log10(min_freq), np.log10(max_freq), num_frex)
    # number of cycles of morlet wavelet as function of frequency (more cycles with increasing wavelet frequency)
    if not n_cycles:
        n_cycles = np.logspace(np.log10(3), np.log10(10), num_frex) / (2 * np.pi * frex)
    else:
        n_cycles = np.ones_like(frex) * n_cycles
    # define convolution parameters
    n_wavelet = len(time)
    n_data = len(data)
    n_convolution = n_wavelet + n_data - 1
    n_conv_pow2 = 2 ** (math.ceil(math.log(n_convolution, 2)))
    half_of_wavelet_size = int((n_wavelet - 1) / 2)
    # get FFT of data
    eeg_fft = np.fft.fft(data, n_conv_pow2)
    # initialize
    eeg_power = np.zeros((num_frex, n_data))  # frequencies X time
    # loop through frequencies and compute synchronization
    for fi in range(num_frex):
        wavelet_fft = \
        np.fft.fft(np.sqrt(1 / (n_cycles[fi] * np.sqrt(np.pi)))  #todo empirical scaling factor for varying wavelet cycles
                   # complex sine at different frequencies
                   * np.exp(2 * 1j * np.pi * frex[fi] * time)
                   # gaussian with s cycles
                   * np.exp(-time ** 2 / (2 * (n_cycles[fi] ** 2))), n_conv_pow2)  # more cycles with increasing wavelet frequency
        # convolution
        eeg_conv = np.fft.ifft(wavelet_fft * eeg_fft)  # convolve
        eeg_conv = eeg_conv[:n_convolution]  # cut result to length of n_convolution
        eeg_conv = eeg_conv[half_of_wavelet_size + 1: n_convolution - half_of_wavelet_size]
        # calculate power
        temp_power = (np.abs(eeg_conv) ** 2)
        # # baseline normalization
        eeg_power[fi] = 10*np.log10(temp_power)
    return eeg_power

def plot_tf_data(data, fs=500, min_freq=2, max_freq=20, axis=None):
    time = np.arange(0, len(data[1]) / fs, 1 / fs)  # start, stop, step size
    num_frex = int(max_freq - min_freq / 2)
    frex = np.logspace(np.log10(min_freq), np.log10(max_freq), num_frex)
    # plot
    x, y = np.meshgrid(time, frex)
    if not axis:
        fig, ax = plt.subplots(1, 1, sharex=True, sharey=True)
    c_ax = ax.contour(x, y, data, linewidths=0.3, colors="k", norm=colors.Normalize())
    c_ax = ax.contourf(x, y, data, norm=colors.Normalize(), cmap=plt.cm.jet)
    cbar = fig.colorbar(c_ax)
    plt.show()
    # plt.vlines(0, ymin=frex.min(), ymax=frex.max(), colors='k', linestyles='dashed')
    # plt.title(list(event_id.keys())[list(event_id.values()).index(stim_id)])


"""
DIR = Path.cwd()
eeg_DIR = DIR / "data"
subdir = '100 bpm'
filename = 'record-[2022.11.04-17.23.44].vhdr'
filepath = eeg_DIR / subdir / filename

raw = read_raw(filepath)

# wavelet convolution

fs = raw.info['sfreq']

raw.set_eeg_reference(ref_channels=['Fz'])

eeg_data = raw._data[22]

# get stimulus onset times (up: 1, down: 2, left: 3, right: 4, front: 5)
# select stimulus
stim_id = 3

# set epoch times
tmin=-0.2
tmax=0.3

stim_times = events[events[:, 2] == stim_id][:, 0]
epoch_tf = np.zeros((len(stim_times), num_frex, int(tmax*fs-tmin*fs)))

# get epoch data
for i in range(len(stim_times)):
    # get data around each event
    epoch_tf[i] = eeg_power[:, stim_times[i]+int(fs*tmin):stim_times[i]+int(fs*tmax)]
    # baseline
    for fi in range(num_frex):
        epoch_tf[i, fi] = epoch_tf[i, fi] / np.mean(epoch_tf[i, fi, :int(-tmin * fs)])
# average across epochs
evoked_tf = np.mean(epoch_tf, axis=0)
"""
