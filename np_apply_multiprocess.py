"""
Build Multiprocess Apply for Numpy Array

- [X] A target function setting the element of position `i` in an array to value `i`
- [X] The array should be numpy memory map 
- [X] Create multiple child process using fork (debug in .py)
    - [X] parent creating new child 
    - [X] child execute the function 
    - [X] child sys.exit after done 
    - [X] parent record child process id into mmap
- [ ] Develop numpy multicore function apply. 
    - [ ] Split numpy by CPU count rather than creating process for each element. 
    - [ ] convertion of numpy to numpy memmap (check speed) 
    - [ ] Research numpy abritrary function apply along axis. 
    - [ ] Allow inplace numpy transform using this module (numpy to write allow mmap)
    - [ ] Allow numpy to numpy transform using this module (numpy to readonly mmap + empty write allow mmap)
- [ ] Develop pandas multicore function apply 

"""
import os 
import sys 
import psutil
import mmap
import time 
CPU_CNT = os.cpu_count()
def slice_generator(array, cpu_cnt = 1):
    assert cpu_cnt >= 1
    size = int(np.ceil(len(fp)/cpu_cnt))
    i = 0 
    while True:
        try:
            ans = array[i: i + size]
            if len(ans) == size:
                yield ans 
            else:
                raise ValueError('size not enough')
            i += size
        except:
            break
    ans = array[i:]
    if len(ans) > 0:
        yield ans 
    else:
        pass

def multiprocess_map(func, array, **kwargs):
    """
    Apply func to array along the first axis of array. 
    i.e., for i in range(len(array)): array[i] = func(array[i]) 
    
    Args: 
        - func : function to be apply to array[i] 
        - array : a numpy array. 
    
    TODO: 
    - [X] make sure all child is stopped before existing the parent function 
    - [X] Input function, fix args to the function, mem array, and determine process count using array size.  
    - [ ] detemine process count using cpu count 
    - [ ] error handling: 
        - [ ] what if pid is negative? how to handle? 
        - [ ] make sure input is invariate to avoid change to the input when error happended. 
    - [ ] save empty numpy to file 
    - [ ] read as 'c' mode (write read availble on ram but read only on disk) 
    - [ ] remove the file once calculation done. 
    """
    process_cnt = len(mmap_array)
    # pid_records records whether a child is finished. 
    pid_records = mmap.mmap(-1, length=process_cnt, access=mmap.ACCESS_WRITE)
    for i in range(process_cnt):
        pid = os.fork()
        if pid == 0:
            func(array[i], **kwargs)
            pid_records[i] = 1
            sys.exit()
        else:
            pass 
    while pid_records[:] != b'\x01' * process_cnt:
        continue
    return mmap_array

from tempfile import mkdtemp
import mmap
import time
import os
import os.path as path
import numpy as np 

def assign_position(element):
    element += 2
    element[0] = element[1] + element[2]
    element[:] = element[:] + element ** 2
    
if __name__ == '__main__':

    input_a = np.zeros((10,4))
    filename = path.join(mkdtemp(), 'tmp_numpy.dat')
    fp = np.memmap(filename, dtype=input_a.dtype, mode='w+', shape=input_a.shape)
    fp[:] = input_a[:]
    print('Start MultiProcess')
    ans = multiprocess_map(assign_position, fp)
    print('End MultiProcess')
    print(ans)