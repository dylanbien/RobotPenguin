from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()
print("Sleep")
#sleep(5)
print("Done homing")



#arm.compute_triple_inverse_kinematics(1,2, 5)
sleep(1)

#arm.position_to_angle(0,-7)
#arm.angle_to_position(0,25)
print('ready')
#arm.move_point()
#sleep(5)
#arm.set_all_to_different_angle(6.25,10,2.5)
##sleep(5)
arm.move_to_point(0,0,4.5)
arm.move_to_point(-2,0,4.5)
arm.move_to_point(-3,0,4.5)
arm.move_to_point(-3,0,4)
#sleep(3)
#arm.move_to_point(-3.2,-4.3,0)
#print('at 0,0,5')
#sleep(4)
#print('going')

#for i in [x*.4 for x in range(0,30)]:

   # arm.move_to_point(i-4,0,4.5)
  #  sleep(.3)
   # print(i)
