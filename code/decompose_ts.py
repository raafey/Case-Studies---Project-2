# Project: 2

# Group: 3

# Group Members:
#  - Muhammad Raafey Tariq (231806)
#  - Farrukh Ahmed (230614)
#  - Amirreza Khamehchin Khiabani (230891)
#  - Aymane Hachcham (236392)



import os
import matplotlib
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose


matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams.update({'font.size': 16})


def decompose_ts_dataset(data, data_set):
    dat = data[data_set]["dat"]
    channel_names = data[data_set]["hdr"].channel_names
    results = {}
    for channel in channel_names:
        result = decompose_ts(dat[channel])
        results[channel] = result
        plot_decomposed_ts(result, data_set, channel)
    
    return results


def decompose_ts(dat):
    result = seasonal_decompose(dat, model='additive')
    return result


def plot_decomposed_ts(result, data_set, channel):
    result.plot()
    plt.savefig(os.path.join("Figures", data_set, data_set + "_" + channel + "_TS_decomp.pdf"), dpi=180, bbox_inches='tight')
    plt.show()
    
