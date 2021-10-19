import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages


def plot_data(file_format, data):
    if not os.path.exists("Plots/{}".format(filename)):
        os.makedirs("Plots/{}".format(filename))
    x_axis_labels = ["Integer", "Integer Chunked", "Float", "Float Chunked"]
    creation_access_labels = ["Dataset Creation", "Dataset Access"]
    write = data.Write.to_numpy()[0:4].astype(float)
    read = data.Read.to_numpy()[0:4].astype(float)
    overwrite = data.Overwrite.to_numpy()[0:4].astype(float)
    resize = data.Resize.to_numpy()[0:4].astype(float)
    append = data.Append.to_numpy()[0:4].astype(float)
    creation_access = np.array([data.get(data.keys()[0])[6], data.get(data.keys()[1])[6]]).astype(float)

    x = np.arange(len(x_axis_labels))
    c = np.arange(len(creation_access_labels))

    plt.figure(1)
    plt.xticks(x, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.xlabel("Dataset Type")
    plt.ylabel("Time (seconds)")
    plt.bar(x - .25, write, 0.25, label="Write")
    plt.bar(x, read, 0.25, label="Read")
    plt.bar(x + .25, append, 0.25, label="Append")
    plt.title("{} Read/Write/Append Times".format(file_format))
    plt.legend()

    plt.figure(2)
    plt.xticks(x, x_axis_labels)
    plt.locator_params(axis="y", nbins=20)
    plt.xlabel("Dataset Type")
    plt.ylabel("Time (seconds)")
    plt.bar(x, overwrite, .5)
    plt.title("{} Overwrite Times".format(file_format))

    if not file_format == "NetCDF":
        plt.figure(3)
        plt.xticks(x, x_axis_labels)
        plt.locator_params(axis="y", nbins=20)
        plt.xlabel("Dataset Type")
        plt.ylabel("Time (seconds)")
        plt.bar(x, resize, 0.5)
        plt.title("{} Resize Times".format(file_format))

    plt.figure(4)
    plt.xticks(c, creation_access_labels)
    plt.locator_params(axis="y", nbins=10)
    plt.xlabel("Dataset Creation/Access")
    plt.ylabel("Time (seconds)")
    plt.bar(c, creation_access, .5)
    plt.title("{} Dataset Creation/Access".format(file_format))

    with PdfPages("Plots/{}/{}.pdf".format(filename, file_format)) as pdf:
        pdf.savefig(plt.figure(1))
        pdf.savefig(plt.figure(2))
        pdf.savefig(plt.figure(3))
        pdf.savefig(plt.figure(4))

    # plt.plot()
    # plt.show()

    plt.close(1)
    plt.close(2)
    plt.close(3)
    plt.close(4)


if __name__ == "__main__":
    if not os.path.exists("Plots"):
        os.makedirs("Plots")

    filename = str(input("Enter the name of the CSV File to plot, excluding the file extension.\n"))

    data_frame_1 = pd.read_csv('{}.csv'.format(filename), skiprows=0, nrows=7)
    data_frame_2 = pd.read_csv('{}.csv'.format(filename), skiprows=9, nrows=7)
    data_frame_3 = pd.read_csv('{}.csv'.format(filename), skiprows=18, nrows=7)

    plot_data("HDF5", data_frame_1)
    plot_data("NetCDF", data_frame_2)
    plot_data("Zarr", data_frame_3)
