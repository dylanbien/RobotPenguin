import Slush
import math
import time
import sys

sys.path.insert(0, "/home/pi/packages/RaspberryPiCommon/pidev")
from stepper import stepper
#sys.path.insert(0,'Adafruit_Python_PCA9685/Adafruit_PCA9685')
#import PCA9685


class DeltaArm:

    #Static constants
    #angles of each effector arm relative to coordinate axis
    phi_vals = [math.radians(210), math.radians(90), math.radians(330)]
    
    #feet
    fixed_edge = 2.1651
    effector_edge = 1.775
    upper_len = 12.5
    lower_len = 17.778
    end_effector_z_offset = 5.459
    #Position constants in steps
    zero_vals = [-2000, -2000, -2000]
    ninety_vals = [64000, 64000 ,64000]

    def __init__(self, c1, c2, c3):
        self.board = Slush.sBoard()
        self.motors = [stepper(port = c1, micro_steps = 32, speed = 20),
                   stepper(port = c2, micro_steps = 32, speed = 20),
                    stepper(port = c3, micro_steps = 32, speed = 20)]
      #  self.rotator = stepper(port = 3, micro_steps = 128, speed = 1000)
       # self.solenoid = PCA9685.PCA9685() 
        
        

    def home_all(self):
        for mtr in self.motors:
            mtr.goUntilPress(0,1,5000)
            
            print(self.get_position(0))
            print(self.get_position(1))
            print(self.get_position(2))
            print('done')

   # def magnet_up(self):
    #    self.solenoid.set_pwm(0,1,0)
    
   # def magnet_down(self):
        #self.solenoid.set_pwm(0,0,0)

    def set_single_position_steps(self,num,pos):
        while self.motors[num].isBusy():
            continue
        '''
        if pos == 0:
            self.motors[num].home(1)
            return
        '''    
        self.motors[num].go_to_position(pos)
        print(self.get_position(0))
        print(self.get_position(1))
        print(self.get_position(2))
        

    def set_all_to_same_position(self,val): 
        for i in range(3):
            self.set_single_position_steps(i,val)

    #def rotator_home(self):
      #  self.rotator.goUntilPress(0,1,1000)
    
  #  def rel_move(self, amount):
     #   self.rotator.relative_move(amount)

        
    def set_single_angle(self,num,ang):
        val = int(self.angle_to_position(num, ang))
        self.set_single_position_steps(num,val)
    
    def set_all_to_same_angle(self,ang):
        for i in range(3):
            self.set_single_angle(i,ang)

    def set_all_to_different_angle(self,a1,a2,a3):
        angs = [a1,a2,a3]
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
        return self.motors[num].getPosition()
    
    def get_angle(self, num):
        return DeltaArm.position_to_angle(num,self.get_position(num))

    @staticmethod
    def position_to_angle(num,pos):
        return (pos - DeltaArm.zero_vals[num])*90.0/( DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])
    
    @staticmethod
    def angle_to_position(num, ang):
        return (ang)*(DeltaArm.ninety_vals[num] - DeltaArm.zero_vals[num])/90.0 + DeltaArm.zero_vals[num]

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
        return math.degrees(theta)

    @staticmethod    
    def compute_triple_inverse_kinematics(x, y, z):
        thetas = []
        for phi in DeltaArm.phi_vals:
            (x0,y0,z0) = DeltaArm.rotate_point_to_yz_plane(x,y,z,phi)
            theta = DeltaArm.inverse_kinematics_in_yz_plane(x0,y0,z0)
            if theta == -1:
                raise ValueError('that point is impossible!')
            thetas.append(theta)
        return (thetas[0], thetas[1], thetas[2])

    def move_to_point(self,x,y,z):
        print('start move arm to point')
        (a1,a2,a3) = DeltaArm.compute_triple_inverse_kinematics(x,y,z)
        print('end move arm to point' + str(a1) + str(a2) + str(a3) )
        self.set_all_to_different_angle(a1,a2,a3)
         
    @staticmethod
    def forward_kinematics(theta1, theta2, theta3):
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
            rCurr += dr
            (xCurr,yCurr,zCurr) = tuple([w+q for (w,q) in zip((x0,y0,z0),tuple([a*float(rCurr)/float(rGoal) for a in delta]))])
            print(xCurr,yCurr,zCurr)
            self.move_to_point(xCurr,yCurr,zCurr)
            advance_time = time.time() + dt
            while time.time() < advance_time:
                pass 
           #~ print("XYZ: " + str(x) + " : " + str(y) + " : " + str(z))
        self.move_to_point(x,y,z)


     




     

