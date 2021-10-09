import mmap
import time
import os
def sharing_without_mmap():
    BUF = 'oooooooooo'
    pid = os.fork()
    if pid == 0:
        # Child process
        BUF += "a" * 10
        print('In child:', BUF)
    else:
        time.sleep(2)
        print('In parent', BUF)
        
sharing_without_mmap()