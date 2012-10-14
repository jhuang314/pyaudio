""" Record a few seconds of audio and save to a WAVE file. """
from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
from scipy import *
from pylab import *
import numpy as np
import pyaudio
import matplotlib
import wave
import sys

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
#RECORD_SECONDS = 0.1

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)

print "* recording"
all = []
#for i in range(0, RATE / chunk * RECORD_SECONDS):
for i in range(0, 50): # ~120ms
    data = stream.read(chunk)
    all.append(data)

print "* done recording"

data = ''.join(all)
audio = np.fromstring(data, dtype=np.short)
audio.shape = (audio.shape[0], 1)
#print audio.shape

audio = np.nan_to_num(audio) / 32768.0;
fmax = RATE / 2
audio_size = len(audio)
audio_time = float(audio_size) / float(RATE)
print "%d samples @ %dHz, duration = %f seconds" % (audio_size, RATE, audio_time)
t = linspace(0, audio_time, audio_size);
figure(1)
plot(t, audio)
title('Time-Domain of Signal')


ft =  rfft(audio)
mgft = abs(ft)
#df = fmax/float(audio_size/2)
f = linspace(0, fmax, audio_size/2 + 1)

print f

figure(2)
plot(f, mgft[0:(audio_size/2+1)])
title('Fourier-Domain Magnitude of Signal')

#freq = 22000
#print f[freq]
#print mgft[freq]
sum = 0
#for i in range(RATE/2, int(RATE/1.8)):
#    sum += mgft[i]

#print "sum is at %d" % (sum)

#print f[RATE/2]
#print f[RATE/1.8]

show()


#
stream.close()
p.terminate()
