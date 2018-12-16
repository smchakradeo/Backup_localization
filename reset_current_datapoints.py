import time
def resetcurrentdatapoints(hash):
    members = []
    for k,v in hash.items():
        if((time.time() - float(v[0])) > 10):
		del hash[k]
    for i in hash:
        members.append(hash[i])
        print(members)
    return members
