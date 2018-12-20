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
    for i in range(1, len(v_current)):
        if((time.time() - v_current[i][0]>10)):
            v_current.pop(i)
    return v_current