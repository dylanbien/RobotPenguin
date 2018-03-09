import socket
import sys
send = False
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
	print('server waiting for a connection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)
		if (send): connection.sendall(str.encode(data))
		else:
			data = connection.recv(16)
			data = data.decode("utf-8")
			if ('?' in data): 
				send = False
				connection.sendall(b'bupkis')
			else:
				print ('received this: ' + data)
				connection.sendall(str.encode(data))
				send = True

	finally:
		# Clean up the connection
		connection.close()