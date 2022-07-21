import pyvisa
import time
import math
import numpy

class Keysight_PS():
    def __init__(self, GPIB_Address = 10):

        self.GPIB_Address = GPIB_Address
        # visa.log_to_screen()
        rm = pyvisa.ResourceManager()

        self.SigGen = rm.open_resource("GPIB0::%d::INSTR" %(GPIB_Address))

    def turnOn(self):
        self.SigGen.write("OUTP:STAT ON")

    def turnOff(self):
        self.SigGen.write("OUTP:STAT OFF")
