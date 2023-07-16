import os
import ruptures as rpt
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams.update({'font.size': 16})

select_cpts = {'D0400001': {'CH1_Moment': 2,
              'CH2_Kraft': 2,
              'CH3_Biegemo': 1,
              'CH4_SyncSig': 1,
              'CH5_a3_BOZA': 2,
              'CH6_akustik': 3,
              'CH7_a4_Bohrst': 3},
 'D0600001': {'CH1_Moment': 2,
              'CH2_Kraft': 2,
              'CH3_Biegemo': 1,
              'CH4_SyncSig': 1,
              'CH5_a3_BOZA': 2,
              'CH6_akustik': 3,
              'CH7_a4_Bohrst': 3},
 'D0800001': {'CH1_Moment': 2,
              'CH2_Kraft': 2,
              'CH3_Biegemo': 1,
              'CH4_SyncSig': 1,
              'CH5_a3_BOZA': 2,
              'CH6_akustik': 3,
              'CH7_a4_Bohrst': 3},
 'V10_0001': {'CH1_Moment': 5,
              'CH2_Kraft': 6,
              'CH3_SyncSig': 1,
              'CH4_akustik': 4,
              'CH5_a1_WSAS': 3,
              'CH6_a2_WSAF': 3,
              'CH7_a3_BOZA': 4},
 'V17_0001': {'CH1_Moment': 4,
              'CH2_Kraft': 3,
              'CH3_SyncSig': 0,
              'CH4_akustik': 4,
              'CH5_a1_WSAS': 0,
              'CH6_a2_WSAF': 0,
              'CH7_a3_BOZA': 4},
 'V20_0001': {'CH1_Moment': 5,
              'CH2_Kraft': 6,
              'CH3_SyncSig': 0,
              'CH4_akustik': 4,
              'CH5_a1_WSAS': 2,
              'CH6_a2_WSAF': 2,
              'CH7_a3_BOZA': 4},
 'V24_0001': {'CH1_Moment': 5,
              'CH2_Kraft': 5,
              'CH3_SyncSig': 1,
              'CH4_akustik': 2,
              'CH5_a1_WSAS': 2,
              'CH6_a2_WSAF': 2,
              'CH7_a3_BOZA': 4},
 'V25a_001': {'CH1_Moment': 5,
              'CH2_Kraft': 5,
              'CH3_SyncSig': 1,
              'CH4_akustik': 2,
              'CH5_a1_WSAS': 2,
              'CH6_a2_WSAF': 2,
              'CH7_a3_BOZA': 4},
 'V2_00001': {'CH1_Moment': 5,
              'CH2_Kraft': 2,
              'CH3_SyncSig': 1,
              'CH4_akustik': 3,
              'CH5_a1_WSAS': 2,
              'CH6_a2_WSAF': 2,
              'CH7_a3_BOZA': 3},
 'V6_00001': {'CH1_Moment': 5,
              'CH2_Kraft': 6,
              'CH3_SyncSig': 1,
              'CH4_akustik': 4,
              'CH5_a1_WSAS': 3,
              'CH6_a2_WSAF': 3,
              'CH7_a3_BOZA': 4}}


def calculate_changepoints(data, sensor_name, nchp):
    algo = rpt.BottomUp(model="normal", min_size=20000).fit(data[sensor_name].values)
    my_bkps = algo.predict(n_bkps=nchp)
    change_point_indexes = [x - 1 for x in my_bkps ]
    change_points = data["time"].iloc[change_point_indexes]    
    return change_points, change_point_indexes


def generate_changepoints(data, selected_sensors):
    changepoints = {}
    for dataset in data:
        if dataset != 'V2_00001-1':
            result = process_changepoints(data[dataset]["dat"], selected_sensors, select_cpts[dataset])
            changepoints[dataset] = result


    return changepoints

def process_changepoints(data, sensors, nchps):
    results = {}
    for sensor in sensors:
        change_points, indexes = calculate_changepoints(data, sensor, nchps[sensor])
        results[sensor] = {
            "change_points": change_points,
            "indexes": indexes
        }
    
    return results


def plot_change_points(data, change_points, data_set, sensor_name):
    x_value = data[data_set]["dat"]["time"]
    hdr = data[data_set]["hdr"]
    y_value = data[data_set]["dat"][sensor_name]
    plt.figure(figsize=(10, 6))
    plt.plot(x_value.values, y_value.values)
    plt.ylabel(sensor_name + " (" + hdr.vert_units[hdr.channel_names.index(sensor_name)] + ")")
    plt.xlabel("Time (s)")
    for xc in change_points[data_set][sensor_name]["change_points"]:
        plt.axvline(x=xc,color='red')

    plt.savefig(os.path.join("Figures", data_set, data_set + "_" + sensor_name + "_cp.pdf"), dpi=180, bbox_inches='tight')
    plt.show()


def plot_change_points_mult(datasets, data, change_points, sensor_name, fig_size, fig_name):
    fig, axs = plt.subplots(len(datasets), 1, figsize=fig_size)
    fig.tight_layout(h_pad=3)
    for i in range(len(datasets)):
        data_set = datasets[i]
        x_value = data[data_set]["dat"]["time"]
        hdr = data[data_set]["hdr"]
        y_value = data[data_set]["dat"][sensor_name]
        axs[i].plot(x_value.values, y_value.values)
        axs[i].set_ylabel(sensor_name + " (" + hdr.vert_units[hdr.channel_names.index(sensor_name)] + ")")
        axs[i].set_xlabel("Time (s)")
        axs[i].set_title(data_set)
        for xc in change_points[data_set][sensor_name]["change_points"]:
            axs[i].axvline(x=xc,color='red')
        axs[i].grid()
    
    plt.savefig(os.path.join("Figures",  fig_name), dpi=180, bbox_inches='tight')
    plt.show()