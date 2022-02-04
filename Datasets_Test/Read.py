import time

import h5py
import zarr
from netCDF4 import Dataset


def read(file_format, filename, num_datasets, dimensions):
    dataset_open_time = 0.0
    dataset_read_time = 0.0
    if file_format == "HDF5":
        file = h5py.File(f"Files_Read/{filename}_Copy.hdf5", "r")
    elif file_format == "NetCDF":
        file = Dataset(f"Files_Read/{filename}_Copy.netc", "r")
    else:
        file = zarr.open(f"Files_Read/{filename}_Copy.zarr", "r")
    for i in range(0, num_datasets):
        if file_format == "HDF5":
            t1 = time.perf_counter()
            dataset = file[f"Dataset_{i}"]
            t2 = time.perf_counter()
        elif file_format == "NetCDF":
            t1 = time.perf_counter()
            dataset = file.variables[f"Dataset_{i}"]
            t2 = time.perf_counter()
        else:
            t1 = time.perf_counter()
            dataset = file.get(f"Dataset_{i}")
            t2 = time.perf_counter()
        t3 = time.perf_counter()
        if len(dimensions) == 1:
            print(dataset[:dimensions[0]])
        elif len(dimensions) == 2:
            print(dataset[:dimensions[0], :dimensions[1]])
        else:
            print(dataset[:dimensions[0], :dimensions[1], :dimensions[2]])
        t4 = time.perf_counter()
        dataset_open_time += (t2 - t1)
        dataset_read_time += (t4 - t3)
    if not file_format == "Zarr":
        file.close()
    arr = [1000 * dataset_open_time / num_datasets, 1000 * dataset_read_time / num_datasets]
    return arr
