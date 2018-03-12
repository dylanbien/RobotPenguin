import socket
import sys
import ip
lastMessage = '?'
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (ip.address, 10100)
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
		data = connection.recv(16)
		print ('received this: ' + data.decode())
		if ('?' not in data.decode() and '?' in lastMessage): 
			connection.sendall(data)
			
		elif ('?' in data.decode() and '?' in lastMessage): 
			connection.sendall(b'bupkis ')
			
		elif ('?' in data.decode() and '?' not in lastMessage):
			connection.sendall(lastMessage)
		
		elif ('?' not in data.decode() and '?' not in lastMessage):
			print('something went wrong and i don\'t know how to fix it')
		lastMessage = data.decode()

	finally:
		# Clean up the connection
		connection.close()
