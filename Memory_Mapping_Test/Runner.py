import time
import numpy
if __name__ == "__main__":
    t1 = time.perf_counter()
    arr = numpy.random.rand(1000, 1000, 1000)
    t2 = time.perf_counter()
    print(arr[:20, :20, :20])
    print(arr.shape)

    pass
