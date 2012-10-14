import socket
from gevent import Timeout, GreenletExit
from messages import Message, MessageError
from transport import Transport

class PlayerError(Exception): pass

class Player(object):

    auth_timeout = 5

    def __init__(self, socket, address):
	self.transport = Transport(socket, address)
	self.host = address[0]
	self.port = address[1]
	self.health = 100

    def close(self):
	self.transport.send(Message.exit().pack())
	self.transport.close()

    def auth(self):
	recv = None
	with Timeout(Player.auth_timeout, PlayerError("Authentication timed out")):
	    try:
		msg = self.transport.receive()
	    except PlayerError as e:
		print("error on receive")
		print(e)
		return False

	try:
	    msg = Message.parse(msg)
	except MessageError:
	    print("bad message")
	    return False
	if msg.type == "nick":
	    self.name = msg.payload
	    self.transport.send(Message.auth_success().pack())
	    return True
	return False

    def listen(self):
	return self.transport.receive()

    def send(self, msg):
	self.transport.send(msg)
