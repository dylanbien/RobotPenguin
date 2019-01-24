import DeltaArm
import time

Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5 / 12.0, 17.8 / 12.0, 7.5 / 12.0, 6.148 / 12.0, 0)

arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig)
arm.home_all()
arm.wait()
time.sleep(2)
arm.move_to_point_in_straight_line(-.53, -.45, -1.4, .01)
arm.wait()
time.sleep(2)
arm.solenoid_up()
time.sleep(2)
arm.move_to_point_in_straight_line(-.53, -.47, -1.4, .01)
arm.wait()
time.sleep(1)
arm.solenoid_down()
time.sleep(1)
arm.move_to_point_in_straight_line(0.2, -.45, -1.4, .01)
arm.wait()
arm.solenoid_up()
time.sleep(1)
arm.solenoid_down()

'''while True:
    arm.wait()
    arm.move_to_point_in_straight_line(0, 0, -1.54, .01)
    arm.wait()
    time.sleep(2)
    arm.solenoid_up()
    time.sleep(1)
    arm.solenoid_down()
    time.sleep(1)
    arm.home_all()
'''