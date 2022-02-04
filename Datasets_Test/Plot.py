import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
def plot(file_formats, num_datasets, dimensions):
        if not os.path.exists("Data/Plots"):
                os.mkdir("Data/Plots")
        create_time, write_time, open_time, read_time, error = process_csv(file_formats, num_datasets, dimensions)
        width = .25

        plt.figure(1)
        plt_labels = ["Dataset Read Time", "Dataset Write Time"]
        x = np.arange(len(plt_labels))
        offset = -width
        plt.ylabel("Average Time (s)")
        plt.title(f"{num_datasets} Datasets {dimensions} Elements Dataset Read / Write Times")
        plt.xticks(x, plt_labels)
        for i in range(0, len(file_formats)):
                # Error format: Each row represents one file format.
                bar_read_write = plt.bar(x + offset, [read_time[i], write_time[i]], width, label=file_formats[i], edgecolor="black", yerr=[error[i][3], error[i][1]])
                plt.bar_label(bar_read_write,padding=3)
                offset+=width
        plt.legend()
        plt.tight_layout()      
        plt.savefig(f"Data/Plots/{num_datasets}_{dimensions}_Read_Write.png")
        plt.show()

        plt.figure(2)
        plt_labels = ["Dataset Create Time", "Dataset Open Time"]
        x = np.arange(len(plt_labels))
        offset = -width
        plt.ylabel("Average Time (s)")
        plt.title(f"{num_datasets} Datasets {dimensions} Elements Dataset Create / Open Times")
        plt.xticks(x, plt_labels)
        for i in range(0, len(file_formats)):
                bar_create_open = plt.bar(x + offset, [create_time[i], open_time[i]], width, label=file_formats[i], edgecolor="black", yerr=[error[i][0], error[i][2]])
                plt.bar_label(bar_create_open, padding=3)
                offset+=width
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"Data/Plots/{num_datasets}_{dimensions}_Create_Open.png")
        plt.show()
        
        plt.cla()
        plt.clf()

def process_csv(file_formats, num_datasets, dimensions):
        total_dataset_create_time = []
        total_dataset_write_time = []
        total_dataset_open_time = []
        total_dataset_read_time = []
        error = []
        for file_format in file_formats:
                df = pd.read_csv(f"Data/{file_format}_{num_datasets}_{dimensions}.csv")
                dataset_create_time, dataset_write_time, dataset_open_time, dataset_read_time = df.iloc[:, 1:].mean(axis=0)
                create_deviation, write_deviation, open_deviation, read_deviation = df.iloc[:, 1:].std(axis=0)
                total_dataset_create_time.append(dataset_create_time)
                total_dataset_write_time.append(dataset_write_time)
                total_dataset_open_time.append(dataset_open_time)
                total_dataset_read_time.append(dataset_read_time)
                error.append([create_deviation, write_deviation, open_deviation, read_deviation])
                if df.iloc[-1, 0] == "Average":
                        continue
                average_values = pd.DataFrame({
                        file_format : "Average", 
                        "Dataset Creation Time" : [dataset_create_time], 
                        "Dataset Write Time" : [dataset_write_time], 
                        "Dataset Open Time" : [dataset_open_time], 
                        "Dataset Read Time" : [dataset_read_time]
                })
                df = pd.concat([df, average_values], ignore_index = True)
                df.to_csv(f"Data/{file_format}_{num_datasets}_{dimensions}.csv", index=False)
        return total_dataset_create_time, total_dataset_write_time, total_dataset_open_time, total_dataset_read_time, error

if __name__ == "__main__":
        file_formats = ["HDF5", "NetCDF", "Zarr"]
        plot(file_formats, 10, "[25, 25, 25]")
