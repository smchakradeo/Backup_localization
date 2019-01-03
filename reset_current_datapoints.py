import time
import numpy as np
def resetcurrentdatapoints(hash1):
    #members = []
    mem_del = []
    for k,v in hash1.items():
        if((time.time() - float(v[0])) < 3):
            #print('deleted: ', hash1[k], 'time: ', time.time()-float(v[0]))
            mem_del.append(hash1[k])
        else:
            print(k,": ", hash1[k])
    #for i in hash1:
    #    members.append(hash1[i])
    #print('length: ', mem_del)
    return mem_del
def resetV(v_current):
    mem = []
    for i in range(1, len(v_current)-1):
        if((time.time() - v_current[i][0]>5)):
            print('Being Popped:' , v_current[i], 'At Time :' , (time.time()-v_current[i][0]))
            mem.append(i)
    for ii in range(1, len(mem)-1):
        del v_current[mem[ii]]
    return v_current
