import socket
import random
import json
from datapoint import datapoint
import time
import reset_current_datapoints as rcd
import trilat as tri
class Anchor:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

class Tag:
    def __init__(self, ip, user):
        self.ip = ip
        self.user = user


dplist = {}
malist = {}
input_data = open("Config.json", "r")
json_data = json.load(input_data)
anchors = [json_data["anchors1"]]
tags = [json_data["tags1"]]
values_all = []
id, x, y, z = [], [], [], []
ip, user = [], []
thresh = 2
socket_for_sending = socket.socket()
host = '192.168.50.231'
port = 12345
socket_for_sending.bind((host,port))
socket_for_sending.listen(1) 
for i in anchors:
    for j in range(len(i)):
        id.append(i[j]["id"])
        x.append(i[j]["x"])
        y.append(i[j]["y"])
        z.append(i[j]["z"])
        malist[i[j]["id"]] = [[thresh]]

for i in tags:
    for j in range(len(i)):
        ip.append(i[j]["ip"])
        user.append(i[j]["user"])
while 1:
    for i in id:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 5678)
        message = str(random.randint(1,101)) + ' 50' + ' '+ i
        try:

            # Send data
            sent = sock.sendto(bytes(message.encode()), server_address)
            # Receive response
            data, server = sock.recvfrom(4096)
            data = data.decode("utf-8")
            data = data.strip('{ }')
            data = data.split()
            if(int(data[1]) == 1):
                x = datapoint(time.time(),data[3],data[4],data[2])
                values = x.get_dp()

                for k,v in malist.items():
                    if k == data[3]:
                        print("id: " , k)
                        v = rcd.resetV(v)
                        if(len(v)<3):
                            v.append(values)
                            malist[k] = v
                            break
                        else:
                            sum_all = 0
                            for ii in range(1, len(v)):
                                sum_all = sum_all + float(v[ii][3])
                            avg = sum_all/(len(v)-1)
                            if (float(values[3]) < avg - float(v[0][0]) or float(values[3]) > avg + float(v[0][0])):
                                v[0][0] = v[0][0] + 0.5
                                values = v[len(v)-1]
                                v.append(values)
                                malist[k] = v
                                break
                            else:
                                v.append(values)
                                malist[k] = v
                                break
                    else:
                        pass
                dplist[data[3]] = values
                currentDataPoints = rcd.resetcurrentdatapoints(dplist)
                if(len(currentDataPoints) >= 3):
                   location_tag =  tri.trilateration(currentDataPoints)
                   cc1, addr1 = socket_for_sending.accept()
                   cc1.send(bytes(str(location_tag).encode()))
                   cc1.close()
            else:
                pass
        finally:
            pass


