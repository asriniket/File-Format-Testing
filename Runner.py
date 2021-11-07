import csv
import os
import shutil

import yaml

import Plot
import Read
import Write


def run(config_name):
    arr_hdf5 = []
    arr_netcdf = []
    arr_zarr = []
    with open("{}.yaml".format(config_name), "r") as file:
        config_file = yaml.safe_load(file)
        filename = config_file.get("FILE_NAME")
        num_datasets = config_file.get("NUMBER_DATASETS")
        dimensions = config_file.get("NUMBER_ELEMENTS")
        minimum = config_file.get("MIN_DATA_VALUE")
        maximum = config_file.get("MAX_DATA_VALUE")
        chunk = config_file.get("CHUNK")

    # Run test, and add it to the results array for storing.
    for i in range(0, num_trials):
        arr_hdf5.extend(Write.write("HDF5", filename, num_datasets, dimensions, "f", minimum, maximum, chunk))
        arr_hdf5.extend(Read.read("HDF5", filename, num_datasets, dimensions))
        arr_netcdf.extend(Write.write("NetCDF", filename, num_datasets, dimensions, "f", minimum, maximum, chunk))
        arr_netcdf.extend(Read.read("NetCDF", filename, num_datasets, dimensions))
        arr_zarr.extend(Write.write("Zarr", filename, num_datasets, dimensions, "f", minimum, maximum, chunk))
        arr_zarr.extend(Read.read("Zarr", filename, num_datasets, dimensions))
        delete_files()

    # Average out results arrays and create CSV.
    arr_hdf5 = split_arr(arr_hdf5)
    arr_netcdf = split_arr(arr_netcdf)
    arr_zarr = split_arr(arr_zarr)
    arr_hdf5.insert(0, "HDF5")
    arr_netcdf.insert(0, "NetCDF")
    arr_zarr.insert(0, "Zarr")
    write_csv(filename, arr_hdf5, arr_netcdf, arr_zarr)
    Plot.plot_data(
        filename, "{} Datasets {}".format(str(num_datasets), str(dimensions)), arr_hdf5, arr_netcdf, arr_zarr)


# Split array into 4 sub arrays with each sub array containing one function (e.g. creation time, write time)
def split_arr(arr):
    arr_creation_time = arr[::4]
    arr_write_time = arr[1::4]
    arr_open_time = arr[2::4]
    arr_read_time = arr[3::4]
    return [arr_creation_time, arr_write_time, arr_open_time, arr_read_time]


def delete_files():
    if os.path.exists("Files"):
        shutil.rmtree("Files")
    if os.path.exists("Files_Read"):
        shutil.rmtree("Files_Read")


def write_csv(filename, hdf5_arr, netcdf_arr, zarr_arr):
    fields = ["File Format",
              "Dataset Creation Time",
              "Dataset Write Time",
              "Dataset Open Time",
              "Dataset Read Time"]
    with open(filename + ".csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fields)
        # Write down each array instead of its average time, just in case any future visualizations need to be made.
        writer.writerow(hdf5_arr)
        writer.writerow(netcdf_arr)
        writer.writerow(zarr_arr)


if __name__ == "__main__":
    num_trials = 3
    # Create configuration file if it does not exist.
    # check = int(input("Would you like a sample configuration file to be generated? Press 1 for yes and 2 for no.\n"))
    # if check == 1:
    #     data = {
    #         "FILE_NAME": "File_Name",
    #         "NUMBER_DATASETS": 0,
    #         "NUMBER_ELEMENTS": [0, 0, 0],
    #         "CHUNK_SIZE": 0,
    #         "MIN_DATA_VALUE": 0,
    #         "MAX_DATA_VALUE": 0,
    #     }
    #     with open("1.yaml", "w") as f:
    #         yaml.safe_dump(data, f, sort_keys=False)
    #
    # config = str(input("Enter the configuration file to be used, excluding the file extension.\n"))
    # run("0")
    run("1")
    run("2")
    run("3")
    run("4")
    run("5")
    run("6")
