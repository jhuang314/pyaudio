from scipy import fft
import pyaudio
import wave
import sys
import os

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
TRIALS = 3

try:
    os.remove("./output.wav")
except OSError:
    pass
except:
    print "shit!"

    
p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

print "* recording"

all = []
for i in range(0, RATE / chunk * RECORD_SECONDS):
    try:
        data = stream.read(chunk)
    except IOError:
        pass
    all.append(data)

print "* done recording"
#print all[0]
stream.close()
p.terminate()

# write data to WAVE file
data = ''.join(all)
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(data)
# wf.close()




p = pyaudio.PyAudio()

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)

for c in chunks(data, chunk):
    stream.write(c)

stream.close()
p.terminate()

# wf = wave.open("output.wav", 'rb')

# p = pyaudio.PyAudio()

# # open stream
# stream = p.open(format =
#                 p.get_format_from_width(wf.getsampwidth()),
#                 channels = wf.getnchannels(),
#                 rate = wf.getframerate(),
#                 output = True)

# # read data
#data = wf.readframes(chunk)

# # play stream
# while data != '':
#     stream.write(data)
#     data = wf.readframes(chunk)

# stream.close()
# p.terminate()
