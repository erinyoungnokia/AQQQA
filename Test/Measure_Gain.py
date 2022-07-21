import time
from SetUp import Set_Up, Excel, Capture_Functions



C_Band = True

if C_Band == True:
    cen_freq = 3840e6
else:
    cen_freq = 3500e6

#Parameters

freq = 3850e6
Power = -60
Temp = 25
SETUP_FPGA = False
FPGA_Wait = 150
IIP3 = False
Antenna = False
num_cap = 1

#Test Cases
Made = [1]
Cap_Point = [50,52,54,56]


#EXCEL File
excel_file_name = 'Gain_Measurements_X11.xlsx'
excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Gain Measurements\\Gain_Measurements_X11.xlsx'
gain_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Gain Measurements\\'

#SetUP
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)

for x in range(0, len(Made)):
    activeMade = Set.Made_Setup(Made[x], C_Band)

    for y in range(0, len(Cap_Point)):
        Set.Set_Switch(x,y,Cap_Point)
        Set.Set_SigGen(x,y,Cap_Point,Power + Offset[(4 * x) + (y)],freq)
        Cap.Gain(Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power,Temp,Offset[(4 * x) + (y)],activeMade,cen_freq,num_cap)
        time.sleep(3)

    Set.Set_Made_Off(x,IIP3,activeMade)








