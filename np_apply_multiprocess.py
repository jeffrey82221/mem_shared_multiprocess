"""
Build Multiprocess Apply for Numpy Array

- [X] A target function setting the element of position `i` in an array to value `i`
- [X] The array should be numpy memory map 
- [X] Create multiple child process using fork (debug in .py)
    - [X] parent creating new child 
    - [X] child execute the function 
    - [X] child sys.exit after done 
    - [X] parent record child process id into mmap
- [X] Develop numpy multicore function apply. 
    - [X] Split numpy by CPU count rather than creating process for each element. 
    - [X] convertion of numpy to numpy memmap (check speed) 
    - [X] Research numpy abritrary function apply along axis. 
    - [X] Allow numpy to numpy transform using this module (numpy to readonly mmap + empty write allow mmap)
- [ ] Testing the speed of the numpy apply function 
    - [X] On mac (not faster) 
    - [ ] On AiCloud 
- [ ] Develop pandas multicore function apply 

"""
import gc 
import os 
import sys 
import psutil
import mmap
import time 
from tempfile import mkdtemp
import os.path as path
import numpy as np 
import sharedmem
# https://github.com/rainwoodman/sharedmem

def slice_generator(array, cpu_cnt = 1):
    assert cpu_cnt >= 1
    size = int(np.ceil(len(array)/cpu_cnt))
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
    
def create_share_mem_array(array):
    #filename = path.join(mkdtemp(), 'tmp_numpy.dat')
    #fp = np.memmap(filename, dtype=array.dtype, mode='w+', shape=array.shape)
    fp = sharedmem.empty(array.shape, dtype=array.dtype)

    fp[:] = array[:]
    #fp.flush()
    #del fp 
    #gc.collect()
    #fp = np.memmap(filename, dtype=array.dtype, mode='c', shape=array.shape)
    return fp

def multiprocess_map(func, input_array, **kwargs):
    """
    Apply func to array along the first axis of array. 
    i.e., for i in range(len(array)): array[i] = func(array[i]) 
    
    Args: 
        - func : function to be apply to array[i] 
        - array : a numpy array. 
        
    Notes: 
        - pid_records: records whether a child is finished. 
    
    TODO: 
    - [X] make sure all child is stopped before existing the parent function 
    - [X] Input function, fix args to the function, mem array, and determine process count using array size.  
    - [X] detemine process count using cpu count 
    - [X] error handling: 
        - [X] what if pid is negative? how to handle? 
        - [X] make sure input is invariate to avoid change to the input when error happended. 
    - [X] save empty numpy to file 
    - [X] remove the file once calculation done. 
    """
    array = create_share_mem_array(input_array)
    process_cnt = os.cpu_count()
    pid_records = mmap.mmap(-1, length=process_cnt, access=mmap.ACCESS_WRITE)
    pids = []
    for i, sub_array in enumerate(slice_generator(array, cpu_cnt = process_cnt)):
        pid = os.fork()
        if pid == 0:
            sub_array[:] = np.apply_along_axis(
                func, 1, sub_array, **kwargs)
            pid_records[i] = 1
            os._exit(1)
        elif pid < 0:
            for _pid in pids:
                os.kill(_pid, 9)
            raise ValueError(f'{i}th process creation failed')
        else:
            pids.append(pid)
    while pid_records[:] != b'\x01' * process_cnt:
        continue
    result = np.array(array)
    del array
    gc.collect()
    return result

################################################################################

def assign_position(in_element, plus_number = 1):
    element = in_element.copy()
    element += plus_number
    for i in range(1000):
        element[0] = element[0] + element[1] + element[2]
        element[1] = element[0] + element[2]
    return element

if __name__ == '__main__':

    input_a = np.ones((10,4))
    
    ans_single_cpu = np.apply_along_axis(assign_position, 1, input_a, plus_number = 1)
    print('Single CPU:\n', ans_single_cpu)
    
    input_a = np.ones((10,4))
    
    
    print('MultiProcess:\n')
    ans_multi_cpu = multiprocess_map(assign_position, input_a, plus_number = 1)
    print(ans_multi_cpu)
    
    identical = np.all(ans_multi_cpu == ans_single_cpu)
    assert identical
    print('Identical:', identical)
    
    print('Original:\n')
    print(input_a)