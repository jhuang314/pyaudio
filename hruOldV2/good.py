""" Record a few seconds of audio and save to a WAVE file. """
from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
from scipy import *
from pylab import *
import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import wave
import sys



last = 0.
cal = []
mean = 0.
std = 0.
hit = 0

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
#RECORD_SECONDS = 0.1
WAVE_FILENAME = '/tmp/ashfs/output.wav'

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)


init = True

while True:
    #print "* recording"
    all = []
    #for i in range(0, RATE / chunk * RECORD_SECONDS):
    i = 0
    while i < 5: # ~120ms
        try:
            data = stream.read(chunk)
            all.append(data)
            i = i + 1
        except:
            pass
        

    #print "* done recording"

    #print data[0]
    #print type(data[0])
    #print "%d" % ord(data[0])
    #audio = numpy.fromstring(data)
    #print type(audio)

    #audio.shape = (audio.shape[0], 1)
    #print audio.shape


    #f = scipy.fft(audio[:,0])


    # write data to WAVE file
    data = ''.join(all)
    wf = wave.open(WAVE_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    rate, input = read(WAVE_FILENAME)
    fmax = rate / 2
    input_len = len(input)
    input_time = float(input_len) / float(rate)
    #print "%d samples @ %dHz, duration = %f seconds" % (input_len, rate, input_time)
    t = linspace(0, input_time, input_len);

    ft = rfft(input)
    mgft = abs(ft)
    df = fmax/float(input_len/2)
    f = linspace(0, fmax, input_len/2 + 1)

    if init:
        plt.ion()
        fig = plt.figure()

        ax = fig.add_subplot(211)
        title('Time-Domain of Signal')
        tplot, = ax.plot(t, input)

        bx = fig.add_subplot(212)
        title('Fourier-Domain Magnitude of Signal')
        fplot, = bx.plot(f, mgft[0:input_len/2+1])

        init = False
    
    #plot(t, input)
    tplot.set_ydata(input)
    fplot.set_ydata(mgft[0:input_len/2+1])

    fig.canvas.draw()


    #show()

    sum = 0
    # @50 22000, 25000
    # @5 2200, 2500
    # @4 1300, 1500
    #print f[1300]
    #print f[1500]
    sum2 = 0
    sum_d = 0
    sum2_d = 0
    #print f[1800]
    #print f[2000]
    for i in range(2200, 2500):
        sum += mgft[i]

    for i in range(2400, 2500):
        sum_d += mgft[i]

    for i in range(1800, 2000):
        sum2 += mgft[i]

    for i in range(1950, 2000):
        sum2_d += mgft[i]


    #exit()

    hitstr="""
#     #  ###  #######  
#     #   #      #     
#     #   #      #     
#######   #      #     
#     #   #      #     
#     #   #      #     
#     #  ###     #     

    """
    ratio = sum2/sum
    ratio_d = (sum2_d + ratio * sum_d)/(sum2 + ratio * sum) 
    if sum > 10000000:
        #delta = ratio - last
        

        #if ratio > 7:
        #print sum
        #delta = last - sum;
        #if len(cal) < 21:
        #    cal.append(sum)
        #    print "Calibrating Delta = %f..." %(delta)
        #    if len(cal) == 21:
        #        mean = np.average(cal)
        #        std = np.std(cal)
        #        print "Done calibrating! STD=%f, MEAN=%f" % (std, mean)
        #        print cal
        #else:
        #    print "STD: %f" % (float(sum - mean)/std)
        #print "Delta (%f%%) : %f" % (sum/last * 100, delta);
        #if sum > 60000000:
        #    hit = hit + 1
        #    print hitstr
        #    print "Hits = %d" % (hit)
        last = ratio

    #last = sum
    #print sum
    #print sum2
    print "stability: %f, delta: %f, sum: %f" % (ratio * 100, ratio_d * 100, sum)



stream.close()
p.terminate()
