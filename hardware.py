# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
import DeltaArm
import socket
import sys
import ip

da = DeltaArm.DeltaArm(0,1,2)

def obey(self, retry = 5):
	data = ''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ip.server_address
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
		main.playerForward()
	elif (data == 'backward '):
		main.playerBackward()
	elif (data == 'left '):
		main.playerRotate('left')
	elif (data == 'right '):
		main.playerRotate('right')
	else:
		print ('fail')
		return

class MyApp(App):
	def build(self):
		pass



# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

MyApp().run()
