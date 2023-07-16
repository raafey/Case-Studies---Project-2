import scipy.signal as signal
import numpy as np
import os
from scipy.signal import find_peaks
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams.update({'font.size': 16})

def generate_points(breaking_points, sensor_data, cpt):
    # take the 10000 observations before each break point:
    before = sensor_data.loc[:breaking_points[cpt]][-20000:]
    after = sensor_data.loc[breaking_points[cpt]:][0:20000]

    data_bf = before.values.reshape(-1)
    data_af = after.values.reshape(-1)

    data_bf_af = np.concatenate((data_bf, data_af), axis=None)

    return data_bf_af


def calculate_eigen_freq(data, frequency, amp):
    freq, psd = signal.welch(data, fs=frequency, nperseg=1024)
    peaks, _ = find_peaks(psd, height=amp)
    
    return freq, psd, peaks


def generate_eigen_freqs(data, changepoints, sensor, cpts, amp):
    eigen_freqs = {}
    for dataset in cpts:
        eigen_freqs[dataset] = {}
        if type(changepoints[dataset]) == dict:
            changepoint_indexes = changepoints[dataset][sensor]["indexes"]
        elif type(changepoints[dataset]) == list:
            changepoint_indexes = changepoints[dataset]
        dp = generate_points(changepoint_indexes, data[dataset]["dat"][sensor], cpts[dataset]-1)

        freq, psd, peaks = calculate_eigen_freq(dp, 20000, amp)
        eigen_freqs[dataset][sensor] = {
            "freq": freq,
            "psd": psd, 
            "peaks": peaks,
        }

    return eigen_freqs


def plot_eigen_freq(datasets, eigen_freqs, sensor, fig_size, fig_name):
    fig, axs = plt.subplots(len(datasets), 1, figsize=fig_size)
    fig.tight_layout(h_pad=3)
    for i in range(len(datasets)):
        data_set = datasets[i]
        x_value = eigen_freqs[data_set][sensor]["freq"]
        y_value = eigen_freqs[data_set][sensor]["psd"]
        axs[i].plot(x_value, y_value)
        axs[i].set_ylabel(r'PSD $(V^2/Hz)$')
        axs[i].set_xlabel("Frequency (Hz)")
        axs[i].set_title(data_set)
    
    plt.savefig(os.path.join("Figures",  fig_name), dpi=180, bbox_inches='tight')
    plt.show()

def get_freq_info(eigen_info):
    freq = eigen_info["freq"]
    psd = eigen_info["psd"]
    peaks = eigen_info["peaks"]
    peaks_s = peaks[np.argsort(psd[peaks])[-10:]]
    peaks_s = np.sort(peaks_s)[::-1]
    top_freqs = freq[peaks_s][:5]
    top_psds = psd[peaks_s][:len(top_freqs)]
    # top_psds = np.sort(psd)[-10:][::-1][:len(top_freqs)]
    return {
        "top_freq": top_freqs,
        "top_psds": top_psds
    }

def print_freq_infos(eigen_freqs, dataset, sensor):
    for dataset in eigen_freqs:
        print(dataset)
        pprint(get_freq_info(eigen_freqs[dataset][sensor]))