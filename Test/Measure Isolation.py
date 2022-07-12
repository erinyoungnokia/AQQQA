import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions

#Parameters
freq = 3510e6
Power = -40
Temp = 25
SETUP_FPGA = False
FPGA_Wait = 180
IIP3 = False
Antenna = True
cen_freq = 3500e6
num = 1
data_set = []

#Test Cases
Made = [8]
Cap_Point = [50,52,54,56]
ISO_LIST = [8,9,10,12,13,14,15]

#EXCEL File
excel_file_name = 'ISO_Measurements_X11.xlsx'
excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\ISO_Measurements_X11.xlsx'
iso_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\'

#SetUP
Set = Set_Up.Set_Up()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)
Cap = Capture_Functions.Captures()
for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x])
    for y in range(0, len(Cap_Point)):
        Set.Set_Switch(x, y, Cap_Point)
        Set.Set_SigGen(x, y, Cap_Point, Power + Offset[(4 * x) + (y)], freq)
        peak_gain = Cap.ISO_Gain(Made,x,y,Cap_Point,excel_file_path,iso_file_path,Power,Temp,Offset,freq,activeMade,Set,cen_freq,num,data_set)
    Set.Set_Made_Off(x,IIP3,activeMade)
    for m in range(0, len(ISO_LIST)):
        activeMade = Cap.ISO_Meas(Made, x, y, Cap_Point, excel_file_path, iso_file_path, Power, Temp, Offset, freq, activeMade,Set, cen_freq, num, data_set,ISO_LIST,m,peak_gain)
        if m+8 != Made[x]:
            Set.Set_Made_Off(x,IIP3,activeMade)