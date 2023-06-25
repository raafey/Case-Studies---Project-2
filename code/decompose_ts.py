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
from matplotlib.backends.backend_pdf import PdfPages
from statsmodels.tsa.seasonal import seasonal_decompose


matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams.update({'font.size': 16})


def decompose_ts_dataset(data, data_set, plot_fig=False):
    dat = data[data_set]["dat"]
    hdr = data[data_set]["hdr"]
    channel_names = hdr.channel_names
    results = {}
    for channel in channel_names:
        df = dat[["time", channel]]
        df.set_index('time', inplace=True)
        result = decompose_ts(df, channel, hdr.rate)
        results[channel] = result
        if plot_fig:
            plot_decomposed_ts(result, data_set, channel)
    
    return results


def decompose_ts(df, channel_name, period):
    result = seasonal_decompose(df[channel_name], period=period, model='additive', extrapolate_trend='freq')
    return result


def plot_decomposed_ts(result, data_set, channel):
    fig = result.plot()
    fig.set_size_inches((16, 9))
    plt.xlabel("Time (s)")
    plt.savefig(os.path.join("Figures", data_set, data_set + "_" + channel + "_TS_decomp.png"), dpi=200, bbox_inches='tight')
    # plt.show()
