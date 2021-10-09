import time

import h5py
import yaml


# Prints out all values in the group and returns the time taken to do so. Relies on the read_dataset function.
def read_group(elements_array):
    file_read = h5py.File("Files_Read/{}_Copy.hdf5".format(filename), "r")
    results_file = open("{}_HDF5_results.txt".format(filename), "a")
    if len(elements_array) == 1:
        group_name = "Vector"
    elif len(elements_array) == 2:
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
    results_file.write("\nTime taken to Open all 4 datasets: %f seconds.\n\n" % (t2 - t1))

    # Measure time taken to read data from datasets and record it in results file.
    read_dataset(dataset_int, elements_array, results_file)
    read_dataset(dataset_int_chunk, elements_array, results_file)
    read_dataset(dataset_float, elements_array, results_file)
    read_dataset(dataset_float_chunk, elements_array, results_file)

    results_file.close()
    file_read.close()


# Print array at once
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


def write_file(dataset, operation, time_elapsed, results_file):
    dataset_name = dataset.name
    dataset_type = dataset_name[dataset_name.index("/", 1) + 1:]
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

    read_group(num_elements)
