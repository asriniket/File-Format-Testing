import os
import random
import shutil
import time

import h5py
import numpy as np
import zarr
from netCDF4 import Dataset


# Creates datasets for the specified file format and populates them. dimensions, and chunks are tuples.
def write(file_format, filename, num_datasets, dimensions, datatype, minimum, maximum, chunk=None):
    if not os.path.exists("Files"):
        os.makedirs("Files")
    if not os.path.exists("Files_Read"):
        os.makedirs("Files_Read")
    is_integer = True if datatype == "i" else False
    data = generate_array(dimensions, is_integer, minimum, maximum)
    dataset_creation_time = 0.0
    dataset_population_time = 0.0
    if chunk == 0:
        chunk = None
    if file_format == "HDF5":
        file = h5py.File("Files/{}.hdf5".format(filename), "w")
        # Create all datasets and populate each one of them.
        for i in range(0, num_datasets):
            t1 = time.time()
            dataset = file.create_dataset("Dataset_{}".format(i), shape=dimensions, dtype=datatype, chunks=chunk)
            t2 = time.time()
            dataset_creation_time += (t2 - t1)

            t3 = time.time()
            if len(dimensions) == 1:
                dataset[:dimensions[0]] = data
            elif len(dimensions) == 2:
                dataset[:dimensions[0], :dimensions[1]] = data
            else:
                dataset[:dimensions[0], :dimensions[1], :dimensions[2]] = data
            t4 = time.time()
            dataset_population_time += (t4 - t3)
        file.close()
    elif file_format == "NetCDF":
        file = Dataset("Files/{}.netc".format(filename), "w", format="NETCDF4")
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
            t1 = time.time()
            dataset = file.createVariable(
                "Dataset_{}".format(i), dimensions=axes, datatype=datatype, chunksizes=chunk)
            t2 = time.time()
            dataset_creation_time += (t2 - t1)

            t3 = time.time()
            if len(dimensions) == 1:
                dataset[:dimensions[0]] = data
            elif len(dimensions) == 2:
                dataset[:dimensions[0], :dimensions[1]] = data
            else:
                dataset[:dimensions[0], :dimensions[1], :dimensions[2]] = data
            t4 = time.time()
            dataset_population_time += (t4 - t3)
        file.close()
    elif file_format == "Zarr":
        file = zarr.open("Files/{}.zarr".format(filename), "w")
        # Create all datasets and populate each one of them.
        for i in range(0, num_datasets):
            t1 = time.time()
            dataset = file.create_dataset("Dataset_{}".format(i), shape=dimensions, dtype=datatype, chunks=chunk)
            t2 = time.time()
            dataset_creation_time += (t2 - t1)

            t3 = time.time()
            if len(dimensions) == 1:
                dataset[:dimensions[0]] = data
            elif len(dimensions) == 2:
                dataset[:dimensions[0], :dimensions[1]] = data
            else:
                dataset[:dimensions[0], :dimensions[1], :dimensions[2]] = data
            t4 = time.time()
            dataset_population_time += (t4 - t3)

    copy_file(file_format, filename)
    # print("Average time taken to create {} datasets: {}".format(num_datasets, dataset_creation_time / num_datasets))
    # print("Dataset Population Time: {}".format(dataset_population_time))

    # arr contains the average time taken to create each dataset along with the average time taken to write to it.
    arr = [dataset_creation_time / num_datasets, dataset_population_time / num_datasets]
    return arr


def generate_array(num_elements, is_integer, minimum, maximum):
    random.seed(time.time())
    if len(num_elements) == 1:
        arr = np.zeros((num_elements[0],))
        for i in range(0, num_elements[0]):
            if is_integer:
                num = random.randint(minimum, maximum)
            else:
                num = random.uniform(minimum, maximum)
            arr[i] = num
    elif len(num_elements) == 2:
        arr = np.zeros((num_elements[0], num_elements[1]))
        for i in range(0, num_elements[0]):
            for j in range(0, num_elements[1]):
                if is_integer:
                    num = random.randint(minimum, maximum)
                else:
                    num = random.uniform(minimum, maximum)
                arr[i, j] = num
    else:
        arr = np.zeros((num_elements[0], num_elements[1], num_elements[2]))
        for i in range(0, num_elements[0]):
            for j in range(0, num_elements[1]):
                for k in range(0, num_elements[2]):
                    if is_integer:
                        num = random.randint(minimum, maximum)
                    else:
                        num = random.uniform(minimum, maximum)
                    arr[i, j, k] = num
    return arr


def copy_file(file_format, filename):
    if file_format == "HDF5":
        if os.path.exists("Files_Read/{}_Copy.hdf5".format(filename)):
            os.remove("Files_Read/{}_Copy.hdf5".format(filename))
        shutil.copy2("Files/{}.hdf5".format(filename), "Files_Read")
        os.rename("Files_Read/{}.hdf5".format(filename), "Files_Read/{}_Copy.hdf5".format(filename))
    elif file_format == "NetCDF":
        if os.path.exists("Files_Read/{}_Copy.netc".format(filename)):
            os.remove("Files_Read/{}_Copy.netc".format(filename))
        shutil.copy2("Files/{}.netc".format(filename), "Files_Read")
        os.rename("Files_Read/{}.netc".format(filename), "Files_Read/{}_Copy.netc".format(filename))
    elif file_format == "Zarr":
        if os.path.exists("Files_Read/{}_Copy.zarr".format(filename)):
            shutil.rmtree("Files_Read/{}_Copy.zarr".format(filename))
        shutil.copytree("Files/{}.zarr".format(filename), "Files_Read/{}.zarr".format(filename))
        os.rename("Files_Read/{}.zarr".format(filename), "Files_Read/{}_Copy.zarr".format(filename))
