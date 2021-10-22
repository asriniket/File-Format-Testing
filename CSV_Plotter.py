import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def plot_data(elements, operation, data):
    width = .25
    if not os.path.exists("Plots/{}".format(filename[:filename.index(".")])):
        os.makedirs("Plots/{}".format(filename[:filename.index(".")]))

    if operation == "Creation_Access":
        x_axis_labels = ["Dataset Creation", "Dataset Access"]
        x_axis = np.arange(len(x_axis_labels))
        hdf5_time = np.array([data.get(data.keys()[0])[6], data.get(data.keys()[1])[6]]).astype(float)
        netcdf_time = np.array([data.get(data.keys()[0])[15], data.get(data.keys()[1])[15]]).astype(float)
        zarr_time = np.array([data.get(data.keys()[0])[24], data.get(data.keys()[1])[24]]).astype(float)
        plt.bar(x_axis - width, hdf5_time, color="r", width=width, edgecolor="black", label="HDF5")
        plt.bar(x_axis, netcdf_time, color="g", width=width, edgecolor="black", label="NetCDF")
        plt.bar(x_axis + width, zarr_time, color="b", width=width, edgecolor="black", label="Zarr")
    else:
        x_axis_labels = ["Integer", "Integer Chunked", "Float", "Float Chunked"]
        x_axis = np.arange(len(x_axis_labels))

        hdf5_time = data.to_numpy()[0:4].astype(float)
        netcdf_time = data.to_numpy()[9:13].astype(float)
        zarr_time = data.to_numpy()[18:22].astype(float)

        if operation == "Resize":
            plt.bar(x_axis - width / 2, hdf5_time, color="r", width=width, edgecolor="black", label="HDF5")
            plt.bar(x_axis + width / 2, zarr_time, color="b", width=width, edgecolor="black", label="Zarr")
        else:
            plt.bar(x_axis - width, hdf5_time, color="r", width=width, edgecolor="black", label="HDF5")
            plt.bar(x_axis, netcdf_time, color="g", width=width, edgecolor="black", label="NetCDF")
            plt.bar(x_axis + width, zarr_time, color="b", width=width, edgecolor="black", label="Zarr")

    plt.xticks(x_axis, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.xlabel("Dataset")
    plt.ylabel("Time (seconds)")
    plt.title("{} elements {} times".format(elements, operation.lower()))
    plt.legend()
    plt.tight_layout()
    plt.savefig("Plots/{}/{}_{}.png".format(filename[:filename.index(".")],
                                            filename[:filename.index("_", filename.index("_") + 1)], operation))
    plt.close()


# def plot_data_OLD(file_format, data):
#     if not os.path.exists("Plots/{}".format(filename)):
#         os.makedirs("Plots/{}".format(filename))
#     x_axis_labels = ["Integer", "Integer Chunked", "Float", "Float Chunked"]
#     creation_access_labels = ["Dataset Creation", "Dataset Access"]
#     write = data.Write.to_numpy()[0:4].astype(float)
#     read = data.Read.to_numpy()[0:4].astype(float)
#     overwrite = data.Overwrite.to_numpy()[0:4].astype(float)
#     resize = data.Resize.to_numpy()[0:4].astype(float)
#     append = data.Append.to_numpy()[0:4].astype(float)
#     creation_access = np.array([data.get(data.keys()[0])[6], data.get(data.keys()[1])[6]]).astype(float)
#
#     x = np.arange(len(x_axis_labels))
#     c = np.arange(len(creation_access_labels))
#
#     plt.figure(1)
#     plt.xticks(x, x_axis_labels)
#     plt.locator_params(axis="y", nbins=20)
#     plt.xlabel("Dataset Type")
#     plt.ylabel("Time (seconds)")
#     plt.bar(x - .25, write, 0.25, label="Write")
#     plt.bar(x, read, 0.25, label="Read")
#     plt.bar(x + .25, append, 0.25, label="Append")
#     plt.title("{} Read/Write/Append Times".format(file_format))
#     plt.legend()
#     plt.tight_layout()
#
#     plt.figure(2)
#     plt.xticks(x, x_axis_labels)
#     plt.locator_params(axis="y", nbins=20)
#     plt.xlabel("Dataset Type")
#     plt.ylabel("Time (seconds)")
#     plt.bar(x, overwrite, .5)
#     plt.title("{} Overwrite Times".format(file_format))
#     plt.tight_layout()
#
#     if not file_format == "NetCDF":
#         plt.figure(3)
#         plt.xticks(x, x_axis_labels)
#         plt.locator_params(axis="y", nbins=20)
#         plt.xlabel("Dataset Type")
#         plt.ylabel("Time (seconds)")
#         plt.bar(x, resize, 0.5)
#         plt.title("{} Resize Times".format(file_format))
#         plt.tight_layout()
#
#     plt.figure(4)
#     plt.xticks(c, creation_access_labels)
#     plt.locator_params(axis="y", nbins=10)
#     plt.xlabel("Dataset Creation/Access")
#     plt.ylabel("Time (seconds)")
#     plt.bar(c, creation_access, .5)
#     plt.title("{} Dataset Creation/Access".format(file_format))
#     plt.tight_layout()
#
#     with PdfPages("Plots/{}/{}.pdf".format(filename, file_format)) as pdf:
#         pdf.savefig(plt.figure(1))
#         pdf.savefig(plt.figure(2))
#         pdf.savefig(plt.figure(3))
#         pdf.savefig(plt.figure(4))
#
#     # plt.plot()
#     # plt.show()
#
#     plt.close(1)
#     plt.close(2)
#     plt.close(3)
#     plt.close(4)

if __name__ == "__main__":
    if not os.path.exists("Plots"):
        os.makedirs("Plots")

    # filename = str(input("Enter the name of the CSV File to plot, excluding the file extension.\n"))
    # output_name = str(input("Enter the size of the data tested.\n"))

    # OLD METHOD (DOES NOT COMPARE FILE FORMATS).
    #
    # data_frame_1 = pd.read_csv('{}.csv'.format(filename), skiprows=0, nrows=7)
    # data_frame_2 = pd.read_csv('{}.csv'.format(filename), skiprows=9, nrows=7)
    # data_frame_3 = pd.read_csv('{}.csv'.format(filename), skiprows=18, nrows=7)
    #
    # plot_data("HDF5", data_frame_1)
    # plot_data("NetCDF", data_frame_2)
    # plot_data("Zarr", data_frame_3)

    filename = "Vector_16777216_results.csv"
    output_name = "[16777216]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

    filename = "Vector_134217728_results.csv"
    output_name = "[134217728]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

    filename = "Matrix_8192_results.csv"
    output_name = "[8192, 8192]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

    filename = "Matrix_16384_results.csv"
    output_name = "[16384, 16384]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

    filename = "Tensor_512_results.csv"
    output_name = "[512, 512, 512]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

    filename = "Tensor_512_1024_results.csv"
    output_name = "[512, 1024, 1024]"
    dataset = pd.read_csv("{}".format(filename))
    plot_data("{}".format(output_name), "Write", dataset.Write)
    plot_data("{}".format(output_name), "Read", dataset.Read)
    plot_data("{}".format(output_name), "Overwrite", dataset.Overwrite)
    plot_data("{}".format(output_name), "Resize", dataset.Resize)
    plot_data("{}".format(output_name), "Append", dataset.Append)
    plot_data("{}".format(output_name), "Creation_Access", dataset)

