from time import sleep
import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)
arm.home_all()
print("Sleep")
sleep(5)
print("Done homing")

#arm.move_to_point_in_straight_line(0.1, 0.1, 0.1, 1)
arm.move_to_point(0, 0, 8)

#arm.set_single_position_steps(0, -25)
#arm.set_single_position_steps(1, -25)
#arm.set_single_position_steps(2, -15)
