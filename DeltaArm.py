import Slush
import math
import time
import _thread
import sys
import math
sys.path.insert(0, "/home/pi/packages/RaspberryPiCommon/pidev")
from stepper import stepper
#sys.path.insert(0,'Adafruit_Python_PCA9685/Adafruit_PCA9685')
#import PCA9685


#Welcome to the delta arm!
#The following code utilizes 3 motors in a delta arm formation
#withing this code an individual is able to move either a single motor or multiple motors a number of steps
#In addition, the user can move all three motors in an Carteisan corrdinate plane

class DeltaArm:

    #Static constants
    
    #angles of each effector arm relative to coordinate axis
    
    #Will sometimes be changed besed on which ports the motors are plugged into
    #6 possible combnations so just trt different ones and see which one creates
    #desired XY plane
    phi_vals = [math.radians(330), math.radians(210), math.radians(90)]
    
    #inches (can change)
    #An image in the delta arm readme will show what each of these values correlates to
    fixed_edge = 7.5
    effector_edge = 6.1487
    upper_len = 12.5 #length of the upper arm
    lower_len = 17.778 #length of the lower arm
    end_effector_z_offset = 5.459
    Sb = 24.6646
    Wb = 10.4591
    wp = 1.3313
    ub = 3.5522

    #Position constants in steps

    zero_vals = [-1750,-980,-2000]  #number of steps required for an arm to be horizontal
    ninety_vals = [-26750,-26800,-27000]  #number of steps required for an arm to be vertical

    
    sqrt3 = math.sqrt(3.0)
    pi = 3.141592653
    sin120 = sqrt3 / 2.0
    cos120 = -0.5
    tan60 = sqrt3
    sin30 = 0.5
    tan30 = 1 / sqrt3

    def __init__(self, c1, c2, c3):
        self.board = Slush.sBoard()
        self.motors = [stepper(port = c1, micro_steps = 32, speed = 30),
                   stepper(port = c2, micro_steps = 32, speed = 30),
                    stepper(port = c3, micro_steps = 32, speed = 30)]

        self.constantMultiplier = self.motors[0].get_micro_steps() * (200/25.4)

        print(self.constantMultiplier)
      #  self.rotator = stepper(port = 3, micro_steps = 128, speed = 1000)
       # self.solenoid = PCA9685.PCA9685() 
        
        

    def home_all(self):
        #_thread.start_new_thread(self.motors[0].goUntilPress, (0, 1, 5000))
        #_thread.start_new_thread(self.motors[1].goUntilPress, (0, 1, 5000))
        #_thread.start_new_thread(self.motors[2].goUntilPress, (0, 1, 5000))

        for mtr in self.motors:
            mtr.goUntilPress(0,1,5000)
            print('homing')

   # def magnet_up(self):
    #    self.solenoid.set_pwm(0,1,0)
    
   # def magnet_down(self):
        #self.solenoid.set_pwm(0,0,0)

    def set_single_position_steps(self,num,pos):
        while self.motors[num].isBusy():
            continue

        self.motors[num].go_to(pos)

        

    def set_all_to_same_position(self,val):
        _thread.start_new_thread(self.set_single_position_steps, (0, val))
        _thread.start_new_thread(self.set_single_position_steps, (1, val))
        _thread.start_new_thread(self.set_single_position_steps, (2, val))
        #for i in range(3):
        #    self.set_single_position_steps(i,val)

    #def rotator_home(self):
      #  self.rotator.goUntilPress(0,1,1000)
    
  #  def rel_move(self, amount):
     #   self.rotator.relative_move(amount)

    def set_all_to_different_position(self,pos0,pos1,pos2):
        _thread.start_new_thread(self.set_single_position_steps, (0, pos0))
        _thread.start_new_thread(self.set_single_position_steps, (1, pos1))
        _thread.start_new_thread(self.set_single_position_steps, (2, pos2))

    def set_single_angle(self,num,ang):
        val = self.angle_to_position(num, ang)
        self.set_single_position_steps(num,val)
        return
    
    def set_all_to_same_angle(self,ang):
        _thread.start_new_thread(self.set_single_angle, (0, ang))
        _thread.start_new_thread(self.set_single_angle, (1, ang))
        _thread.start_new_thread(self.set_single_angle, (2, ang))
        #for i in range(3):
        #    self.set_single_angle(i,ang)
        #test

    def set_all_to_different_angle(self,a1,a2,a3):
        angs = [a1,a2,a3]
        print('testing values')
        for i in range(3):
            val = int(self.angle_to_position(i, angs[i]))
            if val > 0:
                return
        print('all good')
        for i in range(3):
            self.set_single_angle(i,angs[i])
    
    def set_single_velocity(self, num, v):
        d = 0 if v < 0 else 1
        self.motors[num].run(d,abs(v))

    def set_all_to_different_velocity(self, v1, v2, v3):
        vels = [v1,v2,v3]
        for i in range(3):
            self.set_single_velocity(i,vels[i])

    def stop_all(self):
        self.motors[0].hardStop()
        self.motors[1].hardStop()
        self.motors[2].hardStop()

    
    def reset_pos_all(self):
        self.motors[0].setAsHome()
        self.motors[1].setAsHome()
        self.motors[2].setAsHome()

    def get_position(self,num):
        print('position of motor ' + str(num) + ' is:' +
        str(self.motors[num].getPosition()/self.constantMultiplier))
        return self.motors[num].getPosition()/self.constantMultiplier
    
    def get_angle(self, num):
        print('angle of motor ' + str(num) + ' is:v ' +
              (str(DeltaArm.position_to_angle(num,self.get_position(num)))))
        return DeltaArm.position_to_angle(num,self.get_position(num))

    @staticmethod
    def position_to_angle(num,pos):
        return (pos - DeltaArm.zero_vals[num])*90.0/( DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])
    
    @staticmethod
    def angle_to_position(num, ang):
        print('angle to position: ' +
        str((ang)*((DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])/90.0 )+ DeltaArm.zero_vals[num]) +
        ' steps' )
        return ((ang)*((DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])/90.0 )+ DeltaArm.zero_vals[num])


    @staticmethod
    def wrap_angle_rad(theta):
        while abs(theta) > math.pi:
            if theta < math.pi:
                theta += 2*math.pi
            if theta > math.pi:
                theta -= 2*math.pi
        return theta

    @staticmethod
    def rotate_point_to_yz_plane(x0,y0,z0,phi):
        #do rotation matrix
        x = x0*math.cos(phi) + y0*math.sin(phi)
        y = -x0*math.sin(phi) + y0*math.cos(phi)

        #z is the same
        z = z0
        return (x,y,z)


    @staticmethod
    def inverse_kinematics_in_yz_plane(x0,y0,z0):
        print('starting inverse_kinematics_in_yz_plane')
        # parameters
        rf = DeltaArm.upper_len
        re = DeltaArm.lower_len
        f = DeltaArm.fixed_edge
        e = DeltaArm.effector_edge
        z0 = z0 + DeltaArm.end_effector_z_offset

        #linear coefficients of EQN z = b*y + a

        a = (x0**2 + (y0-e/(2*math.sqrt(3)))**2 + z0**2 + rf**2 - re**2 - f**2/12)/(2*z0) 
        b = (-f/(2*math.sqrt(3)) - y0 + e/(2*math.sqrt(3)))/z0

        #plug line (z = b*y + a) into circle in yz w/ center (-f/2sqrt(3),0)

        disc = (f/math.sqrt(3) + 2*a*b) - 4*(b**2+1)*(f**2/12 + a**2 - rf**2)
        if disc < 0:
            #disciminate < 0 -> no solution
            return -1

        #compute solution w/ lower y value
        y = (-(f/math.sqrt(3) + 2*a*b) - math.sqrt(disc))/(2*(b**2+1))
        z = b*y + a

        theta = DeltaArm.wrap_angle_rad(math.atan(z/(y + f/(2*math.sqrt(3)))))
        print('ending inverse_kinematics_in_yz_plane, returning ' +
              str(theta) + ' = ' + str(math.degrees(theta)) + ' degrees')
        return math.degrees(theta)

    @staticmethod    
    def compute_triple_inverse_kinematics(x, y, z):
        print('starting compute_triple_inverse_kinematics ')
        thetas = []
        for phi in DeltaArm.phi_vals:
            (x0,y0,z0) = DeltaArm.rotate_point_to_yz_plane(x,y,z,phi)
            theta = DeltaArm.inverse_kinematics_in_yz_plane(x0,y0,z0)
            if theta == -1:
                raise ValueError('that point is impossible!')
            thetas.append(theta)

        print('ending compute_triple_inverse_kinematics, returning '
              + str(thetas[0])+ ' ' + str(thetas[1]) + ' ' + str(thetas[2]))
        return (thetas[0], thetas[1], thetas[2])

    def move_to_point(self,x,y,z):
        print('start move arm to point (' + str(x) + (', ') + str(y) + ', ' + str(z) + (')') )
        (a1,a2,a3) = DeltaArm.compute_triple_inverse_kinematics(x,y,z)
        print('end move to point with angles ' + str(a1) + ' ' + str(a2) + ' ' + str(a3) )
        self.set_all_to_different_angle(a1,a2,a3)
    
    @staticmethod
    def forward_kinematics(theta1, theta2, theta3):
        print('start forward kinematics')
        rf = DeltaArm.upper_len
        re = DeltaArm.lower_len
        f = DeltaArm.fixed_edge
        e = DeltaArm.effector_edge

        #Finding J' points (centers of intersecting spheres)
        x1 = 0
        y1 = (f-e)/(2*math.sqrt(3)) + rf*math.cos(math.radians(theta1))
        z1 = -rf*math.sin(math.radians(theta1))
        (x1,y1,z1) = DeltaArm.rotate_point_to_yz_plane(x1,y1,z1,DeltaArm.phi_vals[0])
        
        x2 = 0
        y2 = (f-e)/(2*math.sqrt(3)) + rf*math.cos(math.radians(theta2))
        z2 = -rf*math.sin(math.radians(theta2))
        (x2,y2,z2) = DeltaArm.rotate_point_to_yz_plane(x2,y2,z2,DeltaArm.phi_vals[1])

        x3 = 0
        y3 = (f-e)/(2*math.sqrt(3)) + rf*math.cos(math.radians(theta3))
        z3 = -rf*math.sin(math.radians(theta3))
        (x3,y3,z3) = DeltaArm.rotate_point_to_yz_plane(x3,y3,z3,DeltaArm.phi_vals[2])

        #Find intersection of 3 spheres
        w1 = x1**2 + y1**2 + z1**2
        w2 = x2**2 + y2**2 + z2**2 
        w3 = x3**2 + y3**2 + z3**2

        #Coefficients in EQN x = a1*z + b1
        dnm = (x3 - x1)*(y2 - y1) - (x2 - x1)*(y3 - y1)
        
        a1 = ((z2 - z1)*(y3 - y1) - (z3 - z1)*(y2 - y1))
        b1 = -((w2 - w1)*(y3 - y1) - (w3 - w1)*(y2 - y1)) / 2
 
        a2 = -((z2 - z1)*(x3 - x1) - (z3 - z1)*(x2 - x1))
        b2 = ((w1 - w2)*(x1 - x3) - (w1 - w3)*(x1 - x2)) / 2

        #Coefficients in Quadratic
        A = dnm**2 + a1**2 + a2**2
        B = 2*(a1*(b1 - x1*dnm) + a2*(b2 - y1*dnm) - z1*dnm**2)
        C = (b1 - x1*dnm)**2 + (b2 - y1*dnm)**2 + (z1**2 - re**2)*dnm**2

        #Quadratic EQN
        disc = B**2 - 4*A*C
        #discriminant < 0 -> no solution
        if disc < 0:
            return (-99,-99,-99) 
        z = (-B - math.sqrt(disc))/(2*A)

        #Solve for x and y from z
        x = (a1*z + b1) / dnm
        y = -(a2*z + b2) / dnm

        #Fudge z for end effector height
        z = z - DeltaArm.end_effector_z_offset


        print('ending forward kinematics: ' + str(x) + ' ' + str(y) + ' ' + str(z) )

        #GG EZ
        return (x,y,z)

    def move_to_point_in_straight_line(self,x,y,z,dr):
        (a1,a2,a3) = [self.get_angle(i) for i in range(3)] 
        (x0,y0,z0) = DeltaArm.forward_kinematics(a1,a2,a3)
        delta = tuple([a-b for (a,b) in zip((x,y,z),(x0,y0,z0))])
        rGoal =  math.sqrt(delta[0]**2 + delta[1]**2 + delta[2]**2)

        (xCurr, yCurr, zCurr) = (x0,y0,z0)
        rCurr = 0

        while rCurr < rGoal:
            rGoal_local = rCurr + dr
            (xCurr,yCurr,zCurr) = tuple([w+q for (w,q) in zip((x0,y0,z0),tuple([a*rGoal_local/rGoal for a in delta]))])
            (agoal1,agoal2,agoal3) = DeltaArm.compute_triple_inverse_kinematics(xCurr,yCurr,zCurr)
            (acurr1,acurr2,acurr3) = [self.get_angle(i) for i in range(3)] 
            delta_angle = (agoal1 - acurr1, agoal2 - acurr2, agoal3 - acurr3)
            abs_delta = [abs(d) for d in delta_angle]
            scale = max(abs_delta)
            (s1,s2,s3) = [d/scale * 750 for d in delta_angle]
            self.set_all_to_different_velocity(s1,s2,s3)
            while abs(rCurr - rGoal_local) > dr/2:
                print(abs(rCurr - rGoal_local))
                (atemp1,atemp2,atemp3) = [self.get_angle(i) for i in range(3)] 
                (xtemp,ytemp,ztemp) = DeltaArm.forward_kinematics(atemp1,atemp2,atemp3)
                deltatemp = tuple([a-b for (a,b) in zip((xtemp,ytemp,ztemp),(x0,y0,z0))])
                rCurr =  math.sqrt(deltatemp[0]**2 + deltatemp[1]**2 + deltatemp[2]**2)
        #~ print("XYZ: " + str(x) + " : " + str(y) + " : " + str(z))
        self.move_to_point(x,y,z)

'''
    @staticmethod
    def compute_triple_inverse_kinematics(x, y, z):
        a = (DeltaArm.Sb/2) - DeltaArm.fixed_edge
        b = DeltaArm.Wb - DeltaArm.wp
        C_zero = x**2 + y**2+z**2 + a**2
        L_zero = -z + math.sqrt(z**2-C_zero)
    '''











     

