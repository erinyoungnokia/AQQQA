from SetUp import Set_Up, Excel, Capture_Functions

Made = [15]
Cap_Point = [56]
x = 0
y = 0

Power = -60
Antenna = False
freq = 3845e6
dist = 5e6

Set = Set_Up.Set_Up()
Offset = Set.CableOffset(Antenna)
while(True):
#Set.Set_SigGen_IIP3(Power + Offset[(4 * x) + (y)],dist,freq)
    cc = input()
    cc = float(cc)
    if int(cc) == 1:
        Power = Power + .5
    else:
        Power = Power - .5

    print("Power ={}".format(str(Power)))
    print('Offset = {}'.format(str(1.44)))


    Set.Set_SigGen(x,y,Cap_Point,Power+1.44,freq)