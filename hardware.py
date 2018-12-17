import DeltaArm
import socket
from threading import Timer
from time import sleep

# 0 is up, 90 is right, 180 is down, 270 is left
da = DeltaArm.DeltaArm(0, 1, 2)
da.home_all()
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

def obey(self, data):


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
sleep(2)
print('1')
# MyApp().run()
