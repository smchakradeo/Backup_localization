import sys
sys.path.insert(0,"/home/pi/.local/lib/python3.5/site-packages/localization")
import localization as lx
import json

inp_data = open("Config.json", "r")
json_data = json.load(inp_data)
anchors = [json_data["anchors1"]]
id, x, y, z = [], [], [], []
P=lx.Project(mode='2D',solver='LSE')

for i in anchors:
    for j in range(len(i)):
       # id.append(i[j]["id"])
       # x.append(i[j]["x"])
       # y.append(i[j]["y"])
       # z.append(i[j]["z"])
        P.add_anchor(str(i[j]["id"]),(i[j]["x"], i[j]["y"]))
        

def trilateration(hash_list):
    t,label=P.add_target()

    #t.add_measure('anchore_A',50)
    #t.add_measure('anchore_B',50)
    #t.add_measure('anchore_C',50)
    for i in hash_list:
        t.add_measure(i[1], i[3])
    try:        
        P.solve()
        print(t.loc)
        return t.loc
    except ZeroDivisionError:
        pass
