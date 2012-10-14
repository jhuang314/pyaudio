from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent.server import StreamServer
import gevent
from messages import Message, MessageError
from game import Game
from player import Player

tcpserver_port = 51234
players = []
games = []

def game_maker():
    while True:
	if len(players) >= 2:
	    print "starting game"
	    p1 = players.pop()
	    p2 = players.pop()
	    game = Game(p1, p2)
	    game.start()
	    games.append(game)
	gevent.sleep(10)

def tcp_handler(socket, address):
    player = Player(socket, address)
    if not player.auth():
	player.close()
    else:
	players.append(player)
	print("Player " + player.name + " connected")

if __name__ == "__main__":
    gevent.spawn(game_maker)
    tcpserver = StreamServer(('0.0.0.0', tcpserver_port), tcp_handler)
    print("Serving TCP sockets on port %d" % tcpserver_port)
    tcpserver.serve_forever()
