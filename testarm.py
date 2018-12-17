from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()

#on the table is height -1.335
#arm.set_all_to_same_angle(0)

'''
#angs = arm.compute_triple_inverse_kinematics(0, 0, -1.2)
print(angs)
print('---')
print(arm.forward_kinematics(angs[0], angs[1], angs[2]))
'''

#sleep(2)
#arm.set_single_position_steps(0, -1750)
arm.move_to_point(0, 0, -1.0)
sleep(2)
arm.move_to_point(-0.32, -0.3, -1.2)
sleep(4)
arm.move_to_point(0, 0, -1.0)
sleep(4)
arm.move_to_point_in_straight_line(-0.32, -0.3, -1.2, 0.01)
sleep(4)

'''

#arm.move_to_point_in_straight_line(0.32,0, -1.2, .01)
#sleep(5)
#arm.move_to_point(-1,-.5, -1.1)

# i in [x*.04 for x in range(0,25)]:
     #   arm.move_to_point(-i,0,-1.2)
      #  sleep(.3)
'''
#print(a0)
#print('next')
#x, y, z = arm.forward_kinematics(a0, a1, a2)
#arm.set_single_position_steps(2,-2000)
'''
x, y, z = arm.forward_kinematics(arm.get_angle(0), arm.get_angle(1), arm.get_angle(2))
print("X: ", x)
print("Y: ", y)
print("Z: ", z)
sleep(1)


while 1:
    print("move 1")
    x+=int(input("X: "))
    y+=int(input("Y: "))
    z+=int(input("Z: "))
    a0, a1, a2 = arm.compute_triple_inverse_kinematics(x, y, z)
    print("0: ", a0)
    print("1: ", a1)
    print("2: ", a2)
    x, y, z = arm.forward_kinematics(a0, a1, a2)
    print("X: ", x)
    print("Y: ", y)
    print("Z: ", z)
    arm.set_all_to_different_angle(a0,a1,a2)

'''

    
