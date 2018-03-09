#socket_echo_server.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.1.61', 10003)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)
x = 0
y = 0
a = 0
b = 0
while True:
	# Wait for a connection
	print('waiting for a connection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)

		# Receive the data in small chunks and retransmit it
		while True:
			data = connection.recv(16)
			decoded_data = data.decode("utf-8")
			print('received {!r}'.format(data))
			if data:
				print('sending data back to the client')
				#connection.sendall(decoded_data)
			else:
				print('no data from', client_address)
				break


	finally:
		# Clean up the connection
		connection.close()