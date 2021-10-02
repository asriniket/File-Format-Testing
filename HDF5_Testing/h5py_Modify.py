import time

import h5py
import yaml


# Modifies specified elements in each dataset in the group.
# "first_half" modifies the first half of each dataset,
# "second_half" modifies the second half of each dataset, and
# if neither first half nor first half is True, the function modifies alternating elements of each dataset.
def modify_group(element_array, first_half=False, second_half=False):
    file_read = h5py.File("Files_Read/{}_Copy.hdf5".format(filename), "a")
    if len(element_array) == 1:
        group_name = "Vector"
    elif len(element_array) == 2:
        group_name = "Matrix"
    else:
        group_name = "Tensor"

    # Opens all 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = file_read.get(group_name)["Integer_{}".format(group_name)]
    dataset_int_chunk = file_read.get(group_name)["Integer_{}_Chunk".format(group_name)]
    dataset_float = file_read.get(group_name)["Float_{}".format(group_name)]
    dataset_float_chunk = file_read.get(group_name)["Float_{}_Chunk".format(group_name)]
    t2 = time.time()

    # Measure time taken to modify data from datasets.
    t_dataset_int = modify_dataset(dataset_int, element_array, first_half, second_half)
    t_dataset_int_chunk = modify_dataset(dataset_int_chunk, element_array, first_half, second_half)
    t_dataset_float = modify_dataset(dataset_float, element_array, first_half, second_half)
    t_dataset_float_chunk = modify_dataset(dataset_float_chunk, element_array, first_half, second_half)

    # Write the time taken in a results.txt file.
    results_file = open("{}_HDF5_results.txt".format(filename), "a")
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


if __name__ == "__main__":
    config_name = "sample_config"
    with open("{}.yaml".format(config_name), "r") as file:
        config_file = yaml.safe_load(file)
    filename = config_file.get("FILE_NAME")
    num_elements = config_file.get("NUMBER_ELEMENTS")
    chunk_size = config_file.get("CHUNK_SIZE")
    min_value = config_file.get("MIN_DATA_VALUE")
    max_value = config_file.get("MAX_DATA_VALUE")
    first_half_modify = config_file.get("MODIFY_FIRST_HALF")
    second_half_modify = config_file.get("MODIFY_SECOND_HALF")

    modify_group(num_elements, first_half_modify, second_half_modify)
