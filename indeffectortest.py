from time import sleep
import os
from pidev import stepper
from time import sleep
import Adafruit_PCA9685
                                    
rotator = stepper(port = 3, speed = 20, micro_steps = 1)
rotator.setOverCurrent(6000)
rotator.home(0)



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



