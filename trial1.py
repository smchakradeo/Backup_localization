import socket
import random
import json
from datapoint import datapoint
import time
import reset_current_datapoints as rcd
#import trilat as tri
import numpy as np
class Anchor:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z

class Tag:
    def __init__(self, time_T, ip, user):
        self.ip = ip
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.time_T = time_T
        self.px = 0.0
        self.py = 0.0
        self.pz = 0.0
        self.dist = 0.0
        self.ini = True
        self.user = user

    def update_xy(self, x, y, z, time_T):
        if (not self.ini):
            if (time_T - self.time_T <= 3):
                self.dist = np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2)
                if (self.dist <= 5):
                    self.px = self.x
                    self.py = self.y
                    self.pz = self.z
                    self.x = x
                    self.y = y
                    self.z = z
                    self.time_T = time_T
                else:
                    self.time_T = time_T
            else:
                self.px = self.x
                self.py = self.y
                self.pz = self.z
                self.x = x
                self.y = y
                self.z = z
                self.time_T = time_T
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
#socket_for_sending = socket.socket()
host = '192.168.50.254'
port = 12345
#socket_for_sending.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#socket_for_sending.bind((host,port))
#socket_for_sending.listen(1)
tag = Tag(time.time(),host,"vehicle1")

def filesave(data_save):
    #data_save = data_save.strip()
    #data_save = str(data_save).strip('[ ]')
    #data_save = data_save.strip("' '")
    inp1 = open("vehicle_1_back.txt", "a+")
    inp1.write(data_save)
    inp1.write("\n")
    inp1.close()
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
#create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1',5678)
t = time.time()
while 1:
    #On board sensor collection
    rdm_num = random.randint(1,100)
    message2 = str(rdm_num) + ' 51'
    for i in id:
        message1 = str(rdm_num) + ' 50' + ' '+ i
        try:
            # Send data
            sent1 = sock.sendto(bytes(message1.encode()), server_address)
            # Receive response
            data1, server1 = sock.recvfrom(4096)
            data1 = data1.decode("utf-8")
            data1 = data1.strip('{ }')
            data1 = data1.split()
            sent2 = sock.sendto(bytes(message2.encode()), server_address)
            data2, server2 = sock.recvfrom(4096)
            data2 = data2.decode("utf-8")
            data2 = data2.strip('{ }')
            data2 = data2.split()
            #print('data1: ', data1)
            if((int(data1[1]) == 1) and (not (int(data2[1]) == 255)) and len(data2) == 14):
                data_new = str([data2[2], tag.ip, data1[2], data1[3], data2[3], data2[4], data2[5], data2[6], data2[7], data2[8], data2[9], data2[10],data2[11], data2[12], data1[4]])
                print('1: ', data_new)
                filesave(data_new)
            elif((int(data1[1]) == 1) and (int(data2[1]) == 255)):
                data_new = str([time.time()*1000, tag.ip, data1[2], data1[3],"NA", "NA", "NA", "NA","NA","NA","NA","NA","NA","NA", data1[4]])
                print('2: ', data_new)
                filesave(data_new)
            elif(not (int(data1[1]) == 1) and (not (int(data2[1]) == 255)) and len(data2) == 14):
                data_new = str([data2[2], tag.ip,"NA","NA", data2[3], data2[4], data2[5], data2[6], data2[7], data2[8], data2[9], data2[10],data2[11],data2[12], "NA"])
                print('3: ',data_new)
                filesave(data_new)
            else:
                pass
        finally:
            pass




