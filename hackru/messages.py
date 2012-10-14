class MessageError(Exception): pass

class Message(object):

    types = set(['nick', 'punch', 'win', 'lose', 'status', 'auth', 'game', 'opponent'])
    delimeter = '|'

    def __init__(self, type, payload):
	if type not in Message.types:
	    raise MessageError('Invalid message type')
	self.type = type
	self.payload = payload

    def pack(self):
	return '|' + self.type + ':' + str(self.payload) + '|'	

    @staticmethod
    def parse(msg):
	"""
	Returns a Message object if a valid message, else raises MessageError
	"""
	if not Message.is_message(msg):
	    raise MessageError("Invalid message")
	message = msg.strip('|').split(':', 1)
	return Message(message[0], message[1])

    @staticmethod
    def is_message(message):
	if not message:
	    return False
	if not message[0] == '|':
	    return False
	if not message[-1] == '|':
	    return False
	parts = message.strip('|').split(':', 1)
	if len(parts) == 2 and parts[0] in Message.types:
	    return True
	else:
	    return False
    
    @staticmethod 
    def opponent(nick):
	return Message("opponent", nick)

    @staticmethod
    def start_game():
	return Message("game", "start")

    @staticmethod
    def exit():
	return Message("status", "close")

    @staticmethod
    def auth_success():
	return Message("auth", "success")

    @staticmethod
    def nick(nickname):
	return Message('nick', nickname)

    @staticmethod
    def punch():
	return Message('punch', 1)

    @staticmethod
    def lose():
	return Message('lose', 1)

    @staticmethod
    def win():
	return Message('win', 1)

    @staticmethod
    def start():
	pass

