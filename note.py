import pyaudio, array, math, wave, sys, os

chunk = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "testNote.wav"
FREQ = 2000

try:
    os.remove("./" + WAVE_OUTPUT_FILENAME)
except OSError:
    pass
except:
    print "shit!"


p = pyaudio.PyAudio()
stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, output=True)
data = array.array('f',
    (.25 * math.sin(32 * 3.14 * FREQ * i / 1.) for i in range(RATE))).tostring()
stream.write(data)

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(data)
wf.close()

stream.close()
p.terminate()
