from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
from scipy import *
from pylab import *
import numpy as np

rate, input = read('output.wav')
fmax = rate / 2
input_len = len(input)
input_time = float(input_len) / float(rate)
print "%d samples @ %dHz, duration = %f seconds" % (input_len, rate, input_time)
t = linspace(0, input_time, input_len);

figure(1)
plot(t, input)
plot
title('Time-Domain of Signal')


ft = rfft(input)
mgft = abs(ft)
df = fmax/float(input_len/2)
f = linspace(0, fmax, input_len/2 + 1)

figure(2)
plot(f, mgft[0:input_len/2+1])
title('Fourier-Domain Magnitude of Signal')


show()



