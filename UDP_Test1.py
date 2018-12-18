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
while 1:
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
            data = data.split()
	    #print(data)
            if(int(data[1]) == 1):
                #dp.time = time.time()
                #dp.anchor = data[3]
                #dp.power = data[4]
                #dp.distance = data[2]
                x = datapoint(time.time(),data[3],data[4],data[2])
	        values = x.get_dp()
	        dplist[data[3]] = values
		#print(dplist)
		currentDataPoints = rcd.resetcurrentdatapoints(dplist)
                #print(len(currentDataPoints))
                if(len(currentDataPoints) >= 3):
                    tri.trilateration(currentDataPoints)
                #else:
                #    print("not enough points")
            else:
                #print("Not a valid input")
		pass

        finally:
            pass
            #print >>sys.stderr, 'closing socket'
            #sock.close()
    	#time.sleep(3)

