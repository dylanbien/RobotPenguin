import DeltaArm
from time import sleep
from pidev import stepper
from Slush.Devices import L6470Registers as LReg
import Adafruit_PCA9685
Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)

DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5/12.0, 17.8/12.0, 7.5/12.0, 6.148/12.0, 0)
#def wait():
#    while not arm.movement_complete():
#        pass
#    print('done ovng')

arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig, None)
#arm.home_all()#homes it
#wait()
arm.solenoid_up()
sleep(2)
arm.solenoid_down()


