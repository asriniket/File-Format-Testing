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
        file = h5py.File("Files/{}.hdf5".format(filename), "w")
        # Create all datasets and populate each one of them.
        for i in range(0, num_datasets):
            data = generate_array(dimensions)
            t1 = time.perf_counter()
            dataset = file.create_dataset(
                "Dataset_{}".format(i), shape=dimensions, dtype="f")
            t2 = time.perf_counter()
            dataset_creation_time += (t2 - t1)

            t3 = time.perf_counter()
            dataset = data
            t4 = time.perf_counter()
            dataset_population_time += (t4 - t3)
        file.close()
    elif file_format == "NetCDF":
        file = Dataset("Files/{}.netc".format(filename), "w", format="NETCDF4")
        # Variable (dataset) dimensions must be specified before creating them.
        # None means that the specified dimension has infinite length.
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
        # Create all datasets and populate each one of them.
        for i in range(0, num_datasets):
            data = generate_array(dimensions)
            t1 = time.perf_counter()
            dataset = file.createVariable(
                "Dataset_{}".format(i), dimensions=axes, datatype="f")
            t2 = time.perf_counter()
            dataset_creation_time += (t2 - t1)

            t3 = time.perf_counter()
            dataset = data
            t4 = time.perf_counter()
            dataset_population_time += (t4 - t3)
        file.close()
    elif file_format == "Zarr":
        file = zarr.open("Files/{}.zarr".format(filename), "w")
        # Create all datasets and populate each one of them.
        for i in range(0, num_datasets):
            data = generate_array(dimensions)
            t1 = time.perf_counter()
            dataset = file.create_dataset(
                "Dataset_{}".format(i), shape=dimensions, dtype="f")
            t2 = time.perf_counter()
            dataset_creation_time += (t2 - t1)

            t3 = time.perf_counter()
            dataset = data
            t4 = time.perf_counter()
            dataset_population_time += (t4 - t3)

    # Copy the file to another directory for the read operation.
    copy_file(file_format, filename)

    # Return average time taken to create one dataset along with the average time taken to write to it.
    arr = [dataset_creation_time / num_datasets,
           dataset_population_time / num_datasets]
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
        if os.path.exists("Files_Read/{}_Copy.hdf5".format(filename)):
            os.remove("Files_Read/{}_Copy.hdf5".format(filename))
        shutil.copy2("Files/{}.hdf5".format(filename), "Files_Read")
        os.rename("Files_Read/{}.hdf5".format(filename),
                  "Files_Read/{}_Copy.hdf5".format(filename))
    elif file_format == "NetCDF":
        if os.path.exists("Files_Read/{}_Copy.netc".format(filename)):
            os.remove("Files_Read/{}_Copy.netc".format(filename))
        shutil.copy2("Files/{}.netc".format(filename), "Files_Read")
        os.rename("Files_Read/{}.netc".format(filename),
                  "Files_Read/{}_Copy.netc".format(filename))
    elif file_format == "Zarr":
        if os.path.exists("Files_Read/{}_Copy.zarr".format(filename)):
            shutil.rmtree("Files_Read/{}_Copy.zarr".format(filename))
        shutil.copytree("Files/{}.zarr".format(filename),
                        "Files_Read/{}.zarr".format(filename))
        os.rename("Files_Read/{}.zarr".format(filename),
                  "Files_Read/{}_Copy.zarr".format(filename))
