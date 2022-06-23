# Benchmark Operations

This benchmark consists of two main operations, both of which will be discussed below.

## Write Benchmark

The write operation is the first operation to be tested in the benchmark. It creates files with the filename as
specified from the configuration file and extensions `.hdf5` for HDF5 files, `.netc` for netCDF4 files, and `.zarr` for
Zarr files. The file is placed inside a folder named `files/` to help reduce clutter in the working directory.

Taking information from the configuration file, a sample data array is generated with dimensions and length as
specified. Then, the program creates a dataset within the file and writes the sample data array to the dataset. This
process of generating a sample data array, creating a dataset, and populating it with the values from the sample data
array is repeated until the benchmark has created the number of datasets as specified by the configuration file.

After the file is populated with data, the benchmark copies the file to a directory named `files_read/` and renames the
file to avoid any caching effects that may interfere with the read times.

Finally, the time taken to create all the datasets and populate them with data is divided by the number of datasets to
find the average time taken to create and populate one dataset. Both of these times are then returned to the main
program, where they are written to the CSV output file.

## Read Benchmark

The benchmark now opens the copied file in the `files_read/` directory and begins testing the read operations of the
three file formats.

This operation consists of opening each dataset within the file and printing its contents to the standard output. The
time taken to open all the datasets and the time taken to read from all the datasets are once again divided by the
number of datasets within the file out to find the average time taken to open and read one dataset. <br><br> Both of
these times are then returned to the main program, where they are also written to the CSV output file. This process of
running the write operation benchmark and the read operation benchmark are then repeated multiple times in order to
ensure the consistency of the data gathered.

Finally, the data from the CSV file is averaged out with [pandas](https://github.com/pandas-dev/pandas) and plotted
with [matplotlib.pyplot](https://github.com/matplotlib/matplotlib) to show a direct comparison between the file formats
being tested in a given operation.
