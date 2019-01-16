# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import Slush
import math
import time
from pidev import stepper
from collections import namedtuple
import Adafruit_PCA9685

# ////////////////////////////////////////////////////////////////
# //                     Motor Config Class                     //
# ////////////////////////////////////////////////////////////////
class MotorConfig:
    MotorData = namedtuple('MotorData', ['port', 'angle', 'zero_value', 'ninety_value'])

    def createMotor(port, angle, zero_value, ninety_value):
        return MotorConfig.MotorData(port, angle, zero_value, ninety_value)



# ////////////////////////////////////////////////////////////////
# //                   Delta Arm Config Class                   //
# ////////////////////////////////////////////////////////////////

class DeltaArmConfig:
    ArmConstants = namedtuple('ArmConstants',['upper_length', 'lower_length', 'fixed_edge', 'effector_edge', 'end_effector_z_offset'])
    def createConfig(upper_length, lower_length, fixed_edge, effector_edge, end_effector_z_offset):
        return DeltaArmConfig.ArmConstants(upper_length, lower_length, fixed_edge, effector_edge, end_effector_z_offset)


# ////////////////////////////////////////////////////////////////
# //                       DeltaArm   Class                     //
# ////////////////////////////////////////////////////////////////

class DeltaArm:
    # Static constants
    # angles of each effector arm relative to coordinate axis
    # Arm are usually 120 degrees apart from each other
    phi_vals = []

    # Position constants in steps
    zero_vals = []  # number of steps required to make each arm horizontal
    ninety_vals = []  # number of steps required to make each arm vertical

    debug = False

    # ///////////////////////////////////////////////////////////////
    # //                         Init Function                      //
    # ////////////////////////////////////////////////////////////////



    
    #alternate constructor with solenoid + motor
    def __init__(self, Motor1, Motor2, Motor3, DeltaArmConfig,  Motor4=None):
        #all values for Motor4 should be Non except for port
        self.board = Slush.sBoard()
        self.motors = [stepper(port=Motor1.port, micro_steps=32, speed=50, hold_current=30, run_current=30, accel_current=30, deaccel_current=30),
                       stepper(port=Motor2.port, micro_steps=32, speed=50, hold_current=30, run_current=30, accel_current=30, deaccel_current=30),
                       stepper(port=Motor3.port, micro_steps=32, speed=50, hold_current=30, run_current=30, accel_current=30, deaccel_current=30)]
        self.solenoid = Adafruit_PCA9685.PCA9685()
        if Motor4:
            self.indeffector_motor = stepper(port=Motor4.port,speed = 20, micro_steps = 4, run_current=90, accel_current = 25)
            #these values were found through experimentation
            self.indeffector_motor.setMinSpeed(200)
            #self.indeffector_motor.setOverCurrent(4800)
        else:
            self.indeffector_motor = None

        DeltaArm.phi_vals.append(math.radians(Motor1.angle))
        DeltaArm.phi_vals.append(math.radians(Motor2.angle))
        DeltaArm.phi_vals.append(math.radians(Motor3.angle))

        DeltaArm.zero_vals.append(Motor1.zero_value)
        DeltaArm.zero_vals.append(Motor2.zero_value)
        DeltaArm.zero_vals.append(Motor3.zero_value)

        DeltaArm.ninety_vals.append(Motor1.ninety_value)
        DeltaArm.ninety_vals.append(Motor2.ninety_value)
        DeltaArm.ninety_vals.append(Motor3.ninety_value)

        # feet **a picture in the read me shows what each of these values are
        # e = fixed_edge

        global fixed_edge
        global effector_edge
        global upper_len
        global lower_len
        global end_effector_z_offset

        DeltaArm.fixed_edge = DeltaArmConfig.fixed_edge  # length of one side of the top equilateral triangle
        DeltaArm.effector_edge = DeltaArmConfig.effector_edge  # length of one side of the lower equilateral triangle
        DeltaArm.upper_len = DeltaArmConfig.upper_length  # length of the top arm
        DeltaArm.lower_len = DeltaArmConfig.lower_length  # length of the bottom arm
        DeltaArm.end_effector_z_offset = DeltaArmConfig.end_effector_z_offset  # distace from lower equilateral triangle to bottom of the arm

    def debug(message):
        if DeltaArm.debug == True:
            print(message)


    # ////////////////////////////////////////////////////////////////
    # //                    Indeffector Functions                   //
    # ////////////////////////////////////////////////////////////////
    def rotate_degrees(self, deg):
        target = deg * (DeltaArm.rotator_ninety_pos - DeltaArm.rotator_zero_pos) / 90.0 + DeltaArm.rotator_zero_pos
        self.rotator.goTo(int(target))

    # ////////////////////////////////////////////////////////////////
    # //                    Movement Based On Steps                 //
    # ////////////////////////////////////////////////////////////////
    def set_single_position_steps(self, num, pos):
        while self.motors[num].isBusy():
            continue
        self.motors[num].goTo(pos)

    def set_all_to_same_position(self, val):
        for i in range(3):
            self.set_single_position_steps(i, val)

    def set_all_to_different_position(self, pos0, pos1, pos2):
        val = [pos0, pos1, pos2]
        for i in range(3):
            self.set_single_position_steps(i, val[i])

    # ////////////////////////////////////////////////////////////////
    # //                   Movement Based On Angles                 //
    # ////////////////////////////////////////////////////////////////
    def set_single_angle(self, num, ang):
        val = int(self.angle_to_position(num, ang))
        self.set_single_position_steps(num, val)

    def set_all_to_same_angle(self, ang):
        for i in range(3):
            self.set_single_angle(i, ang)

    def set_all_to_different_angle(self, a1, a2, a3):
        angs = [a1, a2, a3]
        DeltaArm.debug('testing values')  # test to make sure all steps are less than zero, or below the sensor
        for i in range(3):
            
            val = int(self.angle_to_position(i, angs[i]))
            if val > 0:
                print('steps > 0: arm would go above sensor')
                return
        DeltaArm.debug('all steps > 0')

        for i in range(3):
            self.set_single_angle(i, angs[i])

    # ////////////////////////////////////////////////////////////////
    # //                      Seting The Velocity                   //
    # ////////////////////////////////////////////////////////////////
    def set_single_velocity(self, num, v):
        d = 0 if v < 0 else 1
        self.motors[num].run(d, abs(v))

    def set_all_to_different_velocity(self, v1, v2, v3):
        vels = [v1, v2, v3]
        for i in range(3):
            self.set_single_velocity(i, vels[i])

    # ////////////////////////////////////////////////////////////////
    # //                       General Functions                    //
    # ////////////////////////////////////////////////////////////////

    def home_all(self):
        DeltaArm.debug('homing')
        for m in self.motors:
            while m.isBusy():
                continue
            m.goUntilPress(1, 0, 5000)

    def stop_all(self):
        self.motors[0].hardStop()
        self.motors[1].hardStop()
        self.motors[2].hardStop()

    def reset_pos_all(self):
        self.motors[0].setAsHome()
        self.motors[1].setAsHome()
        self.motors[2].setAsHome()


    

    def release(self):
        for m in self.motors:
            m.free()

    def movement_complete(self):
	    if (self.motors[0].isBusy() or  self.motors[1].isBusy() or self.motors[2].isBusy() ):
	        return False
	    else:
	       return True  #none of the motors are busy
	
    def wait(self):
            while self.movement_complete() == False:
                pass
            print('done moving')

    # ////////////////////////////////////////////////////////////////
    # //                         Get Functions                      //
    # ////////////////////////////////////////////////////////////////
    def get_position(self, num):

        DeltaArm.debug('      position of motor ' + str(num) + ' is:' +
                       str(self.motors[num].getPosition()))

        return self.motors[num].getPosition()


    def get_angle(self, num):

        DeltaArm.debug('      angle of motor ' + str(num) + ' is: ' +
                       (str(DeltaArm.position_to_angle(num, self.get_position(num)))))

        return DeltaArm.position_to_angle(num, self.get_position(num))

    # ////////////////////////////////////////////////////////////////
    # //                 Angle <----> Position Functions            //
    # ////////////////////////////////////////////////////////////////

    @staticmethod
    def position_to_angle(num, pos):

        DeltaArm.debug('     position to angle: ' + str((pos - DeltaArm.zero_vals[num]) * 90.0 / (
                    DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])) + ' degrees')

        return (pos - DeltaArm.zero_vals[num]) * 90.0 / (DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])

    @staticmethod
    def angle_to_position(num, ang):

        DeltaArm.debug('     angle to position: ' +
                       str((ang) * ((DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num]) / 90.0) + DeltaArm.zero_vals[
                           num]) +
                       ' steps')

        return (ang) * ((DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num]) / 90.0) + DeltaArm.zero_vals[num]

    # ////////////////////////////////////////////////////////////////
    # //                    Move to Point Functions                 //
    # ////////////////////////////////////////////////////////////////

    @staticmethod
    def wrap_angle_rad(theta):
        while abs(theta) > math.pi:
            if theta < math.pi:
                theta += 2 * math.pi
            if theta > math.pi:
                theta -= 2 * math.pi
        return theta

    @staticmethod
    def rotate_point_to_yz_plane(x0, y0, z0, phi):
        # do rotation matrix
        x = x0 * math.cos(phi) + y0 * math.sin(phi)
        y = -x0 * math.sin(phi) + y0 * math.cos(phi)

        # z is the same
        z = z0
        return (x, y, z)
    @staticmethod
    def inverse_kinematics_in_yz_plane(x0, y0, z0):

        DeltaArm.debug('    starting inverse_kinematics_in_yz_plane')

        # parameters
        rf = DeltaArm.upper_len
        re = DeltaArm.lower_len
        f = DeltaArm.fixed_edge
        e = DeltaArm.effector_edge
        z0 = z0 + DeltaArm.end_effector_z_offset
        
        # linear coefficients of EQN z = b*y + a
        a = (x0 ** 2 + (y0 - e / (2 * math.sqrt(3))) ** 2 + z0 ** 2 + rf ** 2 - re ** 2 - f ** 2 / 12) / (2 * z0)
        b = (-f / (2 * math.sqrt(3)) - y0 + e / (2 * math.sqrt(3))) / z0

        # plug line (z = b*y + a) into circle in yz w/ center (-f/2sqrt(3),0)

        disc = (f / math.sqrt(3) + 2 * a * b) - 4 * (b ** 2 + 1) * (f ** 2 / 12 + a ** 2 - rf ** 2)
        if disc < 0:
            # disciminate < 0 -> no solution
            return -1
        
        # compute solution w/ lower y value
        y = (-(f / math.sqrt(3) + 2 * a * b) - math.sqrt(disc)) / (2 * (b ** 2 + 1))
        z = b * y + a

        theta = DeltaArm.wrap_angle_rad(math.atan(z / (y + f / (2 * math.sqrt(3)))))

        DeltaArm.debug('    ending inverse_kinematics_in_yz_plane, returning ' +
                       str(theta) + ' = ' + str(math.degrees(theta)) + ' degrees')

        return math.degrees(theta)

    @staticmethod
    def compute_triple_inverse_kinematics(x, y, z):

        DeltaArm.debug('   starting compute_triple_inverse_kinematics ')

        thetas = []
        for phi in DeltaArm.phi_vals:
            (x0, y0, z0) = DeltaArm.rotate_point_to_yz_plane(x, y, z, phi)
            theta = DeltaArm.inverse_kinematics_in_yz_plane(x0, y0, z0)
            if theta == -1:
                raise ValueError('that point is impossible!')
            thetas.append(theta)

        DeltaArm.debug('   ending compute_triple_inverse_kinematics, returning '
                       + str(thetas[0]) + ' ' + str(thetas[1]) + ' ' + str(thetas[2]))

        return (thetas[0], thetas[1], thetas[2])

    def move_to_point(self, x, y, z):
        DeltaArm.debug('  start move arm to point (' + str(x) + (', ') + str(y) + ', ' + str(z) + (')'))

        (a1, a2, a3) = DeltaArm.compute_triple_inverse_kinematics(x, y, z)

        DeltaArm.debug('  end move to point with angles ' + str(a1) + ' ' + str(a2) + ' ' + str(a3))

        self.set_all_to_different_angle(a1, a2, a3)

    # ////////////////////////////////////////////////////////////////
    # //            Move to Point in Straight Line Functions        //
    # ////////////////////////////////////////////////////////////////

    @staticmethod
    def forward_kinematics(theta1, theta2, theta3):
        rf = DeltaArm.upper_len
        re = DeltaArm.lower_len
        f = DeltaArm.fixed_edge
        e = DeltaArm.effector_edge
        #Finding J' points (centers of intersecting spheres)
        x1 = 0
        y1 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta1))
        z1 = -rf * math.sin(math.radians(theta1))
        (x1, y1, z1) = DeltaArm.rotate_point_to_yz_plane(x1, y1, z1, DeltaArm.phi_vals[0])

        x2 = 0
        y2 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta2))
        z2 = -rf * math.sin(math.radians(theta2))
        (x2, y2, z2) = DeltaArm.rotate_point_to_yz_plane(x2, y2, z2, DeltaArm.phi_vals[1])

        x3 = 0
        y3 = (f - e) / (2 * math.sqrt(3)) + rf * math.cos(math.radians(theta3))
        z3 = -rf * math.sin(math.radians(theta3))
        (x3, y3, z3) = DeltaArm.rotate_point_to_yz_plane(x3, y3, z3, DeltaArm.phi_vals[2])

        # Find intersection of 3 spheres
        w1 = x1 ** 2 + y1 ** 2 + z1 ** 2
        w2 = x2 ** 2 + y2 ** 2 + z2 ** 2
        w3 = x3 ** 2 + y3 ** 2 + z3 ** 2

        # Coefficients in EQN x = a1*z + b1
        dnm = (x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1)

        a1 = ((z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1))
        b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2

        a2 = -((z2 - z1) * (x3 - x1) - (z3 - z1) * (x2 - x1))
        b2 = ((w1 - w2) * (x1 - x3) - (w1 - w3) * (x1 - x2)) / 2

        # Coefficients in Quadratic
        A = dnm ** 2 + a1 ** 2 + a2 ** 2
        B = 2 * (a1 * (b1 - x1 * dnm) + a2 * (b2 - y1 * dnm) - z1 * dnm ** 2)
        C = (b1 - x1 * dnm) ** 2 + (b2 - y1 * dnm) ** 2 + (z1 ** 2 - re ** 2) * dnm ** 2

        # Quadratic EQN
        disc = B ** 2 - 4 * A * C
        # discriminant < 0 -> no solution
        if disc < 0:
            return (-99, -99, -99)
        z = (-B - math.sqrt(disc)) / (2 * A)

        # Solve for x and y from z
        x = (a1 * z + b1) / dnm
        y = -(a2 * z + b2) / dnm

        # Fudge z for end effector height
        z = z - DeltaArm.end_effector_z_offset

        # GG EZ
        return (x, y, z)

    def move_to_point_in_straight_line(self, x, y, z, dr):
        DeltaArm.debug('start move to point in straiht line: ' + str(x) + ' ' + str(y) + ' ' + str(z))

        (a1, a2, a3) = [self.get_angle(i) for i in range(3)]  # gets the current angles
        (x0, y0, z0) = DeltaArm.forward_kinematics(a1, a2, a3) # gets the current XYZ position
        print('starting pt: ' + str(x0) + ' ' + str(y0) + ' ' + str(z0) )
        delta = tuple([a - b for (a, b) in zip((x, y, z), (x0, y0, z0))])  # array (x-x0, y-y0, z-z0) **gets change in cartesisan for all points
        print('change in cartesian: ' + str(delta[0]) + ' ' + str(delta[1]) + ' ' + str(delta[2]))
        rGoal = math.sqrt(delta[0] ** 2 + delta[1] ** 2 + delta[2] ** 2)  # distance between starting and endinng point
        print('distance between starting and ending point is: ' + str(rGoal))
        (xCurr, yCurr, zCurr) = (x0, y0, z0)  # sets current position as starting position
        rCurr = 0  # sets current radius as 0

        while rCurr < rGoal:  # while current radius is less than ending radius
            rCurr += dr  # incriments radius by dr
            #Creates similar triangles and calculates change in x and y
            (xCurr, yCurr, zCurr) = tuple(
                [w + q for (w, q) in zip((x0, y0, z0), tuple([a * float(rCurr) / float(rGoal) for a in delta]))])
            DeltaArm.debug('new position is ' + str(xCurr) + ' ' + str(yCurr) + ' ' + str(zCurr))
            self.move_to_point(xCurr, yCurr, zCurr)

            # advance_time = time.time() + dt
        # while time.time() < advance_time:
        #  pass

        self.move_to_point(x, y, z)
