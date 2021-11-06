import os
import random
import shutil
import time

import numpy as np
import yaml
from netCDF4 import Dataset


# Populates the group with datasets containing randomly generated values.
# Each group has four datasets - 2 integer datasets (chunked and non chunked)
# and 2 float datasets (chunked and non chunked).
# Relies on the write_dataset function to actually populate each dataset with values and measure the elapsed time taken.
# Stores the time taken into a "results.txt" file.
def write_group(element_array, append_array, chunk, minimum_value, maximum_value):
    # Create file to use for testing.
    file = Dataset("Files/{}.netc".format(filename), "w", format="NETCDF4")
    results_file = open("{}_NetCDF_results.txt".format(filename), "w")
    results_file.close()
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")
    # Creating a group based on the number of dimensions specified.
    if len(element_array) == 1:
        group = file.createGroup("Vector")
        group_name = "Vector"
        group.createDimension("x", element_array[0] + append_array[0])
        dimensions = ("x",)
        chunks = (chunk,)
    elif len(element_array) == 2:
        group = file.createGroup("Matrix")
        group_name = "Matrix"
        group.createDimension("x", element_array[0] + append_array[0])
        group.createDimension("y", element_array[1] + append_array[1])
        dimensions = ("x", "y",)
        chunks = (chunk, chunk)
    else:
        group = file.createGroup("Tensor")
        group_name = "Tensor"
        group.createDimension("x", element_array[0] + append_array[0])
        group.createDimension("y", element_array[1] + append_array[1])
        group.createDimension("z", element_array[2] + append_array[2])
        dimensions = ("x", "y", "z",)
        chunks = (chunk, chunk, chunk)

    # Creates 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = group.createVariable(
        "Integer_{}".format(group_name), "i", dimensions)
    dataset_int_chunk = group.createVariable(
        "Integer_{}_Chunk".format(group_name), "i", dimensions, chunksizes=chunks)
    dataset_float = group.createVariable(
        "Float_{}".format(group_name), "f", dimensions)
    dataset_float_chunk = group.createVariable(
        "Float_{}_Chunk".format(group_name), "f", dimensions, chunksizes=chunks)
    t2 = time.time()
    results_file.write("Time taken to Create all datasets: %f seconds.\n\n" % (t2 - t1))
    # Measure time taken to write data to datasets and write it to the results file.
    write_dataset(dataset_int, element_array, True, minimum_value, maximum_value, results_file)
    write_dataset(dataset_int_chunk, element_array, True, minimum_value, maximum_value, results_file)
    write_dataset(dataset_float, element_array, False, minimum_value, maximum_value, results_file)
    write_dataset(dataset_float_chunk, element_array, False, minimum_value, maximum_value, results_file)

    file.close()
    results_file.close()


def write_dataset(dataset, elements_array, is_integer, minimum, maximum, results_file):
    if len(elements_array) == 1:
        arr = generate_array(dataset, elements_array, is_integer, minimum, maximum, results_file)
        t1 = time.time()
        random.seed(t1)
        dataset[:elements_array[0]] = arr
    elif len(elements_array) == 2:
        arr = generate_array(dataset, elements_array, is_integer, minimum, maximum, results_file)
        t1 = time.time()
        random.seed(t1)
        dataset[:elements_array[0], :elements_array[1]] = arr
    else:
        arr = generate_array(dataset, elements_array, is_integer, minimum, maximum, results_file)
        t1 = time.time()
        random.seed(t1)
        dataset[:elements_array[0], :elements_array[1], :elements_array[2]] = arr
    t2 = time.time()
    write_file(dataset, "Write", t2 - t1, results_file)


def generate_array(dataset, elements_array, is_integer, minimum, maximum, results_file):
    t1 = time.time()
    random.seed(t1)
    if len(elements_array) == 1:
        arr = np.zeros((elements_array[0],))
        for i in range(0, elements_array[0]):
            if is_integer:
                num = random.randint(minimum, maximum)
            else:
                num = random.uniform(minimum, maximum)
            arr[i] = num
    elif len(elements_array) == 2:
        arr = np.zeros((elements_array[0], elements_array[1]))
        for i in range(0, elements_array[0]):
            for j in range(0, elements_array[1]):
                if is_integer:
                    num = random.randint(minimum, maximum)
                else:
                    num = random.uniform(minimum, maximum)
                arr[i, j] = num
    else:
        arr = np.zeros((elements_array[0], elements_array[1], elements_array[2]))
        for i in range(0, elements_array[0]):
            for j in range(0, elements_array[1]):
                for k in range(0, elements_array[2]):
                    if is_integer:
                        num = random.randint(minimum, maximum)
                    else:
                        num = random.uniform(minimum, maximum)
                    arr[i, j, k] = num
    t2 = time.time()
    write_file(dataset, "Generate the values of", t2 - t1, results_file)
    return arr


def copy_file():
    if os.path.exists("Files_Read/{}_Copy.netc".format(filename)):
        os.remove("Files_Read/{}_Copy.netc".format(filename))
    shutil.copy2("Files/{}.netc".format(filename), "Files_Read")
    os.rename("Files_Read/{}.netc".format(filename), "Files_Read/{}_Copy.netc".format(filename))


def write_file(dataset, operation, time_elapsed, results_file):
    dataset_type = dataset.name
    results_file.write("Time taken to {} the {} dataset: %f seconds.\n".format(operation, dataset_type) % time_elapsed)


if __name__ == "__main__":
    # Make "Files" folder for storing the files. Make "Files_Read" folder for performing read operations.
    if not os.path.exists("Files"):
        os.makedirs("Files")
    if not os.path.exists("Files_Read"):
        os.makedirs("Files_Read")

    # Configuration file creation
    check = int(input("Would you like a sample configuration file to be generated? Press 1 for yes and 2 for no.\n"))
    if check == 1:
        data = {
            "FILE_NAME": "File_Name",
            "NUMBER_ELEMENTS": [0, 0, 0],
            "CHUNK_SIZE": 0,
            "MIN_DATA_VALUE": 0,
            "MAX_DATA_VALUE": 0,
            "NUMBER_APPEND": [0, 0, 0],
            "MODIFY_FIRST_HALF": True,
            "MODIFY_SECOND_HALF": False
        }
        with open("1.yaml", "w") as f:
            yaml.safe_dump(data, f, sort_keys=False)

    config_name = str(
        input("Enter the name of the configuration file to use (Don't include the file extension).\n"))
    with open("{}.yaml".format(config_name), "r") as f:
        config_file = yaml.safe_load(f)
    filename = config_file.get("FILE_NAME")
    num_elements = config_file.get("NUMBER_ELEMENTS")
    chunk_size = config_file.get("CHUNK_SIZE")
    min_value = config_file.get("MIN_DATA_VALUE")
    max_value = config_file.get("MAX_DATA_VALUE")
    num_append = config_file.get("NUMBER_APPEND")

    # Begin populating each group (group is top-level in HDF5 hierarchy)
    write_group(num_elements, num_append, chunk_size, min_value, max_value)

    # Copy file to new directory to begin remaining operations
    copy_file()
