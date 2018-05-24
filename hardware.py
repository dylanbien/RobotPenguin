# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
#import DeltaArm
import socket
import sys
import ip
import hardwareip
from threading import Timer
from time import sleep

#da = DeltaArm.DeltaArm(0,1,2)

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def obey(retry = 5):
	data = ''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = hardwareip.server_address
	print('connecting to {} port {}'.format(*server_address))
	sock.connect(server_address)
	print('i am hardware.py')
	sock.sendall(b'?')
	spaceReceived = False
	try:
		while (not spaceReceived):
			request = sock.recv(16).decode()
			data += request
			if (' ' in data): spaceReceived = True
	except OSError:
		if(retry >= 0): obey(retry - 1)
				
	if (data == 'bupkis '):
		return
	print('received {!r}'.format(data))
	if (data == 'forward '):
		print('forward')
	elif (data == 'backward '):
		print('back')
	elif (data == 'left '):
		print('left')
	elif (data == 'right '):
		print('right')
	else:
		print ('fail')
		return


print ("starting...")
rt = RepeatedTimer(.1, obey) 

# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

#MyApp().run()
