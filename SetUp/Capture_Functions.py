import time

from matplotlib import pyplot as plt

from SetUp.Excel import Excel
from SetUp.Get_dBm_Meas import Get_dBm_Meas
from SetUp.SshInterface import SshInterface
from SetUp.Set_Up import Set_Up



class Captures:


    def Gain(self,Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power,Temp,Offset,activeMade,cen_freq,num_cap):

        for num in range(0, num_cap):
            file_name = 'Made{}_{}_num{}.txt'.format(str(Made[x]), str(Cap_Point[y]),str(num))
            activeMade.sshWrite(
                'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]),file_name))
            activeMade.sshRead()
            time.sleep(3)

        data_avg = []
        for num in range(0,num_cap):
            file_name = 'Made{}_{}_num{}.txt'.format(str(Made[x]), str(Cap_Point[y]),str(num))
            for z in range(0, 10):
                try:

                    activeMade.getFile('/var/tmp/{}'.format(file_name),gain_file_path)
                except:
                    print('try again')
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]),file_name))
                    activeMade.sshRead()
                    time.sleep(2)
            data_avg.append(file_name)
        ex = Excel()
        ex.Add_Gain_data(excel_file_path, Cap_Point[y], Made[x],gain_file_path, Power,Offset, Temp,cen_freq,file_name,num_cap,data_avg)


    def Flatness(self,Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power, Temp,Offset,freq,activeMade,cen_freq,g_file_name,num,data_set):

        activeMade.sshWrite(
            'sudo ./capture_ul -a {} -l 262144 /var/tmp{}'.format(str(Cap_Point[y]), g_file_name))
        activeMade.sshRead()
        for zp in range(0, 10):
            try:
                time.sleep(1)
                activeMade.getFile('/var/tmp/{}'.format(g_file_name),
                                   gain_file_path)
            except:
                print('try again')
                activeMade.sshWrite(
                    'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]),g_file_name))
                activeMade.sshRead()
                time.sleep(2)
        data_set.append(g_file_name)
        ex = Excel()
        ex.Add_Flat_Data(excel_file_path, Cap_Point[y], Made[x],
                             gain_file_path + g_file_name, Power, Offset, Temp,cen_freq,g_file_name,num,data_set)

    def P1dB(self,Made,x,y,Cap_Point,excel_file_path,gain_file_path,Power,Temp,Offset,freq,activeMade,Set,cen_freq,g_file_name,num,data_set,points,setPower):
        time.sleep(5)
        for pwr in range(0, points):
            Set.Set_SigGen(x, y, Cap_Point, Power + Offset[(4 * x) + (y)], freq)
            g_file_name = 'Made{}_{}_pwr{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(Power))
            activeMade.sshWrite(
                'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), str(g_file_name)))
            activeMade.sshRead()
            print('Sent capture_ul')
            Power = Power + 1
            time.sleep(2)
        Power = setPower
        time.sleep(5)
        pwrIn = []
        pwrOut = []
        for pwr in range(0, points):
            g_file_name = 'Made{}_{}_pwr{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(Power))
            activeMade.getFile('/var/tmp/{}'.format(str(g_file_name)),
                               gain_file_path)
            sl_found = False
            ex = Excel()
            pOut = ex.Add_P1dB_data(excel_file_path, Cap_Point[y], Made[x],
                                    gain_file_path + 'Made{}_{}_pwr{}.txt'.format(str(Made[x]), str(Cap_Point[y]),
                                                                                  str(Power)), Power,
                                    Offset[y], Temp,cen_freq,g_file_name,num,data_set)
            pwrIn.append(Power)
            pwrOut.append(pOut)

            p1x = 0
            if pwr == points - 1:
                m = (pwrOut[9] - pwrOut[4]) / 5
                b = pwrOut[5] - m * pwrIn[5]
                slope = []
                pin_slope = []
                pout_slope = []
                for sl in range(0, points):

                    slope.append(m * pwrIn[sl] + b)
                    pin_slope.append(pwrIn[sl])
                    pout_slope.append(slope[sl])
                    slope[sl] = abs(slope[sl] - pwrOut[sl])
                    if slope[sl] > 1 and pin_slope[sl] > -35:
                        p1x = pwrIn[sl - 1]
                        p1y = slope[sl - 1]
                        p2y = pwrOut[sl - 1]
                        print("P1dB = {}".format(str(p1x)))
                        sl_found = True
                        break
            ex.Add_P1dB_Point(excel_file_path, Cap_Point[y], Made[x],gain_file_path, p1x)

            Power = Power + 1

        plt.plot(pwrIn, pwrOut)
        plt.plot(pin_slope, pout_slope, "--")
        plt.plot(p1x, p1y)

        plt.plot(p1x, p2y)

        plt.grid(True)
        plt.title('P1 dB Data Made {}'.format(str(Made[x])))
        plt.legend(['Pipe {}'.format(str(Cap_Point[y]))])
        plt.ylim(min(pwrOut) - 3, max(pwrOut) + 3)
        plt.xlim(min(pwrIn) - 3, max(pwrIn) + 3)
        plt.xlabel('Pin (dBm)')
        plt.ylabel('Pout (dBm)')
        plt.savefig(gain_file_path + 'Made{}_{}_P1dB.png'.format(str(Made[x]), str(Cap_Point[y])))
        plt.close()

    def ISO_Gain(self,Made,x,y,Cap_Point,excel_file_path,iso_file_path,Power,Temp,Offset,freq,activeMade,Set,cen_freq,num,data_set):
        file_name = 'Made{}_CP{}_Gain.txt'.format(str(Made[x]), str(Cap_Point[y]))
        activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /tmp/{}'.format(str(Cap_Point[y]), file_name))
        activeMade.sshRead()
        time.sleep(5)
        reset = 0
        for ga in range(0, 10):
            try:
                activeMade.getFile('/tmp/{}'.format(file_name), iso_file_path)
            except:
                print("No gain file yet")
                time.sleep(1)
                reset = reset + 1
                if reset > 4:
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a {} -l 262144 /tmp/{}'.format(str(Cap_Point[y]), file_name))
                    activeMade.sshRead()

                    reset = 0
        ex = Excel()
        Data = Get_dBm_Meas()
        Gain = Data.add_Gain_Meas(iso_file_path + file_name,cen_freq,file_name)
        peak_gain = Gain[0]
        ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                        iso_file_path + file_name, Power, Offset[y],
                        Temp, peak_gain, Made[x], Cap_Point[y],cen_freq)
        if Cap_Point[y] != 50:
            activeMade.sshWrite(
                'sudo ./capture_ul -a 50 -l 262144 /tmp/Made{}_CP50_IP{}.txt'.format(str(Made[x]),
                                                                                     str(Cap_Point[y])))
            activeMade.sshRead()
            time.sleep(1)
            iso_file = 'Made{}_CP50_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y]))
            for ga in range(0, 10):
                try:
                    time.sleep(1)
                    activeMade.getFile('/tmp/{}'.format(iso_file), iso_file_path)
                except:
                    print("No gain file yet")
                    time.sleep(1)
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a 50 -l 262144 /tmp/Made{}_CP50_IP{}.txt'.format(str(Made[x]),
                                                                                             str(Cap_Point[y])))
                    activeMade.sshRead()
            ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                            iso_file_path + 'Made{}_CP50_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y])), Power,
                            Offset[y],
                            Temp, peak_gain, Made[x], 50,cen_freq)


        if Cap_Point[y] != 52:
            activeMade.sshWrite(
                'sudo ./capture_ul -a 52 -l 262144 /tmp/Made{}_CP52_IP{}.txt'.format(str(Made[x]),
                                                                                     str(Cap_Point[y])))
            activeMade.sshRead()
            time.sleep(1)
            iso_file = 'Made{}_CP52_IP{}.txt'.format(str(Made[x]),str(Cap_Point[y]))
            for ga in range(0, 10):
                try:
                    time.sleep(1)
                    activeMade.getFile('/tmp/{}'.format(iso_file), iso_file_path)
                except:
                    print("No gain file yet")
                    time.sleep(1)
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a 52 -l 262144 /tmp/Made{}_CP52_IP{}.txt'.format(str(Made[x]),
                                                                                             str(Cap_Point[y])))
                    activeMade.sshRead()
            ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                            iso_file_path + 'Made{}_CP52_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y])), Power,
                            Offset[y],
                            Temp, peak_gain, Made[x], 52,cen_freq)
        if Cap_Point[y] != 54:
            activeMade.sshWrite(
                'sudo ./capture_ul -a 54 -l 262144 /tmp/Made{}_CP54_IP{}.txt'.format(str(Made[x]),
                                                                                     str(Cap_Point[y])))
            activeMade.sshRead()
            time.sleep(1)
            iso_file = 'Made{}_CP54_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y]))
            for ga in range(0, 10):
                try:
                    time.sleep(1)
                    activeMade.getFile('/tmp/{}'.format(iso_file), iso_file_path)
                except:
                    print("No gain file yet")
                    time.sleep(1)
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a 54 -l 262144 /tmp/Made{}_CP54_IP{}.txt'.format(str(Made[x]),
                                                                                             str(Cap_Point[y])))
                    activeMade.sshRead()
            ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                            iso_file_path + 'Made{}_CP54_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y])), Power,
                            Offset[y],
                            Temp, peak_gain, Made[x], 54,cen_freq)
        if Cap_Point[y] != 56:
            activeMade.sshWrite(
                'sudo ./capture_ul -a 56 -l 262144 /tmp/Made{}_CP56_IP{}.txt'.format(str(Made[x]),
                                                                                     str(Cap_Point[y])))
            activeMade.sshRead()
            time.sleep(1)
            iso_file = 'Made{}_CP56_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y]))
            for ga in range(0, 10):
                try:
                    time.sleep(1)
                    activeMade.getFile('/tmp/{}'.format(iso_file), iso_file_path)
                except:
                    print("No gain file yet")
                    time.sleep(1)
                    activeMade.sshWrite(
                        'sudo ./capture_ul -a 56 -l 262144 /tmp/Made{}_CP56_IP{}.txt'.format(str(Made[x]),
                                                                                             str(Cap_Point[y])))
                    activeMade.sshRead()
            ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                            iso_file_path + 'Made{}_CP56_IP{}.txt'.format(str(Made[x]), str(Cap_Point[y])), Power,
                            Offset[y],
                            Temp, peak_gain, Made[x], 56,cen_freq)
        return peak_gain



    def ISO_Meas(self, Made, x, y, Cap_Point, excel_file_path, iso_file_path, Power, Temp, Offset, freq, activeMade,
                 Set, cen_freq, num, data_set,ISO_LIST,m,peak_gain):
        ex = Excel()
        if Made[x] == ISO_LIST[m]:
            print('Back here again')
        else:
            activeMade = Set.Made_Setup(ISO_LIST[m])
            for y in range(0,len(Cap_Point)):
                Set.Set_Switch(x,y,Cap_Point)
                Set.Set_SigGen(x,y,Cap_Point,Power + Offset[(4 * x) + (y)], freq)
                activeMade.sshWrite(
                    'sudo ./capture_ul -a 50 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP50.txt'.format(str(Made[x]),
                                                                                                  str(Cap_Point[y]),
                                                                                                  ISO_LIST[m]))
                activeMade.sshRead()
                time.sleep(1)
                activeMade.sshWrite(
                    'sudo ./capture_ul -a 52 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP52.txt'.format(str(Made[x]),
                                                                                                  str(Cap_Point[y]),
                                                                                                  ISO_LIST[m]))
                activeMade.sshRead()
                time.sleep(1)

                activeMade.sshWrite(
                    'sudo ./capture_ul -a 54 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP54.txt'.format(str(Made[x]),
                                                                                                  str(Cap_Point[y]),
                                                                                                  ISO_LIST[m]))
                activeMade.sshRead()
                time.sleep(1)

                activeMade.sshWrite(
                    'sudo ./capture_ul -a 56 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP56.txt'.format(str(Made[x]),
                                                                                                  str(Cap_Point[y]),
                                                                                                  ISO_LIST[m]))
                activeMade.sshRead()
                time.sleep(1)
                reset = 0
                for b in range(0, 10):

                    try:
                        activeMade.getFile(
                            '/tmp/Made{}_CP{}_IPMade{}_CP50.txt'.format(str(Made[x]), str(Cap_Point[y]),
                                                                        ISO_LIST[m]),
                            'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\')

                        time.sleep(3)
                        break
                    except:
                        print('No file yet')
                        reset = reset + 1
                        time.sleep(4)
                        activeMade.sshWrite(
                            'sudo ./capture_ul -a 50 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP50.txt'.format(
                                str(Made[x]),
                                str(Cap_Point[y]),
                                ISO_LIST[m]))
                        activeMade.sshRead()
                        time.sleep(1)

                        activeMade.sshWrite(
                            'sudo ./capture_ul -a 52 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP52.txt'.format(
                                str(Made[x]),
                                str(Cap_Point[y]),
                                ISO_LIST[m]))
                        activeMade.sshRead()
                        time.sleep(1)

                        activeMade.sshWrite(
                            'sudo ./capture_ul -a 54 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP54.txt'.format(
                                str(Made[x]),
                                str(Cap_Point[y]),
                                ISO_LIST[m]))
                        activeMade.sshRead()
                        time.sleep(1)

                        activeMade.sshWrite(
                            'sudo ./capture_ul -a 56 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP56.txt'.format(
                                str(Made[x]),
                                str(Cap_Point[y]),
                                ISO_LIST[m]))
                        activeMade.sshRead()
                        time.sleep(1)
                        if reset > 5:
                            activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_SHUTDOWN.sh')
                            activeMade.sshRead()
                            time.sleep(10)
                            activeMade.sshWrite('sudo frmonShellClient 127.0.0.1 2000 ./FRMON_CREATE.sh')
                            activeMade.sshRead()
                            time.sleep(20)
                            reset = 0
                            activeMade.sshWrite(
                                'sudo ./capture_ul -a 50 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP50.txt'.format(
                                    str(Made[x]),
                                    str(Cap_Point[y]),
                                    ISO_LIST[m]))
                            activeMade.sshRead()
                            time.sleep(1)

                            activeMade.sshWrite(
                                'sudo ./capture_ul -a 52 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP52.txt'.format(
                                    str(Made[x]),
                                    str(Cap_Point[y]),
                                    ISO_LIST[m]))
                            activeMade.sshRead()
                            time.sleep(1)

                            activeMade.sshWrite(
                                'sudo ./capture_ul -a 54 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP54.txt'.format(
                                    str(Made[x]),
                                    str(Cap_Point[y]),
                                    ISO_LIST[m]))
                            activeMade.sshRead()
                            time.sleep(1)

                            activeMade.sshWrite(
                                'sudo ./capture_ul -a 56 -l 262144 /tmp/Made{}_CP{}_IPMade{}_CP56.txt'.format(
                                    str(Made[x]),
                                    str(Cap_Point[y]),
                                    ISO_LIST[m]))
                            activeMade.sshRead()
                            time.sleep(1)

                activeMade.getFile(
                    '/tmp/Made{}_CP{}_IPMade{}_CP52.txt'.format(str(Made[x]), str(Cap_Point[y]), ISO_LIST[m]),
                    'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\')
                activeMade.getFile(
                    '/tmp/Made{}_CP{}_IPMade{}_CP54.txt'.format(str(Made[x]), str(Cap_Point[y]), ISO_LIST[m]),
                    'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\')
                activeMade.getFile(
                    '/tmp/Made{}_CP{}_IPMade{}_CP56.txt'.format(str(Made[x]), str(Cap_Point[y]), ISO_LIST[m]),
                    'C:\\Users\\eryoung\\Desktop\\Captures\\Isolation Measurements\\')
                ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                                iso_file_path + 'Made{}_CP{}_IPMade{}_CP50.txt'.format(str(Made[x]),
                                                                                       str(Cap_Point[y]),
                                                                                       str(ISO_LIST[m])), Power,
                                Offset[y],
                                Temp, peak_gain, ISO_LIST[m], 50,cen_freq)
                ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                                iso_file_path + 'Made{}_CP{}_IPMade{}_CP52.txt'.format(str(Made[x]),
                                                                                       str(Cap_Point[y]),
                                                                                       str(ISO_LIST[m])), Power,
                                Offset[y],
                                Temp, peak_gain, ISO_LIST[m], 52,cen_freq)
                ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                                iso_file_path + 'Made{}_CP{}_IPMade{}_CP54.txt'.format(str(Made[x]),
                                                                                       str(Cap_Point[y]),
                                                                                       str(ISO_LIST[m])), Power,
                                Offset[y],
                                Temp, peak_gain, ISO_LIST[m], 54,cen_freq)
                ex.Add_ISO_data(excel_file_path, Cap_Point[y], Made[x],
                                iso_file_path + 'Made{}_CP{}_IPMade{}_CP56.txt'.format(str(Made[x]),
                                                                                       str(Cap_Point[y]),
                                                                                       str(ISO_LIST[m])), Power,
                                Offset[y],
                                Temp, peak_gain, ISO_LIST[m], 56,cen_freq)



        return activeMade

    def NF(self, Made, x, y, Cap_Point, excel_file_path, gain_file_path, Power, Temp, Offset, freq, activeMade,
                 Set, cen_freq, num, data_set,BW,g_file_name):
        activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), g_file_name))
        activeMade.sshRead()
        for tries in range(0,10):
            try:
                activeMade.getFile('/var/tmp/{}'.format(g_file_name), gain_file_path)
            except:
                print('Not here yet')
                time.sleep(2)

        gm = Get_dBm_Meas()
        gain_meas = gm.add_Gain_Meas(gain_file_path + g_file_name,cen_freq,g_file_name)
        Gain = gain_meas[2] - Power

        Set.Set_Test_Off(x,IIP3=False)
        for num in range(0, num):
            file_name = 'Made{}_{}_num{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(num))
            activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
            activeMade.sshRead()
            time.sleep(1)
        time.sleep(2)
        data_avg = []
        for num in range(0, num):
            file_name = 'Made{}_{}_num{}.txt'.format(str(Made[x]), str(Cap_Point[y]), str(num))
            activeMade.getFile('/var/tmp/{}'.format(file_name), gain_file_path)
            data_avg.append(file_name)
        ex = Excel()
        ex.Add_NF_data(excel_file_path, Cap_Point[y], Made[x], gain_file_path, Power, Offset[y], Temp, data_avg, num, BW, Gain,
                       freq)

    def Cap(self,x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq):
        file_name = 'Made{}_{}_-60.txt'.format(str(Made[x]),str(Cap_Point[y]))
        activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
        activeMade.sshRead()
        q = 0
        for q in range(0,10):
            try:
                time.sleep(1)
                activeMade.getFile('/var/tmp/{}'.format(file_name), cap_file_path)
                break
            except:
                activeMade.sshWrite(
                    'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
                activeMade.sshRead()
                time.sleep(1)
                print('no file yet')
        Get = Get_dBm_Meas()
        Get.add_Gain_Meas(cap_file_path+file_name,cen_freq,file_name)


    def Cap_IIP3(self,x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq,file_name,dist):

        activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
        activeMade.sshRead()
        for q in range(0,10):
            try:
                time.sleep(1)
                activeMade.getFile('/var/tmp/{}'.format(file_name), cap_file_path)
            except:
                activeMade.sshWrite(
                    'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
                activeMade.sshRead()
                time.sleep(1)
                print('no file yet')
        Get = Get_dBm_Meas()
        Get.add_IP3_Meas(cap_file_path+file_name,dist,cap_file_path+file_name,Made[x],Cap_Point[y])

    def Cap_ATT(self,x,y,Cap_Point,Made,activeMade,Set,cap_file_path,cen_freq,file_name,excel_file_path,gain_file_path,Power,g_file_name,row):
        if Cap_Point[y] == 50:
            channel = 1
        elif Cap_Point[y] == 52:
            channel = 3
        elif Cap_Point[y] == 54:
            channel = 2
        else:
            channel = 4



        activeMade.sshWrite('python3 Palau_Test_20220705.py -t RX_ATTget_{}'.format(str(channel)))
        activeMade.sshRead()
        time.sleep(2)
        ATTlogic = True

        activeMade.sshWrite('sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
        ATT = activeMade.sshRead()

        ATTpos = ATT.find('ATT =')
        print('position is for ATT' +str(ATTpos))
        while ATTlogic == True:
            if str(ATTpos) == '-1':
                activeMade.sshWrite('python3 Palau_Test_20220705.py -t RX_ATTget_{}'.format(str(channel)))
                activeMade.sshRead()
                time.sleep(2)
                activeMade.sshWrite(
                    'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
                ATT = activeMade.sshRead()

                ATTpos = ATT.find('ATT =')
                print('position is ' + str(ATTpos))
            else:
                ATTlogic = False

        activeMade.sshWrite('python3 Palau_Test_20220705.py -t RX_POWER_{}'.format(str(channel)))
        activeMade.sshRead()
        time.sleep(2)
        activeMade.sshWrite('python3 Palau_Test_20220705.py -t RX_POWER_{}'.format(str(channel)))
        Ppow = activeMade.sshRead()
        PowPos = Ppow.find('RX Power:')
        print('position is for POW' + str(PowPos))
        ATTvalue = ATT[ATTpos:ATTpos+15]
        PowValue = Ppow[PowPos:PowPos + 16]
        print(ATTvalue)
        for q in range(0,10):
            try:
                time.sleep(1)
                activeMade.getFile('/var/tmp/{}'.format(file_name), cap_file_path)
            except:
                activeMade.sshWrite(
                    'sudo ./capture_ul -a {} -l 262144 /var/tmp/{}'.format(str(Cap_Point[y]), file_name))
                activeMade.sshRead()
                time.sleep(1)
                print('no file yet')
        ex = Excel()
        ex.Add_ATT_data(excel_file_path,Cap_Point[y],Made[x],gain_file_path,Power,cen_freq,g_file_name,ATTvalue,row,PowValue)

