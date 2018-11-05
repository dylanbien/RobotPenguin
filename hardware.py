import DeltaArm
import socket
from threading import Timer

# 0 is up, 90 is right, 180 is down, 270 is left
da = DeltaArm.DeltaArm(0, 1, 2)
current = (0, 0, 0)
direction = 0


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()


def obey(self, retry=5):
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


def obey(retry=5):
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
        if (retry >= 0): obey(retry - 1)

    if (data == 'bupkis '):
        return

    print('received {!r}'.format(data))

    if (data == 'forward '):
        if (direction % 360 == 0):
            current[1] += 1
            da.move_to_point(current)
        elif (direction % 360 == 90):
            current[0] += 1
            da.move_to_point(current)
        elif (direction % 360 == 180):
            current[1] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 270):
            current[0] -= 1
            da.move_to_point(current)
    elif (data == 'backward '):
        if (direction % 360 == 0):
            current[1] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 90):
            current[0] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 180):
            current[1] += 1
            da.move_to_point(current)
        elif (direction % 360 == 270):
            current[0] += 1
            da.move_to_point(current)
    elif (data == 'left '):
        direction += 270
    # spin to win
    elif (data == 'right '):
        direction += 90
    # spin to win
    else:
        print('fail')
        return


print("starting...")
rt = RepeatedTimer(.1, obey)

# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

# MyApp().run()
