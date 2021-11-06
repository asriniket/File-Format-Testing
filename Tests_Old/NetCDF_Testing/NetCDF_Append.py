import random
import time

import numpy as np
import yaml
from netCDF4 import Dataset


# Appends a dataset of the same size to each dataset within the group.
def append_group(elements_array, append_array, minimum_value, maximum_value):
    file_read = Dataset("Files_Read/{}_Copy.netc".format(filename), "a")
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")
    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
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
    results_file.write("\nTime taken to Open {} datasets: %f seconds.\n\n".format(group_name) % (t2 - t1))

    # Measure time taken to append data to datasets and record it.
    append_dataset(dataset_int, elements_array, append_array, True, minimum_value, maximum_value, results_file)
    append_dataset(dataset_int_chunk, elements_array, append_array, True, minimum_value, maximum_value, results_file)
    append_dataset(dataset_float, elements_array, append_array, False, minimum_value, maximum_value, results_file)
    append_dataset(dataset_float_chunk, elements_array, append_array, False, minimum_value, maximum_value, results_file)

    results_file.close()
    file_read.close()


def append_dataset(dataset, elements_array, append_array, is_integer, minimum, maximum, results_file):
    random.seed(time.time())
    if len(append_array) == 1:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t3 = time.time()
        dataset[elements_array[0]:] = arr[:append_array[0]]
        t4 = time.time()

    elif len(append_array) == 2:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t3 = time.time()
        dataset[elements_array[0]:, elements_array[1]:] = arr[:append_array[0], :append_array[1]]
        t4 = time.time()

    else:
        arr = generate_array(dataset, append_array, is_integer, minimum, maximum, results_file)

        t3 = time.time()
        dataset[elements_array[0]:, elements_array[1]:, elements_array[2]:] \
            = arr[:append_array[0], :append_array[1], :append_array[2]]
        t4 = time.time()

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
    dataset_type = dataset.name
    results_file.write("Time taken to {} the {} dataset: %f seconds.\n".format(operation, dataset_type) % time_elapsed)


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
