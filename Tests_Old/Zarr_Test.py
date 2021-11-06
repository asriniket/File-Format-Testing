import os
import random
import shutil
import time

import numpy as np
import yaml
import zarr


def write_group(element_array, chunk, minimum_value, maximum_value):
    # Create file to use for testing.
    results_file = open("{}_Zarr_results.txt".format(filename), "w")
    results_file.close()
    results_file = open("{}_Zarr_results.txt".format(filename), "a")
    # Creating a group based on the number of dimensions specified.
    if len(element_array) == 1:
        group = zarr.open("Files/{}.zarr".format(filename), "w")
        group_name = "Vector"
        dimensions = (element_array[0],)
        chunks = (chunk,)
    elif len(element_array) == 2:
        group = zarr.open("Files/{}.zarr".format(filename), "w")
        group_name = "Matrix"
        dimensions = (element_array[0], element_array[1])
        chunks = (chunk, chunk)
    else:
        group = zarr.open("Files/{}.zarr".format(filename), "w")
        group_name = "Tensor"
        dimensions = (element_array[0], element_array[1], element_array[2])
        chunks = (chunk, chunk, chunk)

    # Creates 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = group.create_dataset(
        "Integer_{}".format(group_name), shape=dimensions, dtype="i")
    dataset_int_chunk = group.create_dataset(
        "Integer_{}_Chunk".format(group_name), shape=dimensions, dtype="i", chunks=chunks)
    dataset_float = group.create_dataset(
        "Float_{}".format(group_name), shape=dimensions, dtype="f")
    dataset_float_chunk = group.create_dataset(
        "Float_{}_Chunk".format(group_name), shape=dimensions, dtype="f", chunks=chunks)
    t2 = time.time()
    results_file.write("Time taken to Create all datasets: %f seconds.\n\n" % (t2 - t1))

    # Measure time taken to write data to datasets and write it to the results file.
    write_dataset(dataset_int, element_array, True, minimum_value, maximum_value, results_file)
    write_dataset(dataset_int_chunk, element_array, True, minimum_value, maximum_value, results_file)
    write_dataset(dataset_float, element_array, False, minimum_value, maximum_value, results_file)
    write_dataset(dataset_float_chunk, element_array, False, minimum_value, maximum_value, results_file)

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


def copy_file():
    if os.path.exists("Files_Read/{}_Copy.zarr".format(filename)):
        shutil.rmtree("Files_Read/{}_Copy.zarr".format(filename))
    shutil.copytree("Files/{}.zarr".format(filename), "Files_Read/{}.zarr".format(filename))
    os.rename("Files_Read/{}.zarr".format(filename), "Files_Read/{}_Copy.zarr".format(filename))


def read_group(elements_array):
    file_read = zarr.open("Files_Read/{}_Copy.zarr".format(filename), "r")
    results_file = open("{}_Zarr_results.txt".format(filename), "a")
    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Opens all 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.get("Integer_{}".format(group_name))
    dataset_int_chunk = file_read.get("Integer_{}_Chunk".format(group_name))
    dataset_float = file_read.get("Float_{}".format(group_name))
    dataset_float_chunk = file_read.get("Float_{}_Chunk".format(group_name))
    t2 = time.time()
    results_file.write("\nTime taken to Open all 4 datasets: %f seconds.\n\n" % (t2 - t1))

    # Measure time taken to read data from datasets and record it in results file.
    read_dataset(dataset_int, elements_array, results_file)
    read_dataset(dataset_int_chunk, elements_array, results_file)
    read_dataset(dataset_float, elements_array, results_file)
    read_dataset(dataset_float_chunk, elements_array, results_file)

    results_file.close()


def read_dataset(dataset, elements_array, results_file):
    t1 = time.time()
    if len(elements_array) == 1:
        print(dataset[:elements_array[0]])
    elif len(elements_array) == 2:
        print(dataset[:elements_array[0], :elements_array[1]])
    else:
        print(dataset[:elements_array[0], :elements_array[1], :elements_array[2]])
    t2 = time.time()
    write_file(dataset, "Read", t2 - t1, results_file)


def modify_group(elements_array, minimum, maximum, first_half=False, second_half=False):
    file_read = zarr.open("Files_Read/{}_Copy.zarr".format(filename), "a")
    results_file = open("{}_Zarr_results.txt".format(filename), "a")

    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Opens all 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.get("Integer_{}".format(group_name))
    dataset_int_chunk = file_read.get("Integer_{}_Chunk".format(group_name))
    dataset_float = file_read.get("Float_{}".format(group_name))
    dataset_float_chunk = file_read.get("Float_{}_Chunk".format(group_name))
    t2 = time.time()
    results_file.write("\nTime taken to Open all 4 datasets: %f seconds.\n\n" % (t2 - t1))

    # Modify datasets and record time taken to do so.
    modify_dataset(dataset_int, elements_array, True, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_int_chunk, elements_array, True, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_float, elements_array, False, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_float_chunk, elements_array, False, first_half, second_half, results_file, minimum, maximum)

    results_file.close()


