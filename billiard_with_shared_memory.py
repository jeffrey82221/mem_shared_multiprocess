import numpy as np
import sharedmem
from billiard.pool import Pool
import os
from functools import partial

cpu_count = 16

def create_share_mem_array(array):
    fp = sharedmem.empty(array.shape, dtype=array.dtype)
    fp[:] = array[:]
    return fp


# process啟動時的callback function 
def init():
    pid = os.getpid()
    print(f'[init] pid: {pid}')

# process結束的callback function 
def on_exit(pid, exitcode):
    print(f'[on_exit] pid: {pid} , exitcode: {exitcode}')

# 每個process要執行的function
def f(x, shared_array=None):
    pid = os.getpid()
    print(f'[f] input: {x} pid: {pid}')
    print(f'[f] shared array: {shared_array[:]}')
    return x ** 2

# 平行處理寫法: 把1~13進行平方 

array = np.arange(10)
shared_array = create_share_mem_array(array)
print("shared array:", array[:])

with Pool(cpu_count, initializer = init, on_process_exit = on_exit) as p:
    ans_gen = p.imap(partial(f,shared_array=shared_array), range(13))
    ans = list(ans_gen)