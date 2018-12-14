import socket
import random
import json
import datapoint as dp
import time

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

input_data = open("Config.json", "r")
json_data = json.load(input_data)
anchors = [json_data["anchors1"]]
tags = [json_data["tags1"]]
id, x, y, z = [], [], [], []
ip, user = [], []
for i in anchors:
    for j in range(len(i)):
        id.append(i[j]["id"])
        x.append(i[j]["x"])
        y.append(i[j]["y"])
        z.append(i[j]["z"])

for i in tags:
    for j in range(len(i)):
        ip.append(i[j]["ip"])
        user.append(i[j]["user"])

for i in id:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('127.0.0.1', 5678)
    message = str(random.randint(1,101)) + ' 50' + ' '+ i
    #print(message)
    try:

        # Send data
        sent = sock.sendto(message, server_address)

        # Receive response
        data, server = sock.recvfrom(4096)
	data = data.strip('{ }')
	#data = data.strip('{')
        data = data.split()
        if(int(data[1]) == 1):
    	    print(data)
            dp.time = time.time()
            dp.anchor = data[3]
            dp.power = data[4]
            dp.distance = data[2]
            

    finally:
        pass
        #print >>sys.stderr, 'closing socket'
        #sock.close()
