import time
from threading import Thread

def playNote(i):
    print 'playing notes'
    

def detect(i):
    print "detecting punch"


playNoteThread = Thread(target=playNote, args=(1,))
playNoteThread.start()

detectPunchThread = Thread(target=detect, args=(2,))
detectPunchThread.start()
