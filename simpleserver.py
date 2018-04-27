import socket
import sys
import ip
send = False
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ip.server_address
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
		if (send): 
			connection.sendall(data)
			send = False
		else:
			data = connection.recv(16)
			if ('?' in data.decode()): 
				send = False
				connection.sendall(b'bupkis ')
			else:
				print ('received this: ' + data.decode())
				connection.sendall(data)
				send = True

	finally:
		# Clean up the connection
		connection.close()