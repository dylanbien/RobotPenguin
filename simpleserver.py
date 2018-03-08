import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.17.17.116', 10009)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print('waiting for a connection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)
		data = connection.recv(16)
		if ('?' in data): connection.sendall('bupkis')
		else:
			print ('received this: ' + data)
			connection.sendall(data)

	finally:
		# Clean up the connection
		connection.close()