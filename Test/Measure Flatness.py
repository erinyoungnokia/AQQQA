import time
from SetUp import Set_Up, SshInterface, Excel, Capture_Functions


C_Band = True

if C_Band == True:
    cen_freq = 3840e6
else:
    cen_freq = 3500e6

#Parameters
FP = [3460e6, 3500e6, 3540e6]
Power = -60
Temp = 25
SETUP_FPGA = False
FPGA_Wait = 180
IIP3 = False
Antenna = True

num = 1
data_set = []

#Test Cases
Made = [12,13,14]
Cap_Point = [54,56]

#EXCEL File
excel_file_name = 'Gain_Flatness_Measurements_X11.xlsx'
excel_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Gain Flatness Measurements\\Gain_Flatness_Measurements_X11.xlsx'
gain_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\Gain Flatness Measurements\\'


#SetUP
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()
Offset = Set.CableOffset(Antenna)
Set.FPGA_Setup(SETUP_FPGA,FPGA_Wait)

for x in range(1, len(Made)):
    activeMade = Set.Made_Setup(Made[x],C_Band)
    for y in range(0, len(Cap_Point)):
        Set.Set_Switch(x, y, Cap_Point)
        for z in range(0, len(FP)):
            freq = FP[z]
            Set.Set_SigGen(x, y, Cap_Point, Power + Offset[(4 * x) + (y)], freq)
            g_file_name = 'Made{}_{}_{}.txt'.format(str(Made[x]),str(Cap_Point[y]),str(freq))
            Cap.Flatness(Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power,Temp,Offset[(4 * x) + (y)],freq,activeMade,cen_freq,g_file_name,num,data_set)


            #Set.Set_Test_Off(x,IIP3)
    Set.Set_Made_Off(x,IIP3,activeMade)




