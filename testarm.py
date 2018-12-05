from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()

sleep(2)
#arm.set_all_to_same_angle(0)

sleep(2)
arm.move_to_point(0, 0, 1)
#a0, a1, a2 = arm.compute_triple_inverse_kinematics(2, 3, 5)
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

# for i in [x*.4 for x in range(0,20)]:
#
#     arm.move_to_point(i-2,0,5)
#     sleep(.3)
