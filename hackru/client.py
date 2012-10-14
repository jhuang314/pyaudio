from gevent import monkey; monkey.patch_all()
import gevent 
from gevent import Greenlet, GreenletExit
import socket
from transport import Transport
from messages import Message

game_host = 'ruslug.rutgers.edu'
game_port = 51234
nick = 'tester'

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
	    print "sending punch"
	    self.transport.send(Message.punch().pack())

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
