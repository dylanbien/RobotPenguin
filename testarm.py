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
arm.move_to_point_in_straight_line(0, 0, -1.3, .01)
wait()
print('done goin down')
print('arm please work :)')
sleep(2)
arm.move_to_point_in_straight_line(-.62, -.5, -1.3, .01)
wait()
sleep(1)
arm.move_to_point_in_straight_line(.57, -.5, -1.3, .01)
wait()
arm.move_to_point_in_straight_line(.57, .45, -1.3, .01)
print("arm be nice")
##high point 1.2
#low point -1.45