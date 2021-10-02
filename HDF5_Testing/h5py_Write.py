import os
import random
import shutil
import time

import h5py
import yaml


# Populates the group with datasets containing randomly generated values.
# Each group has four datasets - 2 integer datasets (chunked and non chunked)
# and 2 float datasets (chunked and non chunked).
# Relies on the write_dataset function to actually populate each dataset with values and measure the elapsed time taken.
# Stores the time taken into a "results.txt" file.
def write_group(element_array, chunk, minimum_value, maximum_value):
    # Create file to use for testing.
    file = h5py.File("Files/{}.hdf5".format(filename), "w")

    # Creating a group based on the number of dimensions specified.
    if len(element_array) == 1:
        group = file.create_group("Vector")
        group_name = "Vector"
        dimensions = (element_array[0],)
        max_shape = (None,)
        chunks = (chunk,)
    elif len(element_array) == 2:
        group = file.create_group("Matrix")
        group_name = "Matrix"
        dimensions = (element_array[0], element_array[1])
        max_shape = (None, None)
        chunks = (chunk, chunk)
    else:
        group = file.create_group("Tensor")
        group_name = "Tensor"
        dimensions = (element_array[0], element_array[1], element_array[2])
        max_shape = (None, None, None)
        chunks = (chunk, chunk, chunk)

    # Creates 4 datasets in the group and measures the time taken.
    t1 = time.time()
    dataset_int = group.create_dataset(
        "Integer_{}".format(group_name), shape=dimensions, maxshape=max_shape, dtype="i")
    dataset_int_chunk = group.create_dataset(
        "Integer_{}_Chunk".format(group_name), shape=dimensions, maxshape=max_shape, dtype="i", chunks=chunks)
    dataset_float = group.create_dataset(
        "Float_{}".format(group_name), shape=dimensions, maxshape=max_shape, dtype="f")
    dataset_float_chunk = group.create_dataset(
        "Float_{}_Chunk".format(group_name), shape=dimensions, maxshape=max_shape, dtype="f", chunks=chunks)
    t2 = time.time()

    # Measure time taken to write data to datasets.
    t_dataset_int = write_dataset(dataset_int, element_array, True, minimum_value, maximum_value)
    t_dataset_int_chunk = write_dataset(dataset_int_chunk, element_array, True, minimum_value, maximum_value)
    t_dataset_float = write_dataset(dataset_float, element_array, False, minimum_value, maximum_value)
    t_dataset_float_chunk = write_dataset(dataset_float_chunk, element_array, False, minimum_value, maximum_value)

    # Write the time taken in a results.txt file.
    results_file = open("{}_HDF5_results.txt".format(filename), "w")
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
    if os.path.exists("Files_Read/{}_Copy.hdf5".format(filename)):
        os.remove("Files_Read/{}_Copy.hdf5".format(filename))
    shutil.copy2("Files/{}.hdf5".format(filename), "Files_Read")
    os.rename("Files_Read/{}.hdf5".format(filename), "Files_Read/{}_Copy.hdf5".format(filename))


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

    # Begin populating each group (group is top-level in HDF5 hierarchy)
    write_group(num_elements, chunk_size, min_value, max_value)

    # Copy file to new directory to begin remaining operations
    copy_file()
