import time
import numpy as np
def resetcurrentdatapoints(hash1):
    members = []

    for k,v in hash1.items():
        if((time.time() - float(v[0])) > 10):
            del hash1[k]
    for i in hash1:
        members.append(hash1[i])
    return members
def resetV(v_current):
    mem = []
    for i in range(1, len(v_current)):
        if((time.time() - v_current[i][0]>5)):
            print('Being Popped:' , v_current[i], 'At Time :' , (time.time()-v_current[i][0]))
            mem.append(i)
    for ii in range(len(mem)):
        del v_current[mem[ii]]
    return v_current
