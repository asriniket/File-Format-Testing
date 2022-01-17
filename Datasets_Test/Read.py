import time

import h5py
import zarr
from netCDF4 import Dataset


# Reads all datasets of a file and measures the average time taken to open each dataset, along with the time to read it.
def read(file_format, filename, num_datasets, dimensions):
    dataset_open_time = 0.0
    dataset_read_time = 0.0
    if file_format == "HDF5":
        file = h5py.File("Files_Read/{}_Copy.hdf5".format(filename), "r")
        for i in range(0, num_datasets):
            t1 = time.perf_counter()
            dataset = file["Dataset_{}".format(i)]
            t2 = time.perf_counter()
            dataset_open_time += (t2 - t1)

            t3 = time.perf_counter()
            if len(dimensions) == 1:
                print(dataset[:dimensions[0]])
            elif len(dimensions) == 2:
                print(dataset[:dimensions[0], :dimensions[1]])
            else:
                print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
            t4 = time.perf_counter()
            dataset_read_time += (t4 - t3)
        file.close()
    elif file_format == "NetCDF":
        file = Dataset("Files_Read/{}_Copy.netc".format(filename), "r")
        for i in range(0, num_datasets):
            t1 = time.perf_counter()
            dataset = file.variables["Dataset_{}".format(i)]
            t2 = time.perf_counter()
            dataset_open_time += (t2 - t1)

            t3 = time.perf_counter()
            if len(dimensions) == 1:
                print(dataset[:dimensions[0]])
            elif len(dimensions) == 2:
                print(dataset[:dimensions[0], :dimensions[1]])
            else:
                print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
            t4 = time.perf_counter()
            dataset_read_time += (t4 - t3)
        file.close()
    elif file_format == "Zarr":
        file = zarr.open("Files_Read/{}_Copy.zarr".format(filename), "r")
        for i in range(0, num_datasets):
            t1 = time.perf_counter()
            dataset = file.get("Dataset_{}".format(i))
            t2 = time.perf_counter()
            dataset_open_time += (t2 - t1)

            t3 = time.perf_counter()
            if len(dimensions) == 1:
                print(dataset[:dimensions[0]])
            elif len(dimensions) == 2:
                print(dataset[:dimensions[0], :dimensions[1]])
            else:
                print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
            t4 = time.perf_counter()
            dataset_read_time += (t4 - t3)

    # arr Return the average time taken to open one dataset along with the average time taken to read from it.
    arr = [dataset_open_time / num_datasets, dataset_read_time / num_datasets]
    return arr
