import socket
import random
import json
from datapoint import datapoint
import time
import reset_current_datapoints as rcd
import trilat as tri
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
        self.z =0.0
        self.time_T = time_T
        self.px=0.0
        self.py = 0.0
        self.pz = 0.0
        self.dist = 0.0
        self.ini = True
        self.user = user
    def update_xy(self,x,y,z,time_T):
        if(not self.ini):
            if( time_T-self.time_T <= 3):
                self.dist = np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2 + (self.z - z) ** 2)
                if(self.dist<=5):
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
        else:
            self.x = x
            self.y = y
            self.z = z
            self.px = self.x
            self.py = self.y
            self.pz = self.z
            self.time_T = time_T
            self.ini = False



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
socket_for_sending.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket_for_sending.bind((host,port))
socket_for_sending.listen(1) 

tag = Tag(time.time(),host,"vehicle1")
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
                dplist[data[3]] = values
                currentDataPoints = rcd.resetcurrentdatapoints(dplist)
                if(len(currentDataPoints) >= 3):
                    location_tag =  tri.trilateration(currentDataPoints)
                    tag.update_xy(location_tag.x,location_tag.y,location_tag.z,time.time())
                cc1, addr1 = socket_for_sending.accept()
                cc1.send(bytes(str([str(tag.x), str(tag.y), str(tag.z), tag.user]).encode()))
                cc1.close()
            else:
                pass
        finally:
            pass



