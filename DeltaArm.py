#TODO determine if this version is correct with RoboticPenguinHW
import Slush
import math
import time
import sys
import _thread
from pidev import stepper
from apscheduler.schedulers.background import BackgroundScheduler
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
    phi_vals = [math.radians(120), math.radians(240), math.radians(360)]
    
    #inches (can change)
    #An image in the delta arm readme will show what each of these values correlates to
    fixed_edge = 3.76/12.0
    effector_edge = 3.074/12.0
    upper_len = 12.5/12.0 #length of the upper arm
    lower_len = 17.8/12.0#length of the lower arm
    end_effector_z_offset = 0 # 5.459/12.0 **work on
    

    #Position constants in steps

    zero_vals = [-1750,-980,-2000]   #number of steps required for an arm to be horizontal
    ninety_vals = [-26750,-26800,-27000] #number of steps required for an arm to be vertical

    sqrt3 = math.sqrt(3.0)
    pi = 3.141592653
    sin120 = sqrt3 / 2.0
    cos120 = -0.5
    tan60 = sqrt3
    sin30 = 0.5
    tan30 = 1 / sqrt3

    def __init__(self, c1, c2, c3):
        print('hi')
        self.board = Slush.sBoard()
        self.motors = [stepper(port=c1, micro_steps = 32, speed=30),
                   stepper(port=c2, micro_steps=32, speed=30),
                    stepper(port=c3, micro_steps=32, speed=30)]
        self.move_speed = 30
      #  self.rotator = stepper(port = 3, micro_steps = 128, speed = 1000)
       # self.solenoid = PCA9685.PCA9685() 

    def home_all(self):
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
        set_all_same_scheduler = BackgroundScheduler()

        set_all_same_scheduler.add_job(self.set_single_position_steps(0, val))
        set_all_same_scheduler.add_job(self.set_single_position_steps(1, val))
        set_all_same_scheduler.add_job(self.set_single_position_steps(2, val))
        try:
            set_all_same_scheduler.start()
        except KeyboardInterrupt:
            set_all_same_scheduler.shutdown()
            sys.exit("exiting")

        # _thread.start_new_thread(self.set_single_position_steps, (0, val))
        # _thread.start_new_thread(self.set_single_position_steps, (1, val))
        # _thread.start_new_thread(self.set_single_position_steps, (2, val))
        #for i in range(3):
        #    self.set_single_position_steps(i,val)

    def set_all_to_different_position(self,pos0,pos1,pos2):
        set_diff_pos_scheduler = BackgroundScheduler()

        set_diff_pos_scheduler.add_job(self.set_single_position_steps(0, pos0))
        set_diff_pos_scheduler.add_job(self.set_single_position_steps(1, pos1))
        set_diff_pos_scheduler.add_job(self.set_single_position_steps(2, pos2))

        try:
            set_diff_pos_scheduler.start()
        except KeyboardInterrupt:
            set_diff_pos_scheduler.shutdown()
            sys.exit("exiting")

        # _thread.start_new_thread(self.set_single_position_steps, (0, pos0))
        # _thread.start_new_thread(self.set_single_position_steps, (1, pos1))
        # _thread.start_new_thread(self.set_single_position_steps, (2, pos2))

    def set_single_angle(self,num,ang):
        val = int(self.angle_to_position(num, ang))
        self.set_single_position_steps(num,val)
        return
    
    def set_all_to_same_angle(self,ang):
       
        for i in range(3):
            self.set_single_angle(i,ang)


    def set_all_to_different_angle(self,a1,a2,a3):
        angs = [a1,a2,a3]
        
        print('testing values')
        for i in range(3):
            
            val = int(self.angle_to_position(i, angs[i]))
            if val > 0:
                print('cant move, steps > 0')
                return
        print('all good')
        for i in range(3):
            self.set_single_angle(i, angs[i])
    
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
        str(self.motors[num].getPosition()))
        return self.motors[num].getPosition()
    
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
        
      
        
        return (x,y,z0)


    @staticmethod
    def inverse_kinematics_in_yz_plane(x0,y0,z0):
        #print('starting inverse_kinematics_in_yz_plane')
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
        #print('starting compute_triple_inverse_kinematics ')
        thetas = []
        for phi in DeltaArm.phi_vals:
            (x0,y0,z0) = DeltaArm.rotate_point_to_yz_plane(x,y,z,phi)
            theta = DeltaArm.inverse_kinematics_in_yz_plane(x0,y0,z0)
            if theta == -1:
                raise ValueError('that point is impossible!')
            thetas.append(theta)

        #print('ending compute_triple_inverse_kinematics, returning '
        #      + str(thetas[0])+ ' ' + str(thetas[1]) + ' ' + str(thetas[2]))
        return (thetas[0], thetas[1], thetas[2])

    def move_to_point(self,x,y,z):
        #print('start move arm to point (' + str(x) + (', ') + str(y) + ', ' + str(z) + (')') )
        (a1,a2,a3) = DeltaArm.compute_triple_inverse_kinematics(x,y,z)
        #print('end move to point with angles ' + str(a1) + ' ' + str(a2) + ' ' + str(a3) )
        self.set_all_to_different_angle(a1,a2,a3)

    def move_to_point_in_straight_line(self,x,y,z,dr):
        dt = dr/self.move_speed/2
        print('start move to point in straight line')
        (a1,a2,a3) = [self.get_angle(i) for i in range(3)] #gets the current angles 
        (x0,y0,z0) = DeltaArm.forward_kinematics(a1,a2,a3) #gets the current XYZ position
        delta = tuple([a-b for (a,b) in zip((x,y,z),(x0,y0,z0))]) #for all points x-x0 **gets change in cartesisan for all points
        print(delta)
        rGoal =  math.sqrt(delta[0]**2 + delta[1]**2 + delta[2]**2)
        print(rGoal)
        (xCurr, yCurr, zCurr) = (x0,y0,z0) #where the arm starts
        rCurr = 0 #distance away from starting point

        while rCurr < rGoal: #while arm is not add ending point
            rCurr += dr #incirmenting by dr
            (xCurr,yCurr,zCurr) = tuple([w+q for (w,q) in zip((x0,y0,z0),tuple([a*float(rCurr)/float(rGoal) for a in delta]))])
            print(xCurr, yCurr, zCurr)
            self.move_to_point(xCurr, yCurr, zCurr)

            #advance_time = time.time() + dt
            #while time.time() < advance_time:
            #    pass

           
        self.move_to_point(x,y,z)

        print('end move to point in straight line')

    @staticmethod
    def forward_kinematics(theta1, theta2, theta3):
        rf = DeltaArm.upper_len
        re = DeltaArm.lower_len
        f = DeltaArm.fixed_edge
        e = DeltaArm.effector_edge

        t = (f - e) * DeltaArm.tan30 / 2
        dtr = math.pi / float(180.0)

        theta1 *= dtr
        theta2 *= dtr
        theta3 *= dtr

        y1 = -(t + rf * math.cos(theta1))

        z1 = -rf * math.sin(theta1)


        y2 = (t + rf * math.cos(theta2)) * DeltaArm.sin30

        x2 = y2 * DeltaArm.tan60

        z2 = -rf * math.sin(theta2)


        y3 = (t + rf * math.cos(theta3)) * DeltaArm.sin30

        x3 = -y3 * DeltaArm.tan60

        z3 = -rf * math.sin(theta3)


        dnm = (y2 - y1) * x3 - (y3 - y1) * x2


        w1 = y1 * y1 + z1 * z1

        w2 = x2 * x2 + y2 * y2 + z2 * z2

        w3 = x3 * x3 + y3 * y3 + z3 * z3

        # x = (a1 * z + b1) / dnm

        a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)

        b1 = -((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

        # y = (a2 * z + b2) / dnm

        a2 = -(z2 - z1) * x3 + (z3 - z1) * x2

        b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0

        #a * z ^ 2 + b * z + c = 0

        a = a1 * a1 + a2 * a2 + dnm * dnm

        b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)

        c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - re * re)
        #discriminant

        d = b * b - float(4.0 * a * c)
        if (d < 0):
            return -1 #non-existing point

        z0 = -float(0.5 * (b + math.sqrt(d)) / a)
        x0 = (a1 * z0 + b1) / dnm
        y0 = (a2 * z0 + b2) / dnm
        return (x0,y0,z0)


