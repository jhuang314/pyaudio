from gevent import monkey; monkey.patch_all()
import gevent 
from gevent import Greenlet, GreenletExit
import socket
from transport import Transport
from messages import Message

game_host = 'ruslug.rutgers.edu'
game_port = 51234
nick = '22'

class Client(Greenlet):

    def __init__(self, host, port, nick):
	Greenlet.__init__(self)
	self.host = host
	self.port = port
	self.name = nick

    def _run(self):
	self.connect()
	if not self.auth():
	    self.exit("Could not connect to server")
	print("Auth successful")
	self.opponent = self.opponent_wait()
	self.start_wait()
	self.play()
    
    def wait(self, msg_type):
	"""
	Waits for a specific message type, then returns the received message
    	"""
	while True:
	    rec = self.transport.receive()
	    try:
		msg = Message.parse(rec)
	    except MessageError:
		continue
	    if msg.type == msg_type:
		return msg

    def opponent_wait(self):
	msg = self.wait('opponent')
	return msg.payload

    def start_wait(self):
	while True:
	    msg = self.wait('game')
	    if msg.payload == 'start':
		break
	
    def play(self):
	sensor = gevent.spawn(self.handle_punch)	
	sensor.join()

    def handle_punch(self):
	while True:
	    gevent.sleep(2)




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
            last2 = 0.
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
                input_max = max(input)
                input = input / float(input_max)
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
            
                sum = 0.
                # @50 22000, 25000
                # @5 2200, 2500
                # @4 1300, 1500
                #print f[1300]
                #print f[1500]
                #print f[1800]
                #print f[2200]
                #print f[2500]
                sum_d = 0.
            
                for i in range(2200, 2500):
                    sum += mgft[i]
                    if i > 2300:
                        sum_d += mgft[i]
            
                hitstr="""
#     #  ###  #######  
#     #   #      #     
#     #   #      #     
#######   #      #     
#     #   #      #     
#     #   #      #     
#     #  ###     #     
            
                """
                ratio = sum_d/sum
                #print sum
                if sum > 200:
                    #print "ratio: %f, sum: %f" % (ratio * 100 , sum)
                    last = ratio * 100
                    delta = last - last2
                    print "%f" % (delta)
                    last2 = last
                    #delta = ratio - last
                    
                    if abs(delta) > 6:
                        hit = hit + 1
                        print hitstr
                        print "Hits = %d" % (hit)
                        print "Sending punch"
                        self.transport.send(Message.punch().pack())
            
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
            
                #last = sum
                #print sum
                #print sum2
                #print "stability: %f, delta: %f, sum: %f" % (ratio * 100, ratio_d * 100, sum)
            
            
            
            stream.close()
            p.terminate()
    





	    print "sending punch"


#	    self.transport.send(Message.punch().pack())

    def exit(self, msg):
	print(msg)
	raise GreenletExit

    def connect(self):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((self.host, self.port))
	print dir(sock)
	self.transport = Transport(sock, (self.host, self.port))

    def auth(self):
	self.transport.send(Message.nick(self.name).pack())
	data = self.transport.receive()
	try:
	    msg = Message.parse(data)
	except MessageError:
	    return False
	if msg.type == 'auth' and msg.payload == 'success':
	    return True
	else:
	    return False

if __name__ == "__main__":
    client = Client(game_host, game_port, nick)
    client.start()
    client.join()

