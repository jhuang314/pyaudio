import pyaudio
import sys

chunk = 256
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS, 
                rate = RATE, 
                input = True,
                output = True,
		input_device_index = 0,
                frames_per_buffer = chunk)

print "* recording"
for i in range(0, 44100 / chunk * RECORD_SECONDS):
    try:
	data = stream.read(chunk)
    except IOError as ex:
	if ex[1] != pyaudio.paInputOverflowed:
	    raise
	data = '\x00' * chunk  # or however you choose to handle it, e.g. return None    range(0, 44100 / chunk * RECORD_SECONDS):
    # check for silence here by comparing the level with 0 (or some threshold) for 
    # the contents of data.
    # then write data or not to a file
    stream.write(data, chunk)

print "* done"

stream.stop_stream()
stream.close()
p.terminate()
