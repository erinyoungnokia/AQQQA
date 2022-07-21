# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 14:43:48 2022

@author: labuser
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import math
from mpldatacursor import datacursor
import os
import paramiko
from numpy import fft
from numpy.fft import fftshift
from scipy import signal
from scipy.fftpack import fft, fftshift
from scp import SCPClient
import ctypes as ctp


from scipy import signal

#from CapturePlot import adc_bits, Conv_dBm, adc_gain, dec_fil, cen_freq, sample_rate


class NF:


    def plot_NF(self, data_set, num,BW, Gain, Pipe,Made,file_path,freq):




       plot_only = "True"
       data_sum = []
       adc_gain = 0.0  # 0 dB gain
       sample_rate = 245.76e6
       dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
       adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
       Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
       cen_freq = freq
       spec_av = {}
       count = 0
       power_amp = 0
       for l in range(0,len(data_set)):

           capture_file = open(r"C:\Users\eryoung\Desktop\Captures\NF Measurements\{}".format(data_set[l]), "r")
           #Muhammad
           c_file = capture_file.readlines()
           capture_file.close()
           samp_length = len(c_file)
           data_i = np.zeros(samp_length)
           data_q = np.zeros(samp_length)
           data_ii = np.zeros(samp_length)
           data_qq = np.zeros(samp_length)
           i = 0
           for iq in c_file:
               data = iq.rstrip().lstrip()
               data = data[2:-4]
               I_h = data[:6] + '00'
               Q_h = data[6:] + '00'
               data_ii[i] = np.int(I_h, 16)
               if data_ii[i] > (2 ** 31 - 1):
                   data_i[i] = data_ii[i] - 2 ** 32
               else:
                   data_i[i] = data_ii[i]
                   data_qq[i] = np.int(Q_h, 16)
               if data_qq[i] > (2 ** 31 - 1):
                   data_q[i] = data_qq[i] - 2 ** 32
               else:
                   data_q[i] = data_qq[i]
               i += 1
           data_i = data_i / 256
           data_q = data_q / 256



           Wavg = np.mean(sp.signal.windows.flattop(samp_length))
           data_complex = [complex(data_i[i], data_q[i]) for i in range(0, samp_length)]
           data_complex_w = data_complex * sp.signal.windows.flattop(samp_length)
           data_complex_w = data_complex_w / Wavg
           data_complex = np.asarray(data_complex)
           pow_fs = float((((2 ** (adc_bits - 1)) - 1)) ** 2)
           pow_scale = pow_fs * samp_length ** 2
           # put date where data_complex was
           pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex)) ** 2) / pow_fs)
           Pow_dBm_t = pow_dBfs_t + Conv_dBm
           Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil
           #print('ADC Input Power (dBm), time domain = ', Pow_dBm_t_in)
           # spec = np.fft.fftshift(np
           # .fft.fft(data_complex))

           #Sushanth
           lines = c_file
           captureLength = samp_length
           dataQ = np.zeros(captureLength)
           dataI = np.zeros(captureLength)
           dataQ_FP = np.zeros(captureLength)
           dataI_FP = np.zeros(captureLength)
           indx = 0
           for line in lines:
               # print("line: %s" %(line))
               # temp = line
               line = line.rstrip().lstrip()
               line = line[2:-4]

               Istr = line[:6]
               # print("I: %s" %(Istr))
               Qstr = line[6:]
               # print("IQ: %s I: %s Q: %s" %(temp,Istr,Qstr))

               dataI[indx] = int(Istr, 16)

               dataQ[indx] = int(Qstr, 16)

               dataI_FP[indx] = self.convert2FixedPoint(Istr)
               dataQ_FP[indx] = self.convert2FixedPoint(Qstr)

               indx += 1
           # convert from 2's comp to signed int.  (uses NUMPY)

           dataI[dataI > pow(2, 19 - 1)] -= pow(2, 19)
           dataI = dataI.astype(int)

           dataQ[dataQ > pow(2, 19 - 1)] -= pow(2, 19)
           dataQ = dataQ.astype(int)
           d_complex = (dataI_FP + 1j * dataQ_FP)
           Wavg_s = np.mean(signal.flattop(samp_length))
           window = signal.flattop(samp_length)
           data_windowed = data_complex * window / Wavg
           data_windowed_fft = fftshift(fft(d_complex))

           spec = np.fft.fftshift(np.fft.fft(data_complex))



           Vp = .2
           voltage_amp = abs(data_windowed_fft/samp_length)
           power_amp = power_amp + ((voltage_amp * (Vp) / (2 ** (0.5))) ** 2) / 50
           count = count + 1



           spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm

           spec_av['spec{}'.format(l)] = (10 ** (spec_dBm/10))/1000

           sl = len(spec_dBm)

       Pavg = power_amp/count

       power_dbm = 10 * np.log10(Pavg * 1000)



       data_spec = [0]*sl
       spec_sum = [0]*sl

       for x in range(0,sl):
           for y in range(0,len(data_set)):

               z=spec_av.get('spec{}'.format(y))

               data_spec[x] = data_spec[x] + z[x]

               if y == len(data_set)-1:

                   data_spec[x] = data_spec[x]/num
                   #d_av = np.average(data_spec)
                   spec_sum[x] = data_spec[x]
                   data_spec[x] = 10 * np.log10(data_spec[x] * 1000)





       spec_x = np.array(data_spec)
       #f = np.linspace(cen_freq + (-BW / 2), cen_freq + (BW / 2), len(spec_dBm))
       spec_dBml = np.ndarray.tolist(spec_x)
       f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
       power_dbm = 10 * np.log10(Pavg * 1000)













       def myformatter(**kwarg):
           label = '({x:.2f}, {y:.2f})'.format(**kwarg)
           return label



       # spec_dBm = 10.0*(math.fabs(spec / pow_scale * spec)) + Conv_dBm
       Peak_pow = max(spec_dBm)
       Peak_pow_in = Peak_pow - adc_gain + dec_fil
       f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(Pavg))
       result = np.where((f >= freq - BW / 2) & (f <= freq + BW / 2))
       fmn = cen_freq - BW / 2
       fmx = cen_freq + BW / 2
       points = int(len(spec_dBm))
       f_apart = sample_rate / points
       p1 = int((fmn - f[0]) / f_apart)
       p2 = int((fmx - f[0]) / f_apart)

       power_BW = np.sum(Pavg[result])
       print('Power BW sum = {}'.format(str(power_BW)))
       power_BW_dBm = 10 * np.log10(power_BW * 1000)
       print('Power BW sum dBm = {}'.format(str(power_BW_dBm)))
       #power_dbm = 10 * np.log10(Pavg * 1000)
       psum = 0
       for xx in range(p1, p2):
           psum = psum + Pavg[xx]
       print('Psum = {}'.format(str(psum)))
       print('Psum dbm= {}'.format(str(10 * math.log10(psum * 1000))))




       sum = 0

       p_cent = int((cen_freq-f[0])/f_apart)
       p_cen = spec_sum[p_cent]
       p_cen_dbm = 10*math.log10(p_cen*1000)
       #print(10*math.log10(d_av))




       for sm in range(p1,p2+1):
           sum = sum + spec_sum[sm]

       log_sum = 10 * np.log10(sum * 1000)
       print(sum)
       print(log_sum)
       therm = -174+ 10*math.log10(BW)

       total = log_sum - Gain

       F = total - therm

        # f = np.linspace((-sample_rate / 2), (sample_rate / 2), len(spec_dBm))
       #spec_dBml = np.ndarray.tolist(spec_dBm)
       fig = plt.figure()
       ax = fig.add_subplot(111)
       line, = ax.plot(f * 1e-6, spec_dBml)
       plt.grid(True)
       plt.axis([(cen_freq + -BW / 2) / 1e6, (cen_freq + BW / 2) / 1e6, -120, 10])
       plt.title('ADC Capture')
       plt.xlabel('Freq [MHz]')
       plt.ylabel('Input Power [dBm]')
       peak_ind = np.argmax(spec_dBml)
       fmax = f[peak_ind] * 1e-6

       pmax = spec_dBm[peak_ind]







       # pow1 = spec_dBm[16051]
       # pow2 = spec_dBm[16723]
       # pow1s = spec_dBm[15379]
       # pow2s = spec_dBm[17395]
        ################################################################
       text1 = "freq={:.3f}, Power={:.3f}".format(fmax, pmax)
       ax.annotate(text1, xy=(fmax, pmax), xytext=(fmax, pmax + 10),
                    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90"), )

        # text2 = "freq={:.3f}, Power={:.3f}".format(3280, pow2)
        # ax.annotate(text2, xy=(3280,pow2),xytext=(3280+20, pow2-10), arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=135"),)

        # text1s = "freq={:.3f}, Power={:.3f}".format(3260, pow1s)
        # ax.annotate(text1s, xy=(3260,pow1s),xytext=(3260+20, pow1s+5), arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90"),)

        # text2s = "freq={:.3f}, Power={:.3f}".format(3290, pow2s)
        # ax.annotate(text2s, xy=(3290,pow2s),xytext=(3290+20, pow2s-10), arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=135"),)

       datacursor(display='multiple', draggable=True, formatter=myformatter)
       #plt.show()
       print(file_path + 'Made{}_Pipe{}.png'.format(str(Made),str(Pipe)))
       plt.savefig(file_path + 'Made{}_Pipe{}.png'.format(str(Made),str(Pipe)))
       return Gain, log_sum, therm, F

    def convert2FixedPoint(self,hexStr):
        #fixed point format

        Istr1 = "B20001"
        res = format(int(hexStr, 16), '0>24b')
        sign = int(res[0]) * (-1 ) * (2**5)  # sign
        integer = int(res[1:6], 2)  # integer
        frac = 0
        for i in range(6, 24):
            frac = frac + (int(res[i], 2) * (2 ** (5 - i)))
        # print(frac)
        num = sign + (integer + frac)
        # print(num)


        return num


