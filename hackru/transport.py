import socket
from messages import Message

class TransportError(Exception): pass

class Transport(object):
    def __init__(self, sock, address):
	self.sock = sock
	self.host = address[0]
	self.port = address[1]

    def close(self):
	self.sock.close()

    def _recv(self, size):
	data = ''
	while len(data) < size:
	    try:
		chunk = self.sock.recv(size-len(data))
	    except socket.error as (err, msg):
		raise TransportError("[Errno %d] %s" % (err, msg))
	    if chunk == '':
		raise TransportError("Socket connection broken")
	    data += chunk
	return data

    def _receive_message(self):
	msg = ''
	c = self._recv(1)
	if c == Message.delimeter:
	    msg += c
	    while True:
		c = self._recv(1)
		msg += c
		if c == Message.delimeter:
		    break
	return msg
	    
    def _send(self, msg, msglen):
	totalsent = 0
	while totalsent < msglen:
	    try:
		sent = self.sock.send(msg[totalsent:])
	    except socket.error as (err, msg):
		raise TransportError("[Errno %d] %s" % (err, msg))
	    if sent == 0:
		raise TransportError("Socket connection broken")
	    totalsent += sent

    def send(self, msg):
	return self._send(msg, len(msg))
    
    def receive(self):
	return self._receive_message()

