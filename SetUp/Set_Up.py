import time

from SetUp.SshInterface import SshInterface
from SetUp.Switch_S46 import Switch_S46
from SetUp.Agilent_ESG_SignalGen import Agilent_SigGen_ESG
from SetUp.Agilent_MXA_SIGGen import Agilent_SigGen_MXA
from SetUp.Agilent_PSG_SigGen import Agilent_SigGen_PSG

class Set_Up:



    def CableOffset(self,Antenna):
        # Set Offsets
        L = 2
        LA = 1.3
        LB = 1.6
        LC = .5
        LC1 = .2
        LC2 = .4
        LF = 1.2

        LS1 = 1.2
        L1A = .8
        L1B = 1.3
        LS2 = .5
        LC1 = .4
        LC2 = .2

        L1 = LS1 + L1A + 1.35
        L2 = LS1 + L1A + 1.55
        L3 = LS1 + L1A + 1.90
        L4 = LS1 + L1A + .95
        L5 = LS1 + L1A + 1.3
        L6 = LS1 + L1A + 1.5
        L7 = LS1 + L1B + 1.35
        L8 = LS1 + L1B + .95
        L9 = LS1 + L1B + 1.5
        L10 = LS1 + L1B + 1.6
        L11 = LS1 + L1B + 1.4
        L12 = LS1 + L1B + 1.2
        L13 = LS2 + LC1 + 2
        L14 = LS2 + LC1 + 1.75
        L15 = LS2 + LC2 + 2
        L16 = LS2 + LC2 + 2.25
        Offset = [L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13, L14, L15, L16]
        if Antenna == True:
            for x in range(0,len(Offset)):
                Offset[x] = Offset[x] + .7

        return Offset
    def FPGA_Setup(self,Setup,Timeout):
        if Setup == True:
            activeFPGA = SshInterface('192.168.101.1')
            activeFPGA.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\FPGA_SETUP.sh', '/var/tmp/FPGA_SETUP.sh')
            activeFPGA.sshWrite('sudo lmi-eth on')
            activeFPGA.sshRead()
            activeFPGA.sshWrite('cd /var/tmp/')
            activeFPGA.sshRead()
            activeFPGA.sshWrite('chmod +x FPGA_SETUP.sh')
            activeFPGA.sshRead()
            activeFPGA.sshWrite('sudo  frmonShellClient 127.0.0.1 2000 ./FPGA_SETUP.sh')
            activeFPGA.sshRead()
            print("Wait {} seconds".format(str(Timeout)))
            time.sleep(Timeout)
            activeFPGA.SSHClose()

    def Made_Setup(self,Made,Board):
        activeMade = SshInterface('192.168.101.{}'.format(str(Made + 2)))
        activeMade.sshRead()
        time.sleep(2)
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\capture_ul', '/var/tmp/capture_ul')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\MADE_SETUP.sh', '/var/tmp/MADE_SETUP.sh')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\FRMON_CREATE_C.sh', '/var/tmp/FRMON_CREATE_C.sh')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\FRMON_CREATE_DOD.sh', '/var/tmp/FRMON_CREATE_DOD.sh')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\MADE_SHUTDOWN.sh', '/var/tmp/MADE_SHUTDOWN.sh')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\FRMON_SHUTDOWN.sh', '/var/tmp/FRMON_SHUTDOWN.sh')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\Palau_AGC.py', '/var/tmp/Palau_AGC.py')
        activeMade.putFile('C:\\Users\\eryoung\\Desktop\\Captures\\Palau_Test_20220705_MK7.py',
                           '/var/tmp/Palau_Test_20220705_MK7.py')

        activeMade.sshWrite('cd /var/tmp/\n')
        activeMade.sshRead()
        activeMade.sshWrite('sudo chmod +x *')
        activeMade.sshRead()

        if Board == True:
            activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_CREATE_C.sh')
            activeMade.sshRead()
        else:
            activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_CREATE_DOD.sh')
            activeMade.sshRead()
        time.sleep(8)
        activeMade.sshWrite('sudo -u root -i')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC200110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC204110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC208110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC20C110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC210110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC214110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC218110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('devmem 0xFC21C110 32 0x00001300')
        activeMade.sshRead()
        activeMade.sshWrite('cd /var/tmp/\n')
        activeMade.sshRead()




        return activeMade


    def Set_Switch(self, x, y, points):
        SW_path = Switch_S46()
        SW_path.openAll()
        if points[y] == 50:
            path = 0
        elif points[y] == 52:
            path = 1
        elif points[y] == 54:
            path = 2
        elif points[y] == 56:
            path = 3


        if x == 0:
            SW_path.closeChannel(path+1)

        elif x == 1:
            SW_path.closeChannel(path + 5)
            if y > 1:
                SW_path.closeChannel(29)
                print('Relay B Enabled')

        elif x == 2:
            SW_path.closeChannel(path + 9)
            SW_path.closeChannel(29)
            print('Relay B Enabled')

        elif x == 3:
            if path == 1:
                SW_path.closeChannel(31)
                print('R6NC->R7NO')
            elif path == 2:
                SW_path.closeChannel(30)
                print('R6NO->R8NC')
            elif path == 3:
                SW_path.closeChannel(30)
                SW_path.closeChannel(32)
                print('R6NO->R8NO')
            else:
                print('R6NC->R7NC')
        time.sleep(2)

    def Set_SigGen(self,x,y,points,Power,freq):


        if x == 3:
            Amp = Agilent_SigGen_MXA()
        else:
            Amp = Agilent_SigGen_PSG()

        Amp.turnOuputON()
        Amp.setPowerdBm(Power)
        Amp.setFrequency(freq)
        Amp.turnOuputON()
        time.sleep(1)




    def Set_SigGen_IIP3(self,Power,dist,cen_freq):
        C1 = 4.5
        C2 = 4.5
        MXA = Agilent_SigGen_MXA()
        PSG = Agilent_SigGen_PSG()
        MXA.setPowerdBm(Power+C1)
        PSG.setPowerdBm(Power+C2)
        MXA.setFrequency(cen_freq - dist / 2)
        PSG.setFrequency(cen_freq + dist / 2)
        MXA.turnOuputON()
        PSG.turnOuputON()

    def Set_Made_Off(self,x,IIP3,activeMade):

        SW_path = Switch_S46()
        if IIP3 == True:
            MXA = Agilent_SigGen_MXA()
            PSG = Agilent_SigGen_PSG()
            MXA.turnOuputOFF()
            PSG.turnOuputOFF()
            SW_path.openAll()
        else:
            if x == 3:
                Amp = Agilent_SigGen_MXA()
            else:
                #Amp = Agilent_SigGen_ESG()
                Amp = Agilent_SigGen_PSG()

            SW_path.openAll()
            Amp.turnOuputOFF()

        activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_SHUTDOWN.sh')
        activeMade.sshRead()
        time.sleep(5)
        print('FRMON SHUTDOWN')
        activeMade.SSHClose()
        time.sleep(3)


    def Set_Test_Off(self, x, IIP3):

        SW_path = Switch_S46()
        if IIP3 == True:
            MXA = Agilent_SigGen_MXA()
            PSG = Agilent_SigGen_PSG()
            MXA.turnOuputOFF()
            PSG.turnOuputOFF()
            SW_path.openAll()
        else:
            if x == 3:
                Amp = Agilent_SigGen_MXA()
            else:
                Amp = Agilent_SigGen_ESG()

            SW_path.openAll()
            Amp.turnOuputOFF()




