# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
import DeltaArm
import socket
import sys
import ip

da = DeltaArm.DeltaArm(0,1,2)
current = (0, 0, 0)
direction = 0
#0 is up, 90 is right, 180 is down, 270 is left


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
		if (direction%360 == 0):
			current[1] += 1
			da.move_to_point(current)
		elif (direction%360 == 90):
			current[0] += 1
			da.move_to_point(current)
		elif (direction%360 == 180):
			current[1] -= 1
			da.move_to_point(current)
		elif (direction%360 == 270):
			current[0] -= 1
			da.move_to_point(current)
	elif (data == 'backward '):
		if (direction%360 == 0):
			current[1] -= 1
			da.move_to_point(current)
		elif (direction%360 == 90):
			current[0] -= 1
			da.move_to_point(current)
		elif (direction%360 == 180):
			current[1] += 1
			da.move_to_point(current)
		elif (direction%360 == 270):
			current[0] += 1
			da.move_to_point(current)
	elif (data == 'left '):
		direction += 270
		#spin to win
	elif (data == 'right '):
		direction += 90
		#spin to win
	else:
		print ('fail')
		return

class MyApp(App):
	def build(self):
		Clock.schedule_interval(obey, .1)



# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

MyApp().run()
