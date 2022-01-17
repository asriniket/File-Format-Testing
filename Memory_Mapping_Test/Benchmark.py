import h5py
import numpy as np

np.random.seed(2016)


def _mmap_h5(path, h5path):
    with h5py.File(path) as f:
        ds = f[h5path]
        # We get the dataset address in the HDF5 fiel.
        offset = ds.id.get_offset()
        # We ensure we have a non-compressed contiguous array.
        assert ds.chunks is None
        assert ds.compression is None
        assert offset > 0
        dtype = ds.dtype
        shape = ds.shape
    arr = np.memmap(path, mode='r', shape=shape, offset=offset, dtype=dtype)
    return arr


shape = (100000, 1000)
n, ncols = shape
arr = np.random.rand(n, ncols).astype(np.float32)
with h5py.File('test.ipynb.h5', 'w') as f:
    f['/test.ipynb'] = arr
f = h5py.File('test.ipynb.h5', 'r')
np.save('test.ipynb.npy', arr)
ind = slice(None, None, 100)
print('in memory')
# %timeit arr[ind, :] * 1
print()
print('h5py')
# %timeit f['/test.ipynb'][ind, :] * 1
print()
print('memmap of HDF5 file')
# %timeit _mmap_h5('test.ipynb.h5', '/test.ipynb')[ind, :] * 1
print()
print('memmap of NPY file')
# %timeit np.load('test.ipynb.npy', mmap_mode='r')[ind, :] * 1
