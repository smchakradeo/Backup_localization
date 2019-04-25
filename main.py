from datapoint import datapoint
import reset_current_datapoints as rcd
import trilat as tri
import numpy as np
import matplotlib.pyplot as plt
class Anchor:
    def __init__(self, id, x, y, z):
        self.id = id
        self.x = x
        self.y = y
        self.z = z




"""
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
            #self.ini = False



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



tag = Tag(time.time(),"vehicle1")
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
"""


def filesave(data_save):
    inp1 = open("C:\\Users\\smchakra\\Desktop\\Data.txt","a+")
    #print(data_save[0])
    inp1.write(str(data_save))
    inp1.write("\n")
    inp1.close()

dplist = {}
f = open('C:\\Users\\smchakra\\Desktop\\Experiments\\Experiments_Python\\Construction site\\Experiment_4\\Raw\\walking_1_head.txt','r')
line = f.readline()
splitted = line.split(",")
timestamp = float(splitted[0].strip("[").strip("'"))
time_window = 1000.0 # time window to consider the anchor readings in
moving_window = 400.0 # moving window
location_tag = np.array([0.0,0.0],float).reshape(-1,1)
try:
    while line:
        line = f.readline()
        line = line.replace("'", '')
        splitted = line.rstrip().split(",")
        data = splitted
        if(len(splitted)==15 and float(splitted[2].strip("' '"))>0 and float(splitted[14].replace("'", '').strip().strip("]"))>-105): # RSSI greater than -105 and the distance should not be negative
            x = datapoint(float(splitted[0].rstrip().strip("[").strip("'")),(str(splitted[3].strip().replace("'", ''))), float(splitted[14].replace("'", '').strip().strip("]")),float(splitted[2].strip("' '")))
            values = x.get_dp()
            if(float(splitted[0].rstrip().strip("[").strip("'")) - timestamp < time_window):
                dplist[str(splitted[3].strip())] = values
            else:
                if(len(dplist)>=3):
                    location_tag_current = tri.trilateration(dplist)
                    data.append(str(location_tag_current[0]))
                    data.append(str(location_tag_current[1]))
                    location_tag = np.hstack((location_tag, location_tag_current.reshape(-1,1)))
                timestamp = float(splitted[0].rstrip().strip("[").strip("'"))
                currentDataPoints = rcd.resetcurrentdatapoints(timestamp, dplist)
        #filesave(data)
finally:
    pass
    plt.scatter(location_tag[0, :].flatten(), location_tag[1, :].flatten())
    plt.plot(location_tag[0, :].flatten(), location_tag[1, :].flatten(), "-k")
    plt.axis("equal")
    plt.grid(True)
