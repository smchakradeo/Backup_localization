import socket
import math
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
host = '192.168.50.145'
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
        message = str(random.randint(1,101)) + ' 51'
        try:

            # Send data
            sent = sock.sendto(bytes(message.encode()), server_address)
            # Receive response
            data, server = sock.recvfrom(4096)
            data = data.decode("utf-8")
            data = data.strip('{ }')
            data = data.split()
            if((not (int(data[1]) == 255)) and len(data) == 14):
                #print('Acc: ', data[3], ' ',data[4],' ',data[5],' ','Gyro: ',data[6],' ',data[7],' ',data[8],' ','Mag: ',data[9],' ',data[10],' ',data[11])
                tot = (float(data[3])**2+float(data[4])**2+float(data[5])**2)**0.5
                print('Mag: ',data[9],' | ',data[10],' | ', data[11])
                theta = math.degrees(math.atan2((float(data[4])/tot),(float(data[3])/tot)))
                alpha = math.degrees(math.atan2((float(data[5])/tot),(((float(data[3])**2+float(data[4])**2))**0.5)/tot))
                #print('Acc: ', data[3], ' ',data[4],' ',data[5], '| Alpha: ', alpha, ' |Theta: ', theta)
                time.sleep(0.1)
        finally:
            pass


