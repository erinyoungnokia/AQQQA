import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions
import matplotlib.pyplot as plt

#Parameters
freq = 3860e6
Temp = 25
Power = -40
SETUP_FPGA = False
FPGA_Wait = 120
IIP3 = False
Antenna = False
cen_freq = 3840e6
num_cap = 30
data_set = []
BW = 10e6

#Test Cases
Made = [0]
Cap_Point = [50,52,54,56]

#EXCEL File
file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Full Unit Capture\\TEST\\'
excel_path = file_path + 'NF_Measurements_X11.xlsx'

#SetUP
Set = Set_Up.Set_Up()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)
Cap = Capture_Functions.Captures()


for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x])
    for y in range(0, len(Cap_Point)):
        g_file_name = 'Made{}_{}_{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(freq))
        Set.Set_Switch(x, y, Cap_Point)
        Set.Set_SigGen(x, y, Cap_Point, Power + Offset[(4 * x) + (y)], freq)
        Cap.NF(Made,x,y,Cap_Point,excel_path,file_path,Power,Temp,Offset,freq,activeMade,Set,cen_freq,num_cap,data_set,BW,g_file_name)
    Set.Set_Made_Off(x, IIP3, activeMade)