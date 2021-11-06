import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_data(csv, title):
    if not os.path.exists("Plots"):
        os.makedirs("Plots")
    dataframe = pd.read_csv(csv + ".csv")

    # Creation / Open Arrays
    plt.title(title + " Elements Dataset Create / Open Times")
    plt.xlabel("Operation")
    plt.ylabel("Time (seconds)")
    width = .25
    x_axis_labels = ["Dataset Create", "Dataset Open"]
    x_axis = np.arange(len(x_axis_labels))
    hdf5_time = (dataframe.to_numpy()[0][1:5:2].astype(float))
    netcdf_time = (dataframe.to_numpy()[1][1:5:2].astype(float))
    zarr_time = (dataframe.to_numpy()[2][1:5:2].astype(float))
    plt.bar(x_axis - width, hdf5_time, color="r", width=width, edgecolor="black", label="HDF5")
    plt.bar(x_axis, netcdf_time, color="g", width=width, edgecolor="black", label="NetCDF")
    plt.bar(x_axis + width, zarr_time, color="b", width=width, edgecolor="black", label="Zarr")
    plt.xticks(x_axis, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Plots/{}_Create_Open.png".format(csv))
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    # Read / Write Arrays
    plt.title(title + " Elements Dataset Read / Write Times")
    plt.xlabel("Operation")
    plt.ylabel("Time (seconds)")
    width = .25
    x_axis_labels = ["Dataset Write", "Dataset Read"]
    x_axis = np.arange(len(x_axis_labels))
    hdf5_time = (dataframe.to_numpy()[0][2:5:2].astype(float))
    netcdf_time = (dataframe.to_numpy()[1][2:5:2].astype(float))
    zarr_time = (dataframe.to_numpy()[2][2:5:2].astype(float))
    plt.bar(x_axis - width, hdf5_time, color="r", width=width, edgecolor="black", label="HDF5")
    plt.bar(x_axis, netcdf_time, color="g", width=width, edgecolor="black", label="NetCDF")
    plt.bar(x_axis + width, zarr_time, color="b", width=width, edgecolor="black", label="Zarr")
    plt.xticks(x_axis, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Plots/{}_Read_Write.png".format(csv))
    # plt.show()
    plt.clf()
    plt.cla()
    plt.close()
