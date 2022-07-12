from SetUp import Set_Up, Excel, Capture_Functions

Made = [15]
Cap_Point = [56]
x = 0
y = 0
Power = -60
Antenna = False
freq = 3505e6
dist = 5e6

Set = Set_Up.Set_Up()
Offset = Set.CableOffset(Antenna)
#Set.Set_SigGen_IIP3(Power + Offset[(4 * x) + (y)],dist,freq)
print("Power ={}".format(str(Power)))
print('Offset = {}'.format(str(Offset[(4 * x) + (y)])))
print('Output = {}'.format(Power + Offset[(4 * x) + (y)]) )

Set.Set_SigGen(x,y,Cap_Point,Power + Offset[(4 * x) + (y)],freq)