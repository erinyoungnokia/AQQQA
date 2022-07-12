import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions
import matplotlib.pyplot as plt

#Parameters
freq = 3960e6
Temp = 25

FPGA_Wait = 120
IIP3 = False
Antenna = False
cen_freq = 3850e6
num = 1
data_set = []
Power = -60
made = True
dist = 10e6

#Test Cases
Made = [0]
Cap_Point = [50]

#SetUP
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()


excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'
cap_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'


for x in range(0, len(Made)):

    activeMade = Set.Made_Setup(Made[x])
    time.sleep(10)

    for y in range(0, len(Cap_Point)):
        file_name = 'Made{}_{}_MGC_-51.5dbm_ATT-0db.txt'.format(str(Made[x]), str(Cap_Point[y]))
        excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'
        cap_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'

        #Set.Set_Switch(x,y,Cap_Point)
        #Set.Set_SigGen(x,y,Cap_Point,Power + Offset[(4 * x) + (y)],freq)
        Cap.Cap_IIP3(x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq,file_name,dist)


activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_SHUTDOWN.sh')
