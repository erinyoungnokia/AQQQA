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
FPGA_Wait = 180
IIP3 = False
Antenna = False

num = 1
data_set = []
Power = 12
startPow = Power

#Test Cases
Made = [0]
Cap_Point = [50]

#SetUP
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)

excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\X11_SingleTone_ATT.xlsx'
cap_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'

for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x],C_Band)
    time.sleep(5)
    activeMade.sshWrite('python3 Palau_Test_20220705_MK7.py -t AgcCfgSet')

    activeMade.sshRead()
    time.sleep(5)
    #activeMade.sshWrite('python3 Palau_Test_20220705.py -t MGC')

    #activeMade.sshRead()
    time.sleep(5)

    for y in range(0, len(Cap_Point)):
        Power = startPow
        row = 2
        Set.Set_Switch(x, y, Cap_Point)

        for z in range(0,16):
            file_name = 'Made{}_{}_AGC_{}dbmUP_MK7.txt'.format(str(Made[x]), str(Cap_Point[y]),str(Power))
            #Set.Set_SigGen(x, y, Cap_Point, Power + Offset[(4 * x) + (y)], freq)
            Set.Set_SigGen(x, y, Cap_Point, Power+4.7, freq)
            time.sleep(1)
            Cap.Cap_ATT(x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq,file_name,excel_file_path,cap_file_path,Power,cap_file_path+file_name,row)
            Power = Power + .5
            row = row + 1
