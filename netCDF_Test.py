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

    # Creating a group based on the number of dimensions specified.
    # Since you can not resize a NetCDF dimension after initialization, make the dimension with the append array size.
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

    # Measure time taken to write data to datasets.
    t_dataset_int = write_dataset(dataset_int, element_array, True, minimum_value, maximum_value)
    t_dataset_int_chunk = write_dataset(dataset_int_chunk, element_array, True, minimum_value, maximum_value)
    t_dataset_float = write_dataset(dataset_float, element_array, False, minimum_value, maximum_value)
    t_dataset_float_chunk = write_dataset(dataset_float_chunk, element_array, False, minimum_value, maximum_value)

    # Write the time taken in a results.txt file.
    results_file = open("{}_NetCDF_results.txt".format(filename), "w")
    results_file.write(
        "Time taken to create {} datasets: %f seconds. \n".format(group_name)
        % (t2 - t1))
    results_file.write(
        "Time taken to populate the Integer {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int)
    results_file.write(
        "Time taken to populate the Integer Chunked {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int_chunk)
    results_file.write(
        "Time taken to populate the Float {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_float)
    results_file.write(
        "Time taken to populate the Float Chunked {} dataset: %f seconds. \n\n".format(group_name)
        % t_dataset_float_chunk)
    results_file.close()
    file.close()


def write_dataset(dataset, elements_array, is_integer, minimum, maximum):
    t1 = time.time()
    random.seed(t1)
    if len(elements_array) == 1:
        for i in range(0, elements_array[0]):
            random_int = random.randint(minimum, maximum)
            random_float = random.uniform(minimum, maximum)
            dataset[i] = random_int if is_integer else random_float
    elif len(elements_array) == 2:
        for i in range(0, elements_array[0]):
            for j in range(0, elements_array[1]):
                random_int = random.randint(minimum, maximum)
                random_float = random.uniform(minimum, maximum)
                dataset[i, j] = random_int if is_integer else random_float
    else:
        for i in range(0, elements_array[0]):
            for j in range(0, elements_array[1]):
                for k in range(0, elements_array[2]):
                    random_int = random.randint(minimum, maximum)
                    random_float = random.uniform(minimum, maximum)
                    dataset[i, j, k] = random_int if is_integer else random_float
    t2 = time.time()
    return t2 - t1


def copy_file():
    if os.path.exists("Files_Read/{}_Copy.netc".format(filename)):
        os.remove("Files_Read/{}_Copy.netc".format(filename))
    shutil.copy2("Files/{}.netc".format(filename), "Files_Read")
    os.rename("Files_Read/{}.netc".format(filename), "Files_Read/{}_Copy.netc".format(filename))


# Prints out all values in the group and returns the time taken to do so. Relies on the read_dataset function.
def read_group(element_array):
    file_read = Dataset("Files_Read/{}_Copy.netc".format(filename), "r")
    if len(element_array) == 1:
        group_name = "Vector"
    elif len(element_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Opens all 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.groups[group_name].variables["Integer_{}".format(group_name)]
    dataset_int_chunk = file_read.groups[group_name].variables["Integer_{}_Chunk".format(group_name)]
    dataset_float = file_read.groups[group_name].variables["Float_{}".format(group_name)]
    dataset_float_chunk = file_read.groups[group_name].variables["Float_{}_Chunk".format(group_name)]
    t2 = time.time()

    # Measure time taken to read data from datasets.
    t_dataset_int = read_dataset(dataset_int, element_array)
    t_dataset_int_chunk = read_dataset(dataset_int_chunk, element_array)
    t_dataset_float = read_dataset(dataset_float, element_array)
    t_dataset_float_chunk = read_dataset(dataset_float_chunk, element_array)

    # Write the time taken in a results.txt file.
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")
    results_file.write(
        "Time taken to access {} datasets: %f seconds. \n".format(group_name)
        % (t2 - t1))
    results_file.write(
        "Time taken to read the Integer {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int)
    results_file.write(
        "Time taken to read the Integer Chunked {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int_chunk)
    results_file.write(
        "Time taken to read the Float {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_float)
    results_file.write(
        "Time taken to read the Float Chunked {} dataset: %f seconds. \n\n".format(group_name)
        % t_dataset_float_chunk)
    results_file.close()
    file_read.close()


def read_dataset(dataset, element_array):
    t1 = time.time()
    if len(element_array) == 1:
        for i in range(0, element_array[0]):
            print(dataset[i])
    elif len(element_array) == 2:
        for i in range(0, element_array[0]):
            for j in range(0, element_array[1]):
                print(dataset[i, j])
    else:
        for i in range(0, element_array[0]):
            for j in range(0, element_array[1]):
                for k in range(0, element_array[2]):
                    print(dataset[i, j, k])
    t2 = time.time()
    return t2 - t1


# Modifies specified elements in each dataset in the group.
# "first_half" modifies the first half of each dataset,
# "second_half" modifies the second half of each dataset, and
# if neither first half nor first half is True, the function modifies alternating elements of each dataset.
def modify_group(element_array, first_half=False, second_half=False):
    file_read = Dataset("Files_Read/{}_Copy.netc".format(filename), "a")
    if len(element_array) == 1:
        group_name = "Vector"
    elif len(element_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Opens all 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.groups[group_name].variables["Integer_{}".format(group_name)]
    dataset_int_chunk = file_read.groups[group_name].variables["Integer_{}_Chunk".format(group_name)]
    dataset_float = file_read.groups[group_name].variables["Float_{}".format(group_name)]
    dataset_float_chunk = file_read.groups[group_name].variables["Float_{}_Chunk".format(group_name)]
    t2 = time.time()

    # Measure time taken to modify data from datasets.
    t_dataset_int = modify_dataset(dataset_int, element_array, first_half, second_half)
    t_dataset_int_chunk = modify_dataset(dataset_int_chunk, element_array, first_half, second_half)
    t_dataset_float = modify_dataset(dataset_float, element_array, first_half, second_half)
    t_dataset_float_chunk = modify_dataset(dataset_float_chunk, element_array, first_half, second_half)

    # Write the time taken in a results.txt file.
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")
    results_file.write(
        "Time taken to access {} datasets: %f seconds. \n".format(group_name)
        % (t2 - t1))
    results_file.write(
        "Time taken to modify the Integer {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int)
    results_file.write(
        "Time taken to modify the Integer Chunked {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int_chunk)
    results_file.write(
        "Time taken to modify the Float {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_float)
    results_file.write(
        "Time taken to modify the Float Chunked {} dataset: %f seconds. \n\n".format(group_name)
        % t_dataset_float_chunk)
    results_file.close()
    file_read.close()


def modify_dataset(dataset, element_array, first_half, second_half):
    t1 = time.time()
    if len(element_array) == 1:
        if first_half:
            for i in range(0, int(element_array[0] / 2)):
                dataset[i] *= 2
        elif second_half:
            for i in range(int(element_array[0] / 2), element_array[0]):
                dataset[i] *= 2
        else:
            for i in range(0, element_array[0]):
                if i % 2 == 0:
                    dataset[i] *= 2
    elif len(element_array) == 2:
        if first_half:
            for i in range(0, int(element_array[0] / 2)):
                for j in range(0, int(element_array[1] / 2)):
                    dataset[i, j] *= 2
        elif second_half:
            for i in range(int(element_array[0] / 2), int(element_array[0])):
                for j in range(int(element_array[1] / 2), int(element_array[1])):
                    dataset[i, j] *= 2
        else:
            for i in range(0, element_array[0]):
                for j in range(0, element_array[1]):
                    if j % 2 == 0:
                        dataset[i, j] *= 2
    else:
        if first_half:
            for i in range(0, int(element_array[0] / 2)):
                for j in range(0, int(element_array[1] / 2)):
                    for k in range(0, int(element_array[2] / 2)):
                        dataset[i, j, k] *= 2
        elif second_half:
            for i in range(int(element_array[0] / 2), element_array[0]):
                for j in range(int(element_array[1] / 2), element_array[1]):
                    for k in range(int(element_array[2] / 2), element_array[2]):
                        dataset[i, j, k] *= 2
        else:
            for i in range(0, element_array[0]):
                for j in range(0, element_array[1]):
                    for k in range(0, element_array[2]):
                        if k % 2 == 0:
                            dataset[i, j, k] *= 2
    t2 = time.time()
    return t2 - t1


# Appends a dataset of the same size to each dataset within the group.
def append_group(element_array, append_array, minimum_value, maximum_value):
    file_read = Dataset("Files_Read/{}_Copy.netc".format(filename), "a")
    if len(element_array) == 1:
        group_name = "Vector"
    elif len(element_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Open 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.groups[group_name].variables["Integer_{}".format(group_name)]
    dataset_int_chunk = file_read.groups[group_name].variables["Integer_{}_Chunk".format(group_name)]
    dataset_float = file_read.groups[group_name].variables["Float_{}".format(group_name)]
    dataset_float_chunk = file_read.groups[group_name].variables["Float_{}_Chunk".format(group_name)]
    t2 = time.time()

    # Measure time taken to append data to datasets.
    t_dataset_int = append_dataset(
        dataset_int, element_array, append_array, True, minimum_value, maximum_value)
    t_dataset_int_chunk = append_dataset(
        dataset_int_chunk, element_array, append_array, True, minimum_value, maximum_value)
    t_dataset_float = append_dataset(
        dataset_float, element_array, append_array, False, minimum_value, maximum_value)
    t_dataset_float_chunk = append_dataset(
        dataset_float_chunk, element_array, append_array, False, minimum_value, maximum_value)

    # Write the time taken in a results.txt file.
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")

    results_file.write(
        "Time taken to open {} datasets: %f seconds. \n".format(group_name)
        % (t2 - t1))

    results_file.write(
        "Time taken to append to the Integer {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int)

    results_file.write(
        "Time taken to append to the Integer Chunked {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_int_chunk)

    results_file.write(
        "Time taken to append to the Float {} dataset: %f seconds. \n".format(group_name)
        % t_dataset_float)

    results_file.write(
        "Time taken to append to the Float Chunked {} dataset: %f seconds. \n\n".format(group_name)
        % t_dataset_float_chunk)

    results_file.close()
    file_read.close()


def append_dataset(dataset, element_array, append_array, is_integer, minimum, maximum):
    random.seed(time.time())
    if len(append_array) == 1:
        temp = np.zeros((append_array[0],))
        if is_integer:
            for i in range(0, append_array[0]):
                random_int = random.randint(minimum, maximum)
                temp[i] = random_int
        else:
            for i in range(0, append_array[0]):
                random_float = random.uniform(minimum, maximum)
                temp[i] = random_float

        t1 = time.time()
        dataset[element_array[0]:] = temp[:append_array[0]]
        t2 = time.time()

    elif len(append_array) == 2:
        temp = np.zeros((append_array[0], append_array[1]))
        if is_integer:
            for i in range(0, append_array[0]):
                for j in range(0, append_array[1]):
                    random_int = random.randint(minimum, maximum)
                    temp[i, j] = random_int
        else:
            for i in range(0, append_array[0]):
                for j in range(0, append_array[1]):
                    random_float = random.uniform(minimum, maximum)
                    temp[i, j] = random_float

        t1 = time.time()
        dataset[element_array[0]:, element_array[1]:] = temp[:append_array[0], :append_array[1]]
        t2 = time.time()

    else:
        temp = np.zeros((append_array[0], append_array[1], append_array[2]))
        if is_integer:
            for i in range(0, append_array[0]):
                for j in range(0, append_array[1]):
                    for k in range(0, append_array[2]):
                        random_int = random.randint(minimum, maximum)
                        temp[i, j, k] = random_int
        else:
            for i in range(0, append_array[0]):
                for j in range(0, append_array[1]):
                    for k in range(0, append_array[2]):
                        random_float = random.uniform(minimum, maximum)
                        temp[i, j, k] = random_float

        t1 = time.time()
        dataset[element_array[0]:, element_array[1]:, element_array[2]:] \
            = temp[:append_array[0], :append_array[1], :append_array[2]]
        t2 = time.time()

    return t2 - t1


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
        with open("sample_config.yaml", "w") as f:
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
    first_half_modify = config_file.get("MODIFY_FIRST_HALF")
    second_half_modify = config_file.get("MODIFY_SECOND_HALF")

    # Begin populating each group (group is top-level in HDF5 hierarchy)
    write_group(num_elements, num_append, chunk_size, min_value, max_value)

    # Copy file to new directory to begin remaining operations
    copy_file()

    # Read all elements in the file
    read_group(num_elements)

    # Modify half of the elements in the file.
    modify_group(num_elements, first_half_modify, second_half_modify)

    # Append an array of data to each dataset.
    append_group(num_elements, num_append, min_value, max_value)
