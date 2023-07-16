from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib
import os
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams.update({'font.size': 16})

def plot_acf_by_dataset(datasets, data, sensor, changepoints, cpt_idx, figsize, fig_name):
    fig, ax = plt.subplots(nrows=len(datasets), ncols=2, figsize=figsize)
    fig.tight_layout(h_pad=2, w_pad=2)

    for i in range(len(datasets)):
        dataset = datasets[i]
        original_data = data[dataset]["dat"][sensor]
        cpt = cpt_idx[dataset]
        changepoint_indexes = changepoints[dataset][sensor]["indexes"]
        before = original_data.loc[:changepoint_indexes[cpt-1]][-20000:]
        after = original_data.loc[changepoint_indexes[cpt-1]:][0:20000]

        plot_acf(before, ax=ax[i,0], lags=250)
        plot_acf(after, ax=ax[i,1], lags=250)

        if i == 0:
            ax[0,0].set_title("Before")
            ax[0,1].set_title("After")
        else:
            ax[i,0].set_title("")
            ax[i,1].set_title("")

        ax[i,0].set_ylabel('ACF')
        ax[i,1].set_ylabel('ACF')
        ax[i,0].set_xlabel('Lag (s)')
        ax[i,1].set_xlabel('Lag (s)')
    
    for i, ax_row in enumerate(ax):
        # Add the row title to the left of the first subplot in the row
        ax_row[0].text(-0.2, 0.5, datasets[i], rotation=90,
                    va='center', ha='center', transform=ax_row[0].transAxes)

    plt.savefig(os.path.join("Figures",  fig_name), dpi=180, bbox_inches='tight')
    plt.show()