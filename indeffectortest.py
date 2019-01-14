from time import sleep
import os
from pidev import stepper
from time import sleep
import Adafruit_PCA9685
                                    
rotator = stepper(port = 3, speed = 64, micro_steps = 4, run_current=90, accel_current=25)
rotator.setMinSpeed(200)
rotator.setOverCurrent(4800)
rotator.set_max_speed(500)
rotator.goUntilPress(0,1,500)



'''
Using the motor class
  self.rotator = Slush.Motor(1)
self.rotator.setMinSpeed(200)
        self.rotator.setOverCurrent(6000)

'''


'''
solenoid = Adafruit_PCA9685.PCA9685()
#up
solenoid.set_pwm(0,1,0)
sleep(1)
solenoid.set_pwm(0,0,0)
'''



