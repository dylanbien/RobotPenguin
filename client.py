#socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.1.61', 10003)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

def send (message):	
	try:

		# Send data
		print('sending {!r}'.format(message))
		sock.sendall(message)


	finally:
		print('closing socket')
		sock.close()