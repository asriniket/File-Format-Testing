import random
import time

import numpy as np
import yaml
from netCDF4 import Dataset


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
    config_name = "sample_config"
    with open("{}.yaml".format(config_name), "r") as file:
        config_file = yaml.safe_load(file)
    filename = config_file.get("FILE_NAME")
    num_elements = config_file.get("NUMBER_ELEMENTS")
    chunk_size = config_file.get("CHUNK_SIZE")
    min_value = config_file.get("MIN_DATA_VALUE")
    max_value = config_file.get("MAX_DATA_VALUE")
    num_new_elements = config_file.get("NUMBER_APPEND")

    append_group(num_elements, num_new_elements, min_value, max_value)
