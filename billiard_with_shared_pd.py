import numpy as np
import sharedmem
from billiard.pool import Pool
import os
from functools import partial
from pd_share import SharedDataFrame
import pandas as pd
import gc
cpu_count = 16

# process啟動時的callback function
def init():
    pid = os.getpid()
    print(f'[init] pid: {pid}')

# process結束的callback function


def on_exit(pid, exitcode):
    print(f'[on_exit] pid: {pid} , exitcode: {exitcode}')

# 每個process要執行的function


def f(x, shared=None):
    pid = os.getpid()
    print(f'[f] input: {x} pid: {pid}')
    print(f'[f] shared dataframe: {type(shared)}')
    # del shared
    # gc.collect()
    return x ** 2

# 平行處理寫法: 把1~13進行平方

if __name__ == '__main__':
    data = [['Y', 'N', 'N', 'N', 'N', 'N', 'N', 1],
             ['N', 'N', 'N', 'N', 'N', 'Y', 'N', 2],
             ['N', 'N', 'N', 'N', 'N', 'N', 'Y', 2],
             ['N', 'N', 'N', 'N', 'N', 'N', 'N', 3],
             ['Y', 'N', 'N', 'N', 'N', 'Y', 'Y', 1],
             ['N', 'N', 'N', 'N', 'Y', 'N', 'Y', 1]] * 10000
    df = pd.DataFrame(data=data, columns=['travel_card',
                                            'five_profession_card',
                                            'world_card',
                                            'wm_cust',
                                            'gov_employee',
                                            'military_police_firefighters',
                                            'salary_ind',
                                            'output'])
    
    shared_df = SharedDataFrame(df)
    with Pool(cpu_count, initializer=init, on_process_exit=on_exit) as p:
        ans_gen = p.imap(partial(f, shared=shared_df), range(13))
        ans = list(ans_gen)
