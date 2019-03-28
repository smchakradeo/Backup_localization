import socket
import random
import json
from datapoint import datapoint
import time
import reset_current_datapoints as rcd
#import trilat as tri
import numpy as np

input_data = open("Config.json", "r")
json_data = json.load(input_data)
anchors = [json_data["anchors1"]]
id, x, y, z = [], [], [], []

for i in anchors:
    for j in range(len(i)):
        id.append(i[j]["id"])
        x.append(i[j]["x"])
        y.append(i[j]["y"])
        z.append(i[j]["z"])
count_var = {}
for i in id:
   count_var[i] = 0
   
   
f = open("temp.txt")
line = f.readline()
while line:
	line = f.readline()
	line = line.strip()
	print(line)
	splitted = line.split(",")
	for i in splitted:
		for j in id:
			if str(i).strip().replace("'",'')==str(j):
				count_var[j] = count_var[j]+1

print(count_var)
	
