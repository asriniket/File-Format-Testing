import time

import h5py
import yaml


# Prints out all values in the group and returns the time taken to do so. Relies on the read_dataset function.
def read_group(element_array):
    file_read = h5py.File("Files_Read/{}_Copy.hdf5".format(filename), "r")
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

    # Measure time taken to read data from datasets.
    t_dataset_int = read_dataset(dataset_int, element_array)
    t_dataset_int_chunk = read_dataset(dataset_int_chunk, element_array)
    t_dataset_float = read_dataset(dataset_float, element_array)
    t_dataset_float_chunk = read_dataset(dataset_float_chunk, element_array)

    # Write the time taken in a results.txt file.
    results_file = open("{}_HDF5_results.txt".format(filename), "a")
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


if __name__ == "__main__":
    config_name = "sample_config"
    with open("{}.yaml".format(config_name), "r") as file:
        config_file = yaml.safe_load(file)
    filename = config_file.get("FILE_NAME")
    num_elements = config_file.get("NUMBER_ELEMENTS")
    chunk_size = config_file.get("CHUNK_SIZE")
    min_value = config_file.get("MIN_DATA_VALUE")
    max_value = config_file.get("MAX_DATA_VALUE")

    read_group(num_elements)
