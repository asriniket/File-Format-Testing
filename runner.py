import csv
import glob
import os

import yaml

from datasets_test import plot, read, write


def run_benchmark(config_file):
    with open(f'{config_file}', 'r') as file:
        config = yaml.safe_load(file)
        filename = config.get('FILE_NAME')
        num_datasets = config.get('NUMBER_DATASETS')
        dimensions = config.get('NUMBER_ELEMENTS')

    for file_format in file_formats:
        # Create a CSV file to store the data for a given file format
        csvfile = open(f'datasets_test/data/{file_format}_{num_datasets}_{dimensions}.csv', 'w')
        writer = csv.writer(csvfile)
        writer.writerow([file_format, 'Dataset Creation Time', 'Dataset Write Time', 'Dataset Open Time',
                         'Dataset Read Time'])

        # Run write and read benchmarks and write the times taken to the CSV file
        for i in range(num_trials):
            results_write = write.write(file_format, filename, num_datasets, dimensions)
            results_read = read.read(file_format, filename, num_datasets, dimensions)
            writer.writerow([f'Trial {i + 1}', results_write[0], results_write[1], results_read[0], results_read[1]])
        csvfile.close()
    plot.plot(file_formats, num_datasets, dimensions)


def main():
    # Run the datasets test for all .yaml configuration files found in the configuration_files directory.
    # Make a sample configuration file and exit if datasets_test/configuration_files/ is empty.
    directories_create = [directory for directory in directories if not os.path.exists(f'datasets_test/{directory}')]
    for directory in directories_create:
        os.mkdir(f'datasets_test/{directory}')

    config_files = glob.glob('datasets_test/configuration_files/*.yaml')
    if not config_files:
        data = {
            'FILE_NAME': 'File_Name',
            'NUMBER_DATASETS': 0,
            'NUMBER_ELEMENTS': [0, 0, 0]  # Create dataset with dimensions provided by 'NUMBER_ELEMENTS'
        }
        with open('datasets_test/configuration_files/sample_configuration.yaml', 'w') as file:
            yaml.safe_dump(data, file, sort_keys=False)
        print('A sample configuration file has been placed in the directory: datasets_test/configuration_files/')
        exit(0)

    for config_file in config_files:
        run_benchmark(config_file)


if __name__ == '__main__':
    directories = ['configuration_files', 'data', 'files', 'files_read']
    file_formats = ['HDF5', 'netCDF4', 'Zarr']
    num_trials = 5  # Must be greater than 1
    main()
