import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# from matplotlib.backends.backend_pdf import PdfPages


def plot_data(file_format, data, is_creation):
    if not is_creation:
        x_axis_labels = ["Integer", "Integer Chunked", "Float", "Float Chunked"]
        write = data.Write.to_numpy()
        read = data.Read.to_numpy()
        overwrite = data.Overwrite.to_numpy()
        resize = data.Resize.to_numpy()
        append = data.Append.to_numpy()
        x = np.arange(len(x_axis_labels))

        plt.xticks(x, x_axis_labels)
        plt.xlabel("Dataset Type")
        plt.ylabel("Time (seconds)")

        plt.figure(1)
        plt.bar(x - .2, write, 0.2, label="Write")
        plt.bar(x, read, 0.2, label="Read")
        plt.bar(x + .2, append, 0.2, label="Append")
        plt.title("{} Read/Write/Append Times".format(file_format))
        plt.legend()

        plt.figure(2)
        plt.bar(x, overwrite, .5, label="Overwrite")
        plt.title("{} Overwrite Times".format(file_format))
        plt.legend()

        plt.figure(3)
        plt.bar(x, resize, 0.5, label="Resize")
        plt.title("{} Resize Times".format(file_format))
        plt.legend()

        # with PdfPages('{}.pdf'.format(file_format)) as pdf:
        #     pdf.savefig(plt.figure(1))
        #     pdf.savefig(plt.figure(2))
        #     pdf.savefig(plt.figure(3))

        plt.figure(1).savefig("{}_Read_Write_Append.png".format(file_format))
        plt.figure(2).savefig("{}_Overwrite.png".format(file_format))
        plt.figure(3).savefig("{}_Resize.png".format(file_format))
        plt.close(1)
        plt.close(2)
        plt.close(3)
    else:
        # x_axis_labels = ["Dataset Creation", "Dataset Access"]
        time = data.to_numpy()
        time_dict = {"Dataset Creation Time": time[0][0], "Dataset Access Time": time[0][1]}
        plt.ylabel("Time (seconds)")
        plt.figure(1)
        plt.bar(time_dict.keys(), time_dict.values())
        plt.title("{} Dataset Creation/Access".format(file_format))
        plt.figure(1).savefig("{}_Creation_Access.png".format(file_format))
        plt.close(1)


if __name__ == "__main__":
    # filename = str(input("Enter the name of the CSV File to plot, excluding the file extension.\n"))
    filename = "Vector_16777216_results"
    data_frame_1 = pd.read_csv('{}.csv'.format(filename), skiprows=0, nrows=4)
    data_frame_2 = pd.read_csv('{}.csv'.format(filename), skiprows=6, nrows=1)

    data_frame_3 = pd.read_csv('{}.csv'.format(filename), skiprows=9, nrows=4)
    data_frame_4 = pd.read_csv('{}.csv'.format(filename), skiprows=15, nrows=1)

    data_frame_5 = pd.read_csv('{}.csv'.format(filename), skiprows=18, nrows=4)
    data_frame_6 = pd.read_csv('{}.csv'.format(filename), skiprows=24, nrows=1)

    plot_data("HDF5", data_frame_1, False)
    plot_data("HDF5", data_frame_2, True)

    plot_data("NetCDF", data_frame_3, False)
    plot_data("NetCDF", data_frame_4, True)

    plot_data("Zarr", data_frame_5, False)
    plot_data("Zarr", data_frame_6, True)
