import os

import matplotlib.pyplot as plt
import numpy as np


def plot_data(filename, title, arr_hdf5, arr_netcdf, arr_zarr):
    if not os.path.exists("Plots"):
        os.makedirs("Plots")
    # Convert to numpy.
    # 0th Index of 2D array represents Creation time, 1st Index Write time, 2nd Index Open Time, 3rd Index Read time.
    hdf5_arr = np.array(arr_hdf5[1:])
    netcdf_arr = np.array(arr_netcdf[1:])
    zarr_arr = np.array(arr_zarr[1:])

    # Creation / Open Arrays
    plt.title(title + " Elements Dataset Create / Open Times")
    plt.xlabel("Operation")
    plt.ylabel("Time (seconds)")
    width = .25
    x_axis_labels = ["Dataset Create", "Dataset Open"]
    x_axis = np.arange(len(x_axis_labels))
    plt.bar(x_axis - width,
            [np.mean(hdf5_arr[0]), np.mean(hdf5_arr[2])],
            yerr=[np.std(hdf5_arr[0]), np.std(hdf5_arr[2])],
            capsize=10, color="r", width=width, edgecolor="black", label="HDF5")
    plt.bar(x_axis,
            [np.mean(netcdf_arr[0]), np.mean(netcdf_arr[2])],
            yerr=[np.std(netcdf_arr[0]), np.std(netcdf_arr[2])],
            capsize=10, color="g", width=width, edgecolor="black", label="NetCDF")
    plt.bar(x_axis + width,
            [np.mean(zarr_arr[0]), np.mean(zarr_arr[2])],
            yerr=[np.std(zarr_arr[0]), np.std(zarr_arr[2])],
            capsize=10, color="b", width=width, edgecolor="black", label="Zarr")
    plt.xticks(x_axis, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.ylim(ymin=0)
    plt.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig("Plots/{}_Create_Open.png".format(filename), bbox_inches='tight')
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
    plt.bar(x_axis - width,
            [np.mean(hdf5_arr[1]), np.mean(hdf5_arr[3])],
            yerr=[np.std(hdf5_arr[1]), np.std(hdf5_arr[3])],
            capsize=10, color="r", width=width, edgecolor="black", label="HDF5")
    plt.bar(x_axis,
            [np.mean(netcdf_arr[1]), np.mean(netcdf_arr[3])],
            yerr=[np.std(netcdf_arr[1]), np.std(netcdf_arr[3])],
            capsize=10, color="g", width=width, edgecolor="black", label="NetCDF")
    plt.bar(x_axis + width,
            [np.mean(zarr_arr[1]), np.mean(zarr_arr[3])],
            yerr=[np.std(zarr_arr[1]), np.std(zarr_arr[3])],
            capsize=10, color="b", width=width, edgecolor="black", label="Zarr")
    plt.xticks(x_axis, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.ylim(ymin=0)
    plt.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig("Plots/{}_Read_Write.png".format(filename), bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
