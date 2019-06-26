import os
from collections import deque

def tail(fname, window):
    #end-relative seek only works in binary mode
    with open(fname, 'rb') as f:
            BUFSIZ = 1024
            CR = b'\n'
            data = b''
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            pos = -1
            exit = False
            while not exit:
                offset = (pos * BUFSIZ)                
                if (fsize + offset) <= 0:
                    f.seek(0)
                    newdata = f.read(BUFSIZ - (abs(offset) - fsize))
                    exit = True
                else:
                    f.seek(offset, os.SEEK_END)
                    newdata = f.read(BUFSIZ)
                data = newdata + data
                if data.count(CR) >= window:
                    exit = True
                else:
                    pos -= 1
            return data.splitlines()[-window:]

def tail2(fname, window):
    #end-relative seek only works in binary mode
    with open(fname, 'rb') as f:
            STARTPOS = -1024
            CR = b'\n'
            data = list
            f.seek(0, os.SEEK_END)
            fsize = f.tell()
            exit = False
            while not exit:
                STARTPOS*=2                
                if (fsize + STARTPOS) <= 0:
                    f.seek(0)
                    data = f.read()
                    exit = True
                else:
                    f.seek(STARTPOS, os.SEEK_END)
                    data = f.read(abs(STARTPOS))
                if data.count(CR) >= window:
                    exit = True                
            return data.splitlines()[-window:]            

def tailWithDeque(fname, window):
    q=deque(maxlen=window)
    with open(fname, 'r') as f:
        for line in f.readlines():            
            q.append(line)
    return list(q)   

if __name__ == '__main__':
    print("test")
    print (tailWithDeque("test.log",25))
