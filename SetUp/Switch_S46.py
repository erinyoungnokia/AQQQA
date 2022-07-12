
import pyvisa
import logging, coloredlogs
import time
import re

logger = logging.getLogger(__name__)

class Switch_S46:

    def __init__(self, GPIB_Address = 7):
        self.GPIB_Address = GPIB_Address
        rm = pyvisa.ResourceManager()
        self.Switch = rm.open_resource("GPIB0::%d::INSTR" %(GPIB_Address))

    def closeChannel(self,chNum):
        self.Switch.write(':ROUT:CLOS (@%d)' %chNum)
        time.sleep(1)

    def openChannel(self,chNum):
        self.Switch.write(':ROUT:OPEN (@%d)'%chNum)

    def openAll(self):
        closedChannels = self.getClosedChannels()

        for channel in closedChannels:
            self.openChannel(channel)


        time.sleep(5)

    def getClosedChannels(self):
        closedChannels = self.Switch.query(':ROUT:CLOS?')
        logger.info("closed channels: "+ str(closedChannels))

        temp = re.findall(r'\d+', closedChannels)
        res = list(map(int, temp))
        # logger.info(res)
        return res

    def cleanUp(self):
        # self.turnOuputOFF()
        self.Switch.close()
        del self.Switch
        logger.info("closing the connection to Switch")




if __name__ == "__main__":
    coloredlogs.install(level='info')
    SwitchObj = Switch_S46T(GPIB_Address=7)
    # SwitchObj.closeChannel(1)
    # SwitchObj.openChannel(1)
    # SwitchObj.closeChannel(1)
    SwitchObj.getClosedChannels()

    SwitchObj.openAll()
    SwitchObj.getClosedChannels()