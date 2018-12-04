from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()
print("Sleep")
#sleep(5)
print("Done homing")


sleep(1)

arm.move_to_point(1,0,5)
angle0 = arm.get_angle(0)
angle1 = arm.get_angle(1)
angle2 = arm.get_angle(2)

print("-------")
pos = arm.forward_kinematics(angle0,angle1,angle2)
print("---" + str(pos))

'''
print('-----angles = ' +str(angles))
print('-----positions = ' +str(pos))
print('--- Arm positions: ')
print(str(arm.get_position(0)))
print(str(arm.get_position(1)))
print(str(arm.get_position(2)))
'''

#arm.position_to_angle(0,-7)
#arm.angle_to_position(0,25)
print('ready')
#arm.move_point()
#sleep(5)
#arm.set_all_to_different_angle(6.25,10,2.5)
##sleep(5)
sleep(2)
#arm.move_to_point(-1,0,5)
#sleep(2)

#arm.move_to_point(-2,0,4.5)
#arm.move_to_point(-3,0,4.5)
#arm.move_to_point(-3,0,4)
#sleep(3)
#arm.move_to_point(-3.2,-4.3,0)
#print('at 0,0,5')
#sleep(4)
#print('going')
'''
for i in [x*.4 for x in range(0,10)]:

    arm.move_to_point(i,0,5)
    sleep(.3)
    print(i)
'''