import Write
import Read
import Plot
import csv
import os
import shutil

import yaml


def run(file_formats, config_name, num_trials):
    with open("{}.yaml".format(config_name), "r") as file:
        config_file = yaml.safe_load(file)
        filename = config_file.get("FILE_NAME")
        num_datasets = config_file.get("NUMBER_DATASETS")
        dimensions = config_file.get("NUMBER_ELEMENTS")

    for file_format in file_formats:
        csvfile = open(f"Data/{file_format}_{num_datasets}_{dimensions}.csv", "w")
        writer = csv.writer(csvfile)
        writer.writerow([file_format, "Dataset Creation Time", "Dataset Write Time", "Dataset Open Time", "Dataset Read Time"])

        for i in range(0, num_trials):
            results_write = Write.write(file_format, filename, num_datasets, dimensions)
            results_read = Read.read(file_format, filename, num_datasets, dimensions)
            writer.writerow([f"Trial {i + 1}", results_write[0], results_write[1], results_read[0], results_read[1]])
            delete_files()
        csvfile.close()
    Plot.plot(file_formats, num_datasets, dimensions)

def delete_files():
    if os.path.exists("Files"):
        shutil.rmtree("Files")
    if os.path.exists("Files_Read"):
        shutil.rmtree("Files_Read")
    
if __name__ == "__main__":
    delete_files()
    if not os.path.exists("Data"):
        os.mkdir("Data")
    # Create configuration file if it does not exist.
    # check = int(input("Would you like a sample configuration file to be generated? Press 1 for yes and 2 for no.\n"))
    # if check == 1:
    #     data = {
    #         "FILE_NAME": "File_Name",
    #         "NUMBER_DATASETS": 0,
    #         "NUMBER_ELEMENTS": [0, 0, 0],
    #     }
    #     with open("sample_config.yaml", "w") as f:
    #         yaml.safe_dump(data, f, sort_keys=False)
    # config = str(input("Enter the configuration file to be used, excluding the file extension.\n"))
    file_formats = ["HDF5", "NetCDF", "Zarr"]
    run(file_formats, "sample_config", 5)
