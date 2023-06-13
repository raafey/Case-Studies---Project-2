import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime
from pprint import pprint


class ReadHdrFile:
    def __init__(self, file_path):
        self.dataset = None
        self.version = None
        self.channel_names = None
        self.mix_mode = None
        self.date_time = None
        self.external_sampling = None
        self.vert_units = None
        self.horz_units = None
        self.comment = None
        self.num_channels = None
        self.strg_mode = None
        self.file_type = None
        self.slope = None
        self.x_offset = None
        self.y_offset = None
        self.num_samples = None
        self.uq_device = None
        self.device = None
        self.channel_info = None
        self.channel_slots = None
        self.clock = None

        self.file_path = file_path
        hdr_data = self.__read_hdr_data()

        if "DATASET" in hdr_data:
            self.dataset = hdr_data["DATASET"][0]
        
        if "VERSION" in hdr_data:
            self.version = hdr_data["VERSION"][0]
        
        if "SERIES" in hdr_data:
            self.channel_names = hdr_data["SERIES"]
        
        if self.channel_names is not None:
            self.mix_mode = False
            for name in self.channel_names:
                if "MEMO" in name:
                    self.mix_mode = True
                    break
        
        if "DATE" in hdr_data and "TIME" in hdr_data:
            self.date_time = datetime.strptime(hdr_data["DATE"][0] + " " + hdr_data["TIME"][0].replace(".00", ""), '%m-%d-%Y %H:%M:%S')
        
        if "RATE" in hdr_data:
            self.rate = int(hdr_data["RATE"][0])
        
        if self.rate is not None:
            self.external_sampling = False
            if self.rate == 1:
                self.external_sampling = True

        if "VERT_UNITS" in hdr_data:
            self.vert_units = hdr_data["VERT_UNITS"][0]
        
        if "HORZ_UNITS" in hdr_data:
            self.horz_units = hdr_data["HORZ_UNITS"][0]
        
        if "COMMENT" in hdr_data:
            self.comment = hdr_data["COMMENT"]
        
        if "NUM_SERIES" in hdr_data:
            self.num_channels = int(hdr_data["NUM_SERIES"][0])
        
        if "STORAGE_MODE" in hdr_data:
            self.strg_mode = hdr_data["STORAGE_MODE"][0]
        
        if "FILE_TYPE" in hdr_data:
            self.file_type = hdr_data["FILE_TYPE"][0]
        
        if "SLOPE" in hdr_data:
            self.slope = [float(x) for x in hdr_data["SLOPE"]]
        
        if "X_OFFSET" in hdr_data:
            self.x_offset = [float(x) for x in hdr_data["X_OFFSET"]]
        
        if "Y_OFFSET" in hdr_data:
            self.y_offset = [float(x) for x in hdr_data["Y_OFFSET"]]
        
        if "NUM_SAMPS" in hdr_data:
            self.num_samples = int(hdr_data["NUM_SAMPS"][0])
        
        self.uq_device = "DATA" in hdr_data.keys()

        if "DEVICE" in hdr_data:
            self.device = hdr_data["DEVICE"][0]
        
        channels = self.__resolve_channels(hdr_data)
        self.channel_info = channels

        if "CH_SLOT" in hdr_data:
            self.channel_slots = [int(x) for x in hdr_data["CH_SLOT"]]
        
        if "CLOCK" in hdr_data:
            self.clock = hdr_data["CLOCK"]
    

    def print_values(self):
        value_dict = {}
        value_dict["dataset"] = self.dataset
        value_dict["version"] = self.version
        value_dict["channel_names"] = self.channel_names
        value_dict["mix_mode"] = self.mix_mode
        value_dict["date_time"] = self.date_time
        value_dict["rate"] = self.rate
        value_dict["externam_sampling"] = self.external_sampling
        value_dict["vert_units"] = self.vert_units
        value_dict["horz_units"] = self.horz_units
        value_dict["comment"] = self.comment
        value_dict["channels"] = self.num_channels
        value_dict["strg_mode"] = self.strg_mode
        value_dict["file_type"] = self.file_type
        value_dict["slope"] = self.slope
        value_dict["x_offset"] = self.x_offset
        value_dict["y_offset"] = self.y_offset
        value_dict["num_samples"] = self.num_samples
        value_dict["uq_device"] = self.uq_device
        value_dict["device"] = self.device
        value_dict["channel_info"] = self.channel_info
        value_dict["channel_slots"] = self.channel_slots
        value_dict["clock"] = self.clock

        pprint(value_dict)

    def __filter_channel(self, channel):
        info = {
            "amplifier": None,
            "range": None,
            "filter": None,
        }

        if type(channel) == list:
            info["amplifier"] = channel[0]
            if len(channel) > 1:
                _range = channel[1].replace("RANGE=", "").replace("V", "")
                info["range"] = float(_range)
                _filter = channel[2].replace("FILTER=", "")
                info["filter"] = not _filter == "OFF"
        else:
            info["amplifier"] = channel,

        return info

    def __resolve_channels(self, hdr_data):
        return {
            "CH1_1": self.__filter_channel(hdr_data["CH1_1"]),
            "CH2_2": self.__filter_channel(hdr_data["CH2_2"]),
            "CH3_3": self.__filter_channel(hdr_data["CH3_3"]),
            "CH4_4": self.__filter_channel(hdr_data["CH4_4"]),
            "CH5_5": self.__filter_channel(hdr_data["CH5_5"]),
            "CH6_6": self.__filter_channel(hdr_data["CH6_6"]),
            "CH7_7": self.__filter_channel(hdr_data["CH7_7"]),
            "CH8_8": self.__filter_channel(hdr_data["CH8_8"]),
            "CH9_9": self.__filter_channel(hdr_data["CH9_9"]),
            "CH10_10": self.__filter_channel(hdr_data["CH10_10"]),
            "CH11_11": self.__filter_channel(hdr_data["CH11_11"]),
            "CH12_12": self.__filter_channel(hdr_data["CH12_12"]),
        }


    def __read_hdr_data(self):
        hdr_data = {}
        with open(self.file_path, 'r', encoding="latin-1") as header_file:
            for line in header_file:
                line = "".join(list(line)).replace("\n", "").strip()
                if "GX-1_SYS" in line:
                    break
                if line != "":
                    comps = line.split(",")
                    comps = [x.strip() for x in comps]

                    key = None

                    if len(comps) > 1:
                        val_0 = comps[0].split(" ")
                        comps = [val_0[1]] + comps[1:len(comps)]
                        key = val_0[0]
                    else:
                        val_0 = comps[0].split(" ")
                        key = val_0[0]
                        if len(val_0) > 1:
                            comps = val_0[1]
                        else:
                            comps = []

                    if type(comps) != list:
                        comps = [comps]

                    hdr_data[key] = comps
        
        
        return hdr_data


def read_bin_file(file_path, header_obj):
    data = pd.read_csv(file_path, header=0)
    data.columns = header_obj.channel_names

    return data



def plot_channel(data, channel_name, slope, y_offset, x_label, y_label, dataset):
    values = data[channel_name].to_numpy()
    values = values * slope + y_offset
    # increase the size of the labels in the plot
    plt.rcParams.update({'font.size': 15})

    plt.figure(figsize=(10, 6))
    plt.plot(values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(channel_name)
    plt.savefig(os.path.join("Figures", dataset + "_" + channel_name + ".pdf"))
    plt.show()

# function to clear Figures directory
def clear_figures():
    folder = './Figures'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            continue