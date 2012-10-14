import pyaudio, array, math

p = pyaudio.PyAudio()
stream = p.open(rate=44100, channels=1, format=pyaudio.paFloat32, output=True)
stream.write(array.array('f',
    (.25 * math.sin(i / 10.) for i in range(44100))).tostring())
stream.close()
p.terminate()
