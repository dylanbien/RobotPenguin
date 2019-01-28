import DeltaArm
from time import sleep
from pidev import stepper
from Slush.Devices import L6470Registers as LReg
import Adafruit_PCA9685
Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5/12.0, 17.8/12.0, 7.5/12.0, 6.148/12.0, 0)
def wait():
    while not arm.movement_complete():
        pass
    print('done ovng')
def Rotwait():
    while rotator.isBusy() == True:
        pass
    sleep(1)
    print('done rot')
arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig, None)
arm.home_all()#homes it
wait()
'''
rotator = stepper(port = 3, speed = 30, micro_steps = 2, run_current=50, accel_current=55, hold_current=50)
rotator.setParam(LReg.CONFIG, 0x3618)

rotator.setOverCurrent(6000)
rotator.goUntilPress(0,1,5000)
Rotwait()
sleep(2)

sleep(1.5)
rotator.move(-300)
sleep(1.5)
rotator.move(300)
sleep(1.5)
rotator.move(-2000)
sleep(1.5)
rotator.move(300)
sleep(1.5)
'''
'''
rotator.setMinSpeed(200)

rotator.set_max_speed(500)
rotator.goUntilPress(0,1,500)
sleep(5)
print(rotator.getPosition())
rotator.go_to_position(100)
sleep(5)
print('one')
#def turn(dir):
    #if dir == 'right':
        #rotator.goTo()
    
'''
#wait()
arm.move_to_point_in_straight_line(0, 0, -1.5, .01)
wait()
sleep(1)
#rotator.setMinSpeed(200)
#rotator.setMaxSpeed(500)
#rotator.goUntilPress(0,1,500)



while(True): 
    arm.move_to_point_in_straight_line(-.4, -.38, -1.5, .01)
    wait()
    sleep(1)
    arm.move_to_point_in_straight_line(.3, -.38, -1.5, .01)
    wait()
    sleep(1)
    arm.move_to_point_in_straight_line(.3, .3, -1.5, .01)
    wait()
    sleep(1)
    arm.move_to_point_in_straight_line(-.4, .3, -1.5, .01)
    wait()
    sleep(1)

'''
range# right:.3
arm.move_to_point_in_straight_line(0, 0, -1.4, .01)
print('done goin down')
'''
##high point 1.2
#low point -1.45
#top left arm.move_to_point_in_straight_line(-.55, -.35, -1.4, .01)