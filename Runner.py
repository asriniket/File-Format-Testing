import csv
import os
import re

import NetCDF_Test
import Zarr_Test
import h5py_Test

create_arr = []
write_arr = []
read_arr = []
access_arr = []
modify_arr = []
resize_arr = []
append_arr = []


# Run tests based on file format for the specified number of trials.
def run_tests(file_name, file_format, config, num_trials):
    if file_format == "HDF5":
        for i in range(0, num_trials):
            h5py_Test.begin_test(config)
            populate_array("{}_HDF5_results".format(file_name))
    elif file_format == "NetCDF":
        for i in range(0, num_trials):
            NetCDF_Test.begin_test(config)
            populate_array("{}_NetCDF_results".format(file_name))
    else:
        for i in range(0, num_trials):
            Zarr_Test.begin_test(config)
            populate_array("{}_Zarr_results".format(file_name))


# For each of the arrays listed, parse the text file to get the time it takes.
def populate_array(name):
    create_arr.append(txt_parser(name, "Create"))
    write_arr.append(txt_parser(name, "Write"))
    read_arr.append(txt_parser(name, "Read"))
    access_arr.append(txt_parser(name, "Open"))
    modify_arr.append(txt_parser(name, "Modify"))
    resize_arr.append(txt_parser(name, "Resize"))
    append_arr.append(txt_parser(name, "Append"))


# Analyze data from results.txt and populate it in its respective array.
def txt_parser(txt_file, operation):
    arr = []
    with open(txt_file + ".txt", "r") as txt:
        for lines in txt:
            # If the line starts with the operation requested, add it to the array.
            if operation in lines:
                # Append the float portion of the line.
                arr.append(float(re.findall(r"\d+\.\d+", lines)[0]))
    return arr


# Takes average values of the array and writes it to the CSV File. Clears array for later use.
def write_data(file_format, filename):
    create = average_array(create_arr)
    write = average_array(write_arr)
    read = average_array(read_arr)
    access = average_array(access_arr)
    modify = average_array(modify_arr)
    resize = average_array(resize_arr)
    append = average_array(append_arr)
    write_csv(file_format, filename, create, write, read, access, modify, resize, append)
    create_arr.clear()
    write_arr.clear()
    read_arr.clear()
    access_arr.clear()
    modify_arr.clear()
    resize_arr.clear()
    append.clear()


# Average results between trials. Converts the 2D Array of elements into a single 1D elements of the average time taken.
def average_array(arr):
    average_arr = [sum(x) for x in zip(*arr)]
    for i in range(0, len(average_arr)):
        average_arr[i] = average_arr[i] / len(arr)
    return average_arr


# Writes the averaged data into a CSV file for further processing.
def write_csv(file_format, file_name, create, write, read, access, modify, resize, append):
    fields = [file_format, "Write", "Read", "Overwrite", "Resize", "Append"]
    rows = ["Integer", write[0], read[0], modify[0], resize[0], append[0]], \
           ["Integer (Chunked)", write[1], read[1], modify[1], resize[1], append[1]], \
           ["Float", write[2], read[2], modify[2], resize[2], append[2]], \
           ["Float (Chunked", write[3], read[3], modify[3], resize[3], append[3]],
    with open("{}_results.csv".format(file_name), "a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)
        csv_writer.writerow("\n")
        csv_writer.writerow(["Dataset Creation Time", "Dataset Access Time"])
        csv_writer.writerow([create[0], access[0]])
        csv_writer.writerow("\n")


def runner(filename, config_name, num_trials):
    run_tests(filename, "HDF5", config_name, num_trials)
    write_data("HDF5", filename)

    run_tests(filename, "NetCDF", config_name, num_trials)
    write_data("NetCDF", filename)

    run_tests(filename, "Zarr", config_name, num_trials)
    write_data("Zarr", filename)

    files_in_directory = os.listdir(os.getcwd())
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(os.getcwd(), file)
        os.remove(path_to_file)