def modify_dataset(dataset, elements_array, is_integer, first_half, second_half, results_file, minimum, maximum):
    t1 = time.time()
    if len(elements_array) == 1:
        arr = generate_array(dataset, [elements_array[0] // 2], is_integer, minimum, maximum, results_file)
        if first_half:
            dataset[:(elements_array[0] // 2)] = arr[:arr.shape[0]]
        elif second_half:
            dataset[(elements_array[0] // 2):] = arr[:arr.shape[0]]
        else:
            dataset[:elements_array[0]:2] = arr[:arr.shape[0]]
    elif len(elements_array) == 2:
        arr = generate_array(dataset, [elements_array[0] // 2, elements_array[1] // 2], is_integer, minimum, maximum,
                             results_file)
        if first_half:
            dataset[:(elements_array[0] // 2), :(elements_array[1] // 2)] = arr[:arr.shape[0], :arr.shape[1]]
        elif second_half:
            dataset[(elements_array[0] // 2):, (elements_array[1] // 2):] = arr[:arr.shape[0], :arr.shape[1]]
        else:
            dataset[:elements_array[0]:2, :elements_array[1]:2] = arr[:arr.shape[0], :arr.shape[1]]
    else:
        arr = generate_array(dataset, (elements_array[0] // 2, elements_array[1] // 2, elements_array[2] // 2),
                             is_integer, minimum, maximum, results_file)
        if first_half:
            dataset[:(elements_array[0] // 2), :(elements_array[1] // 2), :(elements_array[2] // 2)] \
                = arr[:arr.shape[0], :arr.shape[1], :arr.shape[2]]
        elif second_half:
            dataset[(elements_array[0] // 2):, (elements_array[1] // 2):, (elements_array[2] // 2):] \
                = arr[:arr.shape[0], :arr.shape[1], :arr.shape[2]]
        else:
            dataset[:elements_array[0]:2, :elements_array[1]:2, :elements_array[2]:2] \
                = arr[:arr.shape[0], :arr.shape[1]]
    t2 = time.time()
    write_file(dataset, "Modify", t2 - t1, results_file)


def append_group(elements_array, append_array, minimum_value, maximum_value):
    file_read = zarr.open("Files_Read/{}_Copy.zarr".format(filename), "a")
    results_file = open("{}_Zarr_results.txt".format(filename), "a")
    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Open 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.get("Integer_{}".format(group_name))
    dataset_int_chunk = file_read.get("Integer_{}_Chunk".format(group_name))
    dataset_float = file_read.get("Float_{}".format(group_name))
    dataset_float_chunk = file_read.get("Float_{}_Chunk".format(group_name))
    t2 = time.time()
    results_file.write("\nTime taken to Open {} datasets: %f seconds.\n\n".format(group_name) % (t2 - t1))

    # Measure time taken to append data to datasets and record it.
    append_dataset(dataset_int, elements_array, append_array, True, minimum_value, maximum_value, results_file)
    append_dataset(dataset_int_chunk, elements_array, append_array, True, minimum_value, maximum_value, results_file)
    append_dataset(dataset_float, elements_array, append_array, False, minimum_value, maximum_value, results_file)
    append_dataset(dataset_float_chunk, elements_array, append_array, False, minimum_value, maximum_value, results_file)

    results_file.close()


def append_dataset(dataset, elements_array, append_array, is_integer, minimum, maximum, results_file):
    random.seed(time.time())
    if len(append_array) == 1:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t1 = time.time()
        dataset.resize(((elements_array[0] + append_array[0]),))
        t2 = time.time()  # Time taken to resize the original dataset.

        t3 = time.time()
        dataset[elements_array[0]:] = arr[:append_array[0]]
        t4 = time.time()

    elif len(append_array) == 2:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t1 = time.time()
        dataset.resize(((elements_array[0] + append_array[0]), (elements_array[1] + append_array[1])))
        t2 = time.time()  # Time taken to resize the original dataset.

        t3 = time.time()
        dataset[elements_array[0]:, elements_array[1]:] = arr[:append_array[0], :append_array[1]]
        t4 = time.time()

    else:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t1 = time.time()
        dataset.resize(
            (
                (elements_array[0] + append_array[0]),
                (elements_array[1] + append_array[1]),
                (elements_array[2] + append_array[2])
            )
        )
        t2 = time.time()  # Time taken to resize the original dataset.

        t3 = time.time()
        dataset[elements_array[0]:, elements_array[1]:, elements_array[2]:] \
            = arr[:append_array[0], :append_array[1], :append_array[2]]
        t4 = time.time()

    write_file(dataset, "Resize", t2 - t1, results_file)
    write_file(dataset, "Append", t4 - t3, results_file)


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


def write_file(dataset, operation, time_elapsed, results_file):
    dataset_type = dataset.name[1:]
    results_file.write("Time taken to {} the {} dataset: %f seconds.\n".format(operation, dataset_type) % time_elapsed)


def begin_test(config_name):
    # Make "Files" folder for storing the files. Make "Files_Read" folder for performing read operations.
    if not os.path.exists("Files"):
        os.makedirs("Files")
    if not os.path.exists("Files_Read"):
        os.makedirs("Files_Read")

    # Configuration file creation
    global filename
    with open("{}.yaml".format(config_name), "r") as f:
        config_file = yaml.safe_load(f)

        filename = config_file.get("FILE_NAME")
        num_elements = config_file.get("NUMBER_ELEMENTS")
        chunk_size = config_file.get("CHUNK_SIZE")
        min_value = config_file.get("MIN_DATA_VALUE")
        max_value = config_file.get("MAX_DATA_VALUE")
        first_half_modify = config_file.get("MODIFY_FIRST_HALF")
        second_half_modify = config_file.get("MODIFY_SECOND_HALF")
        num_append = config_file.get("NUMBER_APPEND")

    # Begin populating each group (group is top-level in HDF5 hierarchy)
    write_group(num_elements, chunk_size, min_value, max_value)

    # Copy file to new directory to begin remaining operations
    copy_file()

    # Read all elements in the file
    read_group(num_elements)

    # Modify half of the elements in the file.
    modify_group(num_elements, min_value, max_value, first_half_modify, second_half_modify)

    # Append an array of data to each dataset.
    append_group(num_elements, num_append, min_value, max_value)
