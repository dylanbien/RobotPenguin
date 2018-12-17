from time import sleep
import DeltaArm


Motor1 = DeltaArm.MotorConfig.createMotor(0, 120,-1750,-26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240,-980,-26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360,-2000,-27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(1.04167, 1.4833, 0.3133, 0.25617, 0)
        
crabby = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig)

crabby.home_all()
sleep(2)
crabby.move_to_point(0, 0, -1.34)
sleep(2)
(a1,a2,a3) = (crabby.get_angle(i) for i in range(3) )
print(a1,a2,a3)
crabby.move_to_point_in_straight_line(-.2, .1, -1.34,.01)