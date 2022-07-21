from SetUp import Keysight_PS

Set = Keysight_PS.Keysight_PS()


ON = True

if ON == True:
    Set.turnOn()
else:
    Set.turnOff()