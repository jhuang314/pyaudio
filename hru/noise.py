import pyaudio, array, math, wave

RATE=44100
p = pyaudio.PyAudio()
stream = p.open(rate=RATE, channels=1, format=pyaudio.paFloat32, output=True)
# 10k = 4000000.0
#stream.write(array.array('f',
#    (0.20 * math.sin(i * 5000000.0) for i in range(RATE * 5))).tostring())
stream.write(array.array('f',
    (1. * math.sin(2.843*i) for i in range(RATE * 50))).tostring())
#stream.write(array.array('f',
#    (1 * math.sin(.5*i) for i in range(RATE * 50))).tostring())
#f = wave.open('output.wav', 'rb')
#stream = p.open(rate=44100, channels=1, format=pyaudio.paInt16, output=True)
#wave = array.array('f', (.25 * math.sin(i / 10.) for i in range(44100))).tostring()
print "GOING!"

#data = f.readframes(1024)
#while data != '':
    #print "one!"
#    stream.write(data)
#    data = f.readframes(1024)

stream.close()
p.terminate()

