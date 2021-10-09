import random
import time

import numpy as np
import yaml
from netCDF4 import Dataset


# Modifies specified elements in each dataset in the group.
# "first_half" modifies the first half of each dataset,
# "second_half" modifies the second half of each dataset, and
# if neither first half nor first half is True, the function modifies alternating elements of each dataset.
def modify_group(elements_array, minimum, maximum, first_half=False, second_half=False):
    file_read = Dataset("Files_Read/{}_Copy.netc".format(filename), "a")
    results_file = open("{}_NetCDF_results.txt".format(filename), "a")

    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
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
    results_file.write("\nTime taken to Open all 4 datasets: %f seconds.\n\n" % (t2 - t1))

    # Modify datasets and record time taken to do so.
    modify_dataset(dataset_int, elements_array, True, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_int_chunk, elements_array, True, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_float, elements_array, False, first_half, second_half, results_file, minimum, maximum)
    modify_dataset(dataset_float_chunk, elements_array, False, first_half, second_half, results_file, minimum, maximum)

    results_file.close()
    file_read.close()


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
    first_half_modify = config_file.get("MODIFY_FIRST_HALF")
    second_half_modify = config_file.get("MODIFY_SECOND_HALF")

    modify_group(num_elements, first_half_modify, second_half_modify)
