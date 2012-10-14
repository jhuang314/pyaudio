import gevent
from gevent.event import Event
from gevent import Greenlet, GreenletExit
from messages import Message, MessageError

class Game(Greenlet):
    damage = 10

    def __init__(self, p1, p2):
	"""
	Initiate a game with two players
	"""
	Greenlet.__init__(self)
	self.p1 = p1
	self.p2 = p2
	self.end = Event()

    def _run(self):
	print "game is starting"
	self.p1.transport.send(Message.opponent(self.p2.name).pack())
	self.p2.transport.send(Message.opponent(self.p1.name).pack())
	
	self.p1.transport.send(Message.start_game().pack())
	self.p2.transport.send(Message.start_game().pack())
	player1 = gevent.spawn(self.run_p1)
	player2 = gevent.spawn(self.run_p2)

	self.end.wait()
	gevent.killall([player1, player2])

	if self.p1.health <= 0:
	    print("player 1 won")
	    self.p1.send(Message.win().pack())
	    self.p2.send(Message.lose().pack())
	else:
	    print("player 2 won")
	    self.p1.send(Message.lose().pack())
	    self.p2.send(Message.win().pack())
	
	self.exit()

    def exit(self):
	raise GreenletExit

    def run_p1(self):
	while True:
	    rec = self.p1.listen()
	    try:
		msg = Message.parse(rec)
	    except MessageError:
		continue
	    if msg.type == 'punch' and msg.payload == '1':
		self.p2.health -= Game.damage
		print "player 2 health: " + str(self.p2.health)
		if self.p2.health <= 0:
		    self.end.set()

    def run_p2(self):
	while True:
	    rec = self.p2.listen()
	    try:
		msg = Message.parse(rec)
	    except MessageError:
		continue
	    if msg.type == 'punch' and msg.payload == '1':
		self.p1.health -= Game.damage
		print "player 1 health: " + str(self.p1.health)
		if self.p1.health <= 0:
		    self.end.set()
