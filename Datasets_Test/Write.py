import os
import shutil
import time

import h5py
import numpy as np
import zarr
from netCDF4 import Dataset


# Creates datasets for the specified file format and populates them. dimensions is a tuple.
def write(file_format, filename, num_datasets, dimensions):
    if not os.path.exists("Files"):
        os.makedirs("Files")
    if not os.path.exists("Files_Read"):
        os.makedirs("Files_Read")
    dataset_creation_time = 0.0
    dataset_population_time = 0.0
    if file_format == "HDF5":
        file = h5py.File(f"Files/{filename}.hdf5", "w")
    elif file_format == "NetCDF":
        file = Dataset(f"Files/{filename}.netc", "w", format="NETCDF4")
        if len(dimensions) == 1:
            file.createDimension("x", None)
            axes = ("x",)
        elif len(dimensions) == 2:
            file.createDimension("x", None)
            file.createDimension("y", None)
            axes = ("x", "y",)
        else:
            file.createDimension("x", None)
            file.createDimension("y", None)
            file.createDimension("z", None)
            axes = ("x", "y", "z")
    else:
        file = zarr.open(f"Files/{filename}.zarr", "w")
    for i in range(0, num_datasets):
        data = generate_array(dimensions)
        if not file_format == "NetCDF":
            t1 = time.perf_counter()
            dataset = file.create_dataset(f"Dataset_{i}", shape=dimensions, dtype="f")
            t2 = time.perf_counter()
        else:
            t1 = time.perf_counter()
            dataset = file.createVariable(f"Dataset_{i}", dimensions=axes, datatype="f")
            t2 = time.perf_counter()

        t3 = time.perf_counter()
        dataset = data
        t4 = time.perf_counter()
        dataset_creation_time += (t2 - t1)
        dataset_population_time += (t4 - t3)

    if not file_format == "Zarr":
        file.close()
    copy_file(file_format, filename)

    arr = [1000 * dataset_creation_time / num_datasets, 1000 * dataset_population_time / num_datasets]
    return arr


def generate_array(num_elements):
    np.random.seed()
    if len(num_elements) == 1:
        a = num_elements[0]
        arr = np.random.rand(a).astype(np.float32)
    elif len(num_elements) == 2:
        a, b = tuple(num_elements)
        arr = np.random.rand(a, b).astype(np.float32)
    else:
        a, b, c = tuple(num_elements)
        arr = np.random.rand(a, b, c).astype(np.float32)
    return arr


def copy_file(file_format, filename):
    if file_format == "HDF5":
        shutil.copy(f"Files/{filename}.hdf5", "Files_Read")
        os.rename(f"Files_Read/{filename}.hdf5", f"Files_Read/{filename}_Copy.hdf5")
    elif file_format == "NetCDF":
        shutil.copy(f"Files/{filename}.netc", "Files_Read")
        os.rename(f"Files_Read/{filename}.netc", f"Files_Read/{filename}_Copy.netc")
    elif file_format == "Zarr":
        shutil.copytree(f"Files/{filename}.zarr", f"Files_Read/{filename}.zarr")
        os.rename(f"Files_Read/{filename}.zarr", f"Files_Read/{filename}_Copy.zarr")
