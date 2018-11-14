import DeltaArm

arm = DeltaArm.DeltaArm(0,1,2)

while(True):
    command = input('>>>>')
    print(command)
    if command == 'home':
        arm.home_all()
    elif command[:4] == 'move':
        armnum = int(command[4:5])
        amount = int(command[5:])
        arm.set_single_position_steps(armnum,-amount)
    elif command[:8] == '*moveall':
        amount = int(command[8:])
        arm.set_all_to_same_position(amount)
    elif command == 'leave':
        break
    elif command[:3] == 'pos':
        print(arm.get_position(0))
        print(arm.get_position(1))
        print(arm.get_position(2))
        print(arm.get_angle(0))
        print(arm.get_angle(1))
        print(arm.get_angle(2))
