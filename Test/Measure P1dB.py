import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions
import matplotlib.pyplot as plt

#Parameters
freq = 3510e6
Temp = 25
SETUP_FPGA = False
FPGA_Wait = 600
IIP3 = False
Antenna = True
cen_freq = 3500e6
num = 1
data_set = []

#Test Cases
Made = [11]
Cap_Point = [50]

#P1 Parameters

endPower = -10
setPower = -40
points = endPower - setPower



#EXCEL File
excel_file_name = 'P1dB_Measurements.xlsx'
excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\P1dB Measurements\\P1dB_Measurements.xlsx'
gain_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\P1dB Measurements\\'

#SetUP
Set = Set_Up.Set_Up()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)
Cap = Capture_Functions.Captures()


for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x])

    for y in range(0, len(Cap_Point)):
        Power = setPower
        g_file_name = 'Made{}_{}_pwr{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(Power))
        Set.Set_Switch(x, y, Cap_Point)
        Cap.P1dB(Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power,Temp,Offset,freq,activeMade,Set,cen_freq,g_file_name,num,data_set,points,setPower)

    Set.Set_Made_Off(x, IIP3,activeMade)



