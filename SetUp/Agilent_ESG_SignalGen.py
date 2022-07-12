import pyvisa
import time
import math
import numpy
import logging

logger = logging.getLogger(__name__)

class Agilent_SigGen_ESG():

    def __init__(self, GPIB_Address = 20):
        logger.info("connecting to Signal generator")
        self.GPIB_Address = GPIB_Address
        # visa.log_to_screen()
        rm = pyvisa.ResourceManager()

        self.SigGen = rm.open_resource("GPIB0::%d::INSTR" %(GPIB_Address))
        logger.info(self.getID())


    def getFrequency(self):
        return self.SigGen.query("FREQ:CW?")

    def setFrequency(self, Frequency):

        self.SigGen.write("FREQ:CW %f" % (Frequency))
        self.SigGen.query("*OPC?")

    def getID(self):
        return self.SigGen.query("*IDN?")

    def setPowerdBm(self, pow):
        self.SigGen.write("POW:AMPL "+str(pow)+"dBm")
        self.SigGen.query("*OPC?")

    def getPower(self):
        return self.SigGen.query(":OUTP:LEV?")

    def getAmplitudeOffset(self):
        # return  self.SigGen.query("POW:OFFS?")
        return self.SigGen.query("POW:OFFS?")

    def setAmplitudeOffset(self, offset):
        self.SigGen.write("POW:OFFS "+str(offset)+" dBm")

    def getOutputState(self):
        return self.SigGen.query(":OUTP:STAT?")

    def turnOuputON(self):
        self.SigGen.write(":OUTP:STAT ON")
        #self.SigGen.query("*OPC?")

    def turnOuputOFF(self):
        self.SigGen.write(":OUTP:STAT OFF")
        self.SigGen.query("*OPC?")

    def AmpUp(self):
        self.SigGen.write("POW:OUTP:LEV UP")

    def AmpDown(self):
        self.SigGen.write("POW:OUTP:LEV DOWN")

    def setAMState(self,state):
        self.SigGen.write("AM:STAT "+state)

    def getAMState(self):
        return self.SigGen.query("AM:STAT?")

    def getAMFrequency(self):
        return self.SigGen.query("AM:FREQ?")

    def setAMFrequency(self, freq):
        self.SigGen.write("AM:FREQ "+str(freq)+"KHZ")

    def getAMSource(self):
        return self.SigGen.query("AM:SOUR?")

    def setAMSource(self,source):
        self.SigGen.write("AM:SOUR "+source)

    def getAMDepth(self):
        return self.SigGen.query("AM:DEPT?")

    def setAMDepth(self, pct):
        self.SigGen.write("AM:DEPT "+str(pct)+"%")

    def getModState(self):
        return self.SigGen.query("MOD:STAT?")

    def setModState(self,state):
        self.SigGen.write("MOD:STAT "+str(state))

    def turnMtoneOn(self):
        self.SigGen.write(":RAD:MTON:ARB:STAT ON")

    def turnMtoneOff(self):
        self.SigGen.write(":RAD:MTON:ARB:STAT OFF")

    def setMTone(self,freq,nTon):
        self.SigGen.write(":RAD:MTON:ARB:SET:TABL:PHAS:INIT FIX")
        self.SigGen.write(":RAD:MTON:ARB:SET:TABL:NTON "+str(nTon))
        self.SigGen.write(":RAD:MTON:ARB:SET:TABL:FSP " + str(freq))

    def cleanUp(self):
        # self.turnOuputOFF()
        self.SigGen.close()
        del self.SigGen
        logger.info("closing the connection to SigGen")

    # def __del__(self):
    #     self.cleanUp()

if __name__ == "__main__":
    SigGenObj = Agilent_SigGen(GPIB_Address=19)
    ampOfset = 0
    SigGenObj.setPowerdBm(-20-ampOfset)
    # SigGenObj.setAMState("OFF")
    # print(SigGenObj.getAMState())
    # print(SigGenObj.getAMFrequency())
    SigGenObj.setFrequency(3691e6)
    print("Sig gen is set to: " + SigGenObj.getFrequency())
    # print(SigGenObj.getID())
    # SigGenObj.turnOuputOFF()
    # SigGenObj.setAmplitudeOffset(-1.0)
    # print(SigGenObj.getAmplitudeOffset())
    # print(SigGenObj.getOutputState())
    # SigGenObj.turnOuputON()
    SigGenObj.setAMDepth(100)
    print(SigGenObj.getAMDepth())
    print(SigGenObj.getOutputState())
    SigGenObj.setAMState("OFF")
    SigGenObj.setAMFrequency(5)
    print(SigGenObj.getAMState())
    print(SigGenObj.getModState())
    SigGenObj.setAMSource("INT")
    print(SigGenObj.getAMSource())

    SigGenObj.turnOuputON()


    # SigGenObj.cleanUp()

