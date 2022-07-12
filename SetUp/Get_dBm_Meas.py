
import numpy as np
import scipy as sp
import math

from matplotlib import pyplot as plt
from mpldatacursor import datacursor
from scipy import signal



#from CapturePlot import Conv_dBm, adc_gain, dec_fil, sample_rate, pow_scale, pow_fs, cen_freq
#from CapturePlot import myformatter


class Get_dBm_Meas:
    def __init__(self):
        self.adc_gain = 0.0  # 0 dB gain
        self.sample_rate = 245.76e6
        self.dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        self.adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        self.Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
        self.cen_freq = 3840e6


    def add_Gain_Meas(self, capture_file,cen_freq,g_file_name):
        adc_gain = self.adc_gain
        sample_rate = self.sample_rate
        dec_fil = self.dec_fil  # decimation filter loss (/6 decimation filter);
        adc_bits = self.adc_bits  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = self.Conv_dBm # 0 dBFS power in dBm (before the input match at balun output).
        cen_freq = cen_freq
        path = capture_file
        capture_file = open(capture_file, 'r')
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

        pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex)) ** 2) / pow_fs)
        Pow_dBm_t = pow_dBfs_t + Conv_dBm
        Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil

        spec = np.fft.fftshift(np.fft.fft(data_complex_w))
        spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm

        Peak_pow = max(spec_dBm)
        Peak_pow_in = Peak_pow - adc_gain + dec_fil
        f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
        spec_dBml = np.ndarray.tolist(spec_dBm)
        peak_ind = np.argmax(spec_dBml)
        fmax = f[peak_ind] * 1e-6
        pmax = spec_dBm[peak_ind]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(f * 1e-6, spec_dBml)
        plt.grid(True)

        plt.axis([(cen_freq + -sample_rate/2) / 1e6, (cen_freq + sample_rate/2) / 1e6, -120, 10])
        plt.title('ADC Capture')
        plt.xlabel('Freq [MHz]')
        plt.ylabel('Input Power [dBm]')
        peak_ind = np.argmax(spec_dBml)

        fmax = f[peak_ind] * 1e-6

        pmax = spec_dBm[peak_ind]

        text1 = "freq={:.3f}, Power={:.3f}".format(fmax, pmax)
        ax.annotate(text1, xy=(fmax, pmax), xytext=(fmax, pmax + 10),
                    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90"), )

        plt.savefig(path + '.png')
        plt.close()
        print('pmax = {}'.format(str(pmax)))
        print('data_i max = {}'.format(str(max(data_i))))
        print('data_q max  = {}'.format(str(max(data_i))))


        return peak_ind,fmax,pmax,max(data_i),max(data_q)

    def add_IP3_Meas(self, capture_file, dist, file_path, Made, Pipe):
        adc_gain = 0.0  # 0 dB gain
        sample_rate = 245.76e6
        dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
        cen_freq = 3840e6
        capture_file = open(capture_file, 'r')
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

        pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex_w)) ** 2) / pow_fs)
        Pow_dBm_t = pow_dBfs_t + Conv_dBm
        Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil

        spec = np.fft.fftshift(np.fft.fft(data_complex_w))
        spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm
        spec_dBml = np.ndarray.tolist(spec_dBm)
        Peak_pow = max(spec_dBm)
        Peak_pow_in = Peak_pow - adc_gain + dec_fil
        f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
        points = int(len(spec_dBm))
        f_apart = sample_rate / points
        space = dist
        fr1 = cen_freq - (space * 1.25)
        fr2 = cen_freq + (space * 1.25)
        fr3 = cen_freq - (1.75 * space)
        fr4 = cen_freq + (1.75 * space)

        point1 = int((fr1 - f[0]) / f_apart)
        point2 = int((fr3 - f[0]) / f_apart)
        point3 = int((fr2 - f[0]) / f_apart)
        point4 = int((fr4 - f[0]) / f_apart)

        x1 = point2 + np.argmax(spec_dBml[int(point2):int(point1)])
        x2 = point3 + np.argmax(spec_dBml[int(point3):int(point4)])

        half = int(len(spec_dBm) / 2)
        h1 = spec_dBml[0:half - 1]
        h2 = spec_dBm[half:points]

        ip1 = spec_dBml[int(point2):int(point1)]
        ip2 = spec_dBm[int(point4):int(point3)]

        fh1max = f[np.argmax(h1)]

        fh2max = f[np.argmax(h2) + half]

        fip1max = f[x1]

        fip2max = f[x2]

        ph1max = spec_dBml[np.argmax(h1)]
        ph2max = spec_dBml[np.argmax(h2) + half]
        pip1max = spec_dBml[x1]
        pip2max = spec_dBml[x2]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(f * 1e-6, spec_dBml)
        plt.grid(True)
        plt.axis([(cen_freq) / 1e6, (cen_freq + 20e6) / 1e6, -120, 10])
        plt.title('ADC Capture')
        plt.xlabel('Freq [MHz]')
        plt.ylabel('Input Power [dBm]')
        peak_ind = np.argmax(spec_dBml)
        fmax = f[peak_ind] * 1e-6

        pmax = spec_dBm[peak_ind]
        text1 = "freq={:.3f}, Power={:.3f}".format(fmax, pmax)
        ax.annotate(text1, xy=(fmax, pmax), xytext=(fmax, pmax + 10),
                    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90"), )
        print(file_path + '.png')
        plt.savefig(file_path + '.png')


        return peak_ind,fmax,pmax, fh1max, ph1max, fh2max, ph2max, fip1max, pip1max, fip2max, pip2max

    def add_Iso_Meas(self, capture_file, peak_ind,cen_freq):
        adc_gain = 0.0  # 0 dB gain
        sample_rate = 245.76e6
        dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).

        capture_file = open(capture_file, 'r')
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

        pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex)) ** 2) / pow_fs)
        Pow_dBm_t = pow_dBfs_t + Conv_dBm
        Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil

        spec = np.fft.fftshift(np.fft.fft(data_complex_w))
        spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm

        Peak_pow = max(spec_dBm)
        Peak_pow_in = Peak_pow - adc_gain + dec_fil
        f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
        spec_dBml = np.ndarray.tolist(spec_dBm)
        #peak_ind = np.argmax(spec_dBml)
        f_iso = f[peak_ind] * 1e-6
        p_iso = spec_dBm[peak_ind]
        return f_iso,p_iso

    def add_NF_AVG(self, capture_file):
        adc_gain = 0.0  # 0 dB gain
        sample_rate = 245.76e6
        dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
        cen_freq = 3840e6
        capture_file = open(capture_file, 'r')
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

        def myformatter(**kwarg):
            label = '({x:.2f}, {y:.2f})'.format(**kwarg)
            return label

        pow_fs = float((((2 ** (adc_bits - 1)) - 1)) ** 2)
        pow_scale = pow_fs * samp_length ** 2

        pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex)) ** 2) / pow_fs)
        Pow_dBm_t = pow_dBfs_t + Conv_dBm
        Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil
        print('ADC Input Power (dBm), time domain = ', Pow_dBm_t_in)
        spec = np.fft.fftshift(np.fft.fft(data_complex))
        spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm

        Peak_pow = max(spec_dBm)
        Peak_pow_in = Peak_pow - adc_gain + dec_fil
        f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
        spec_dBml = np.ndarray.tolist(spec_dBm)
        peak_ind = np.argmax(spec_dBml)
        fmax = f[peak_ind] * 1e-6
        pmax = spec_dBm[peak_ind]
        points = int(len(spec_dBm))
        BW = max(f) - min(f)
        f_apart = BW / points
        space = 20e6
        fr1 = cen_freq - 5e6
        fr2 = cen_freq + 5e6


        point1 = int((fr1 - f[0]) / f_apart)
        point2 = int((fr2 - f[0]) / f_apart)
        spec = spec_dBml[int(point1):int(point2)]
        freq = f[int(point1):int(point2)]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(freq * 1e-6, spec)
        plt.grid(True)
        plt.axis([(cen_freq + -sample_rate / 2) / 1e6, (cen_freq + sample_rate / 2) / 1e6, -120, 10])
        plt.title('ADC Capture')
        plt.xlabel('Freq [MHz]')
        plt.ylabel('Input Power [dBm]')
        peak_ind = np.argmax(spec)


        return freq,spec

    def add_IP3_Meas_AVG(self, capture_file, dist, file_path, Made, Pipe, data_set,num):
        adc_gain = 0.0  # 0 dB gain
        sample_rate = 245.76e6
        dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
        cen_freq = 3840e6
        # data_set = ['Made0_50_IIP3_num0.txt','Made0_50_IIP3_num1.txt','Made0_50_IIP3_num2.txt']
        # file_path = 'C:\\Users\\eryoung\\Desktop\\Captures\\IIP3\\'
        # dist = 1e6
        # num = 3

        plot_only = "True"
        data_sum = []
        adc_gain = 0.0  # 0 dB gain
        sample_rate = 245.76e6
        dec_fil = 0.0  # decimation filter loss (/6 decimation filter);
        adc_bits = 19  # ADC is 14 bits but ouput is mapped to 1.5.18 format
        Conv_dBm = -10  # 0 dBFS power in dBm (before the input match at balun output).
        cen_freq = freq = 3840e6
        spec_av = {}

        for l in range(0, len(data_set)):

            capture_file = open(r"C:\Users\eryoung\Desktop\Captures\IIP3\CONT\{}".format(data_set[l]), "r")
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
            pow_dBfs_t = 10 * math.log10(np.mean((abs(data_complex_w)) ** 2) / pow_fs)
            Pow_dBm_t = pow_dBfs_t + Conv_dBm
            Pow_dBm_t_in = Pow_dBm_t - adc_gain + dec_fil
            # print('ADC Input Power (dBm), time domain = ', Pow_dBm_t_in)
            # spec = np.fft.fftshift(np
            # .fft.fft(data_complex))
            spec = np.fft.fftshift(np.fft.fft(data_complex_w))

            spec_dBm = 10 * np.log10(abs(spec ** 2 / pow_scale)) + Conv_dBm

            spec_av['spec{}'.format(l)] = (10 ** (spec_dBm / 10)) / 1000

            sl = len(spec_dBm)

        data_spec = [0] * sl
        spec_sum = [0] * sl

        for x in range(0, sl):
            for y in range(0, len(data_set)):

                z = spec_av.get('spec{}'.format(y))

                data_spec[x] = data_spec[x] + z[x]

                if y == len(data_set) - 1:
                    data_spec[x] = data_spec[x] / num
                    # d_av = np.average(data_spec)
                    spec_sum[x] = data_spec[x]
                    data_spec[x] = 10 * np.log10(data_spec[x] * 1000)
        spec_x = np.array(data_spec)
        # f = np.linspace(cen_freq + (-BW / 2), cen_freq + (BW / 2), len(spec_dBm))
        spec_dBml = np.ndarray.tolist(spec_x)

        def myformatter(**kwarg):
            label = '({x:.2f}, {y:.2f})'.format(**kwarg)
            return label

        # spec_dBm = 10.0*(math.fabs(spec / pow_scale * spec)) + Conv_dBm
        Peak_pow = max(spec_dBm)
        Peak_pow_in = Peak_pow - adc_gain + dec_fil

        f = np.linspace(cen_freq + (-sample_rate / 2), cen_freq + (sample_rate / 2), len(spec_dBm))
        points = int(len(spec_dBm))
        f_apart = sample_rate / points
        space = dist
        fr1 = cen_freq - (space * 1.25)
        fr2 = cen_freq + (space * 1.25)
        fr3 = cen_freq - (1.75 * space)
        fr4 = cen_freq + (1.75 * space)

        point1 = int((fr1 - f[0]) / f_apart)
        point2 = int((fr3 - f[0]) / f_apart)
        point3 = int((fr2 - f[0]) / f_apart)
        point4 = int((fr4 - f[0]) / f_apart)

        x1 = point2 + np.argmax(spec_dBml[int(point2):int(point1)])
        x2 = point3 + np.argmax(spec_dBml[int(point3):int(point4)])

        half = int(len(spec_dBm) / 2)
        h1 = spec_dBml[0:half - 1]
        h2 = spec_dBm[half:points]

        ip1 = spec_dBml[int(point2):int(point1)]
        ip2 = spec_dBm[int(point4):int(point3)]

        fh1max = f[np.argmax(h1)]

        fh2max = f[np.argmax(h2) + half]

        fip1max = f[x1]

        fip2max = f[x2]

        ph1max = spec_dBml[np.argmax(h1)]
        ph2max = spec_dBml[np.argmax(h2) + half]
        pip1max = spec_dBml[x1]
        pip2max = spec_dBml[x2]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line, = ax.plot(f * 1e-6, spec_dBml)
        plt.grid(True)
        plt.axis([(cen_freq + -dist * 2) / 1e6, (cen_freq + dist * 2) / 1e6, -120, 10])
        plt.title('ADC Capture')
        plt.xlabel('Freq [MHz]')
        plt.ylabel('Input Power [dBm]')
        peak_ind = np.argmax(spec_dBml)
        fmax = f[peak_ind] * 1e-6

        pmax = spec_dBm[peak_ind]
        text1 = "freq={:.3f}, Power={:.3f}".format(fmax, pmax)
        ax.annotate(text1, xy=(fmax, pmax), xytext=(fmax, pmax + 10),
                    arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90"), )
        plt.savefig(file_path + 'avgplot.png')
        plt.close()
        return peak_ind,fmax,pmax, fh1max, ph1max, fh2max, ph2max, fip1max, pip1max, fip2max, pip2max
