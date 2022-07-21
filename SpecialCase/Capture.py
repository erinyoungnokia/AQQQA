import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions
import matplotlib.pyplot as plt
C_Band = True

if C_Band == True:
    cen_freq = 3840e6
else:
    cen_freq = 3500e6

#Parameters
freq = 3850e6
Temp = 25
SETUP_FPGA = False
FPGA_Wait = 120
IIP3 = False
Antenna = False
num = 1
data_set = []
Power = -60

#Test Cases
Made = [1]
Cap_Point = [52]

#SetUP
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)

excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'
cap_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'

for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x],C_Band)

    for y in range(0, len(Cap_Point)):
        Set.Set_Switch(x,y,Cap_Point)
        #Set.Set_SigGen(x,y,Cap_Point,Power + Offset[(4 * x) + (y)],freq)
        Set.Set_SigGen(x, y, Cap_Point, Power + 1.44, freq)
        Cap.Cap(x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq)
    Set.Set_Made_Off(x,IIP3,activeMade)