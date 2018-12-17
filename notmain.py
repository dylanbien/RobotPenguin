class PacketType(enum.Enum):
    NULL = 0
    difficulty = 1
    move = 2
    commandResponse = 3


#         |Bind IP       |Port |Packet enum
s = Server("172.17.21.2", 5001, PacketType)
s.open_server()
s.wait_for_connection()

s.send_packet(PacketType.difficulty, b"easy")
s.send_packet(PacketType.difficulty, b"medium")
s.send_packet(PacketType.difficulty, b"hard")

temp = commands[i]
if temp == "forward":
    s.send_packet(PacketType.move, b"forward")
if temp == "backward":
    s.send_packet(PacketType.move, b"backward")
if temp == "left":
    s.send_packet(PacketType.move, b"left")
if temp == "right":
    s.send_packet(PacketType.move, b"right")

s.recv_packet() == (PacketType.commandResponse, b"continue")
s.recv_packet() == (PacketType.commandResponse, b"win")
s.recv_packet() == (PacketType.commandResponse, b"lose")





class PacketType(enum.Enum):
    NULL = 0
    difficulty = 1
    move = 2
    commandResponse = 3

#         |Server IP     |Port |Packet enum
c = Client("172.17.21.2", 5001, PacketType)
c.connect()

c.recv_packet() == (PacketType.difficulty, b"easy")
c.recv_packet() == (PacketType.difficulty, b"medium")
c.recv_packet() == (PacketType.difficulty, b"hard")

recv_packet() == (PacketType.move, b"forward")
recv_packet() == (PacketType.move, b"backward")
recv_packet() == (PacketType.move, b"left")
recv_packet() == (PacketType.move, b"right")

c.send_packet(PacketType.commandResponse, b"continue")
c.send_packet(PacketType.commandResponse, b"win")
c.send_packet(PacketType.commandResponse, b"lose")

