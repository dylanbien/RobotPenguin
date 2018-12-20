import DeltaArm
from time import sleep
    
Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5/12.0, 17.8/12.0, 7.5/12.0, 6.148/12.0, 0)

arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig)

def wait():
    while not arm.movement_complete():
        pass
    
arm.home_all()#homes it
wait()
arm.move_to_point_in_straight_line(0, 0, -1.4, .01)
wait()

print('done goin down')
print('arm please work :)')
sleep(2)
arm.move_to_point_in_straight_line(-.55, -.35, -1.4, .01)
wait()
arm.move_to_point_in_straight_line(-.55, .35, -1.4, .01)
sleep(1)
wait()
##high point 1.2
#low point -1.45
#top left arm.move_to_point_in_straight_line(-.55, -.35, -1.4, .01)