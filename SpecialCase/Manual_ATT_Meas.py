from SetUp import Set_Up, Excel, Capture_Functions, Agilent_ESG_SignalGen

Made = [0]
Cap_Point = [50]
x = 0
y = 0

Power = -18

Increment = .5
Antenna = False
freq = 3845e6
dist = 5e6
C_Band = True
if C_Band == True:
    cen_freq = 3840e6
else:
    cen_freq = 3500e6
Set = Set_Up.Set_Up()
Cap = Capture_Functions.Captures()
Offset = Set.CableOffset(Antenna)
ESG = Set_Up.Agilent_SigGen_ESG()
activeMade = Set.Made_Setup(Made[x],C_Band)
cap_file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\SC\\'
while(True):
#Set.Set_SigGen_IIP3(Power + Offset[(4 * x) + (y)],dist,freq)


    cc = input('Press 1 to increase, 2 to decrease, 3 to turn ON, 4 to turn Off, 5 to end\n')
    cc = float(cc)
    if int(cc) == 1:
        Power = Power + Increment
        print("Power ={}".format(str(Power)))
        print('Offset = {}'.format(str(1.44)))

        Set.Set_SigGen(x, y, Cap_Point, Power + 1.44, freq)
    elif int(cc) == 2:
        Power = Power - Increment
        print("Power ={}".format(str(Power)))
        print('Offset = {}'.format(str(1.44)))

        Set.Set_SigGen(x, y, Cap_Point, Power + 1.44, freq)
    elif int(cc) == 3:
        ESG.turnOuputON()
        print('Turned On')
        print("Power ={}".format(str(Power)))
        print('Offset = {}'.format(str(1.44)))
    elif int(cc) == 4:
        ESG.turnOuputOFF()
        print('Turned Off')
    else:
        ESG.turnOuputOFF()
        print("Exit")
        break

    Cap.Cap(x, y, Cap_Point, Made, activeMade, Set, cap_file_path, cen_freq)




