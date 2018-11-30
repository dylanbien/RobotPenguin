from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()
print("Sleep")
#sleep(5)
print("Done homing")


#arm.set_single_position_steps(0,-107.5)
#arm.set_single_position_steps(1,-104)
#arm.set_single_position_steps(2,-106)
#arm.set_single_position_steps(1,-4)
#arm.set_single_position_steps(2,-6.5)
#arm.set_single_angle(2,45)
#arm.set_single_position_steps(0,-9)
#arm.compute_triple_inverse_kinematics(0,0, 0)
#sleep(1)

arm.position_to_angle(0,-50)
#arm.angle_to_position(0,25)
print('ready')
#arm.move_to_point(0,0,5)
#print('at 0,0,5')
#sleep(4)
#print('going')
#for i in [x*.4 for x in range(0,12)]:
#arm.move_to_point(0,3,5)
#sleep(2)
#arm.move_to_point(3,0,5)
     # sleep(1)
     #print(i)
