# File Format Comparison Benchmark

Scientific data is often stored in files because of the simplicity they provide in managing, transferring, and sharing
data. These files are typically structured in a specific arrangement and contain metadata to understand the structure
the data is stored in. There are numerous file formats in use in various scientific domains that provide abstractions
for storing and retrieving data. With the abundance of file formats aiming to store large amounts of scientific data
quickly and easily,
a question that arises is, "Which scientific file format is best for a general use case?"
In this study, we compiled a set of benchmarks for common file operations, i.e., create, open, read, write, and close,
and used the results of these benchmarks to compare three popular formats: `HDF5`, `netCDF4`, and `Zarr`.

## Benchmark Overview

This benchmark compares the time taken to create a dataset, write data to a dataset, and finally open that dataset at a
later time and read its contents. This can be categorized into two types of operations: the writing operation and the
reading operation.

Additionally, this benchmark uses a configuration-based system in which the user is able to specify the testing
parameters such as the number of datasets to create within the file and the dimensions of the array that will be written
to each dataset by editing a YAML configuration file.

After the benchmark is done, the program then stores the times taken across multiple trials in a CSV file and plots its
data with [matplotlib.pyplot](https://github.com/matplotlib/matplotlib) to allow the user to make a definitive
comparison between the file formats being tested.

## How to Run

1. Install the requirements found in the `requirements.txt` file.
2. Run the `runner.py` file. If no configuration files are found in the `datasets_test/configuration_files/` directory,
   a configuration file will be generated. Otherwise, the benchmark will be run with all `.yaml` configuration files
   found in the directory. The benchmark will test each file format 5 times, but this can be
   modified by changing the `num_trials` variable in the `runner.py` file.

Note: Both the CSV files and the Plots can be found under the generated `datasets_test/data/` folder after the benchmark
is
run.
