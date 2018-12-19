from time import sleep
import os
from pidev import stepper
from time import sleep
import Adafruit_PCA9685

indeffector = stepper(port = 3, speed = 10, micro_steps = 1)
'''
for i in range(10,101,10):
    print('iteration: ' + i)
    indeffector.relative_move(i)
    sleep(1)

sleep(1)

#move back
indeffector.relative_move(-100)

for i in range(-10,-101,-10):
    print('iteration: ' + i)
    indeffector.relative_move(i)
    sleep(1)

#move back again
indeffector.relative_move(100)
'''

solenoid = Adafruit_PCA9685.PCA9685()

#up
solenoid.set_pwm(0,1,0)
solenoid.set_pwm(0,0,0)




