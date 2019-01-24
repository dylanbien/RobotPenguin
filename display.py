from kivy.config import Config

Config.set('graphics', 'resizable', False)

import os
import time

os.environ["DISPLAY"] = ":0.0"
import string
import random
import DeltaArm
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from time import sleep
from kivy.uix.behaviors import ButtonBehavior
import networkx as nx
import copy

G = nx.Graph()

# from kivy.uix.widget import Widget

"""
Setup
"""

difficulty = 'easy'
locPenguin = 1  # sets starting location of the penguin
locGoal = [49, 49, 49]  # location of the fish

sm = ScreenManager()
Window.size = (1920, 1080)
Window.fullscreen = True
TransparentId = 'icons/ICON_Transparent.png'

"""
Arm Info
"""
x_constant = .165  # work on
y_constant = .1183

Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5 / 12.0, 17.8 / 12.0, 7.5 / 12.0, 6.148 / 12.0, 0)

arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig)

arm.home_all()  # homes it
arm.move_to_point_in_straight_line(0, 0, -1.4, .01)

currentPos = [0, 0, -1.4]
nextPos = [0, 0, -1.4]

from pidev import stepper
from Slush.Devices import L6470Registers as LReg

rotator = stepper(port = 3, speed = 30, micro_steps = 2, run_current=50, accel_current=55, hold_current=50)
rotator.setParam(LReg.CONFIG, 0x3618)

rotator.setOverCurrent(6000)
rotator.goUntilPress(0, 1, 5000)

victory = False

def rotatorWait():
    while rotator.isBusy() == True:
        pass
    sleep(.5)

def rotate_arm(direction):
    global nextPos
    global currentPos

    currentPos[2] -= .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()

    sleep(.1)

    currentPos[2] += .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()

    sleep(.1)
    
    print('running rotate arm ' + direction)

    if direction == 'left':
        rotator.move(200)
    else:
        rotator.move(-200)

    rotatorWait()

    sleep(.1)
   
    currentPos[2] -= .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()

    sleep(.1)

    currentPos[2] += .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()

    sleep(.3)

def move_arm():
   
    global nextPos
    global currentPos

    currentPos[2] -= .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    #arm.solenoid_up()
    arm.wait()

    sleep(.1)

    currentPos[2] += .1  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()
    #arm.solenoid_down()
    sleep(.1)

    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move to new position
    arm.wait()

    sleep(.1)

    nextPos[2] -= .1  # change z value
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move down
    arm.wait()

    sleep(.1)

    nextPos[2] += .1
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move up
    arm.wait()

    sleep(.1)

    currentPos = copy.deepcopy(nextPos)

    sleep(.3)
    
"""
Server
"""

import enum
from dpea_p2p import Client

import threading


class PacketType(enum.Enum):
    NULL = 0
    difficulty = 1
    move = 2
    rotate = 3
    responseCommand = 4


#         |Server IP     |Port |Packet enum
c = Client("172.17.21.1", 5001, PacketType)
print('beginning to connect')
c.connect()
print('connected')


def handle_difficulty_packet(payload):
    print("recieved " + payload.decode("ascii"))
    reset(payload.decode("ascii"))


def handle_move_packet(payload):
    print("recieved " + payload.decode("ascii"))
    main.playerMove(payload.decode("ascii"))


def handle_rotate_packet(payload):
    print("recieved " + payload.decode("ascii"))
    main.playerRotate(payload.decode("ascii"))


def check_server():
    handlers = {PacketType.difficulty: handle_difficulty_packet,
                PacketType.move: handle_move_packet,
                PacketType.rotate: handle_rotate_packet}
    packet_type, payload = c.recv_packet()

    if packet_type in handlers:
        handlers[packet_type](payload)
    else:
        print("got unhandled packet!")


def communication():
    while True:
        check_server()


# ////////////////////////////////////////////////////////////////
# //	               		Reset Function			    		//
# ////////////////////////////////////////////////////////////////

            
def reset(dif):
    global difficulty
    difficulty = dif

    print('now is ' + difficulty)
    

    
    # sets possible locations of the obstacles
    allObstacles = [
        [2, 3],
        [11, 12],
        [15, 16],
        [25],
        [20, 21],
        [28, 37],
        [31, 40],
        [39, 41],
        [44, 45],
        [46, 33],
    ]

    bearPos = []
    assignedObstacleLocations = []
    
    for actor in main.children[0].children:
            actor.source = TransparentId
            

    for temp in allObstacles:
        y = random.randint(0, len(temp) - 1)  # get random in in each array
        saved = temp[y]
        assignedObstacleLocations.append(saved)

    print('obstacles at')
    print(assignedObstacleLocations)

    assignedGoal = 0
    not_obstacles = [i for i in main.children[0].children if (i.number_as_int() not in assignedObstacleLocations)]

    if (dif == 'easy'):
        assignedGoal = locGoal[0]
    elif (dif == 'medium'):
        assignedGoal = locGoal[1]
    elif (dif == 'hard'):
        assignedGoal = locGoal[2]

    actorGoal = main.findActor(assignedGoal)  # assigns goal id
    print('goal is ' + str((assignedGoal)))
    actorGoal.source = 'icons/ICON_Goal.jpg'

    actorPenguin = main.findActor(locPenguin)  # places penguin
    print('player is ' + str(locPenguin))
    actorPenguin.source = 'players/ICON_Player_180.jpg'

    rows = [list(range(1, 8)), list(range(8, 15)), list(range(15, 22)), list(range(22, 29)), list(range(29, 36)),
            list(range(36, 43)), list(range(43, 50))]
    row_pairs = []
    for r in rows:
        for x in range(0, len(r) - 1):
            row_pairs.append((r[x], r[x + 1]))

    G.add_edges_from(row_pairs)

    print(row_pairs)
    coloumn_pairs = []

    for c in range(1, 8):
        coloumn = list(range(c, 43 + c, 7))
        for x in range(0, len(coloumn) - 1):
            coloumn_pairs.append((coloumn[x], coloumn[x + 1]))

    G.add_edges_from(coloumn_pairs)

    print("Test: Finding shortest path from 1 to 29 -  " + str(nx.shortest_path(G, source=1, target=29)))

    for actor in main.children[0].children:

        if '26' in actor.id:
            actor.source = 'icons/ICON_Bear_2.jpg'

        for i in assignedObstacleLocations:
            if (actor.id == 'actor' + str(i)):  # assigns jewels id to actor + obstacle
                if (i % 2 == 0):
                    actor.source = 'icons/ICON_Igloo.jpg'
                    #actor.remove_node()

                else:
                    actor.source = 'icons/ICON_Jewel.jpg'
                    actor.remove_node()


    for node in assignedObstacleLocations:
        G.remove_node(node)


#Begins arm stuff after initializing render

    arm.home_all()
    arm.wait()
    rotator.goUntilPress(0, 1, 5000)
    arm.move_to_point_in_straight_line(0, 0, -1.4, .01)
    arm.wait()
    sleep(1)
    arm.move_to_point_in_straight_line(-.53, -.45, -1.4, .01)

    global currentPos
    global nextPos

    currentPos = [-.55, -.41, -1.4]
    nextPos = [-.55, -.41, -1.4]
    # arm.move_to_point(0,0, -1.34)


"""
MyApp Creation
"""


class MyApp(App):

    def build(self):
        # Clock.schedule_interval(obey, .1)
        return sm

    @staticmethod
    def quitAll():
        quit()


"""
MainScreen Class Creation
"""


class MainScreen(Screen):

    def findActor(self, ActorIndex):
        return self.children[0].children[len(self.children[0].children) - ActorIndex]

    def exitProgram(self):
        App.get_running_app().stop()
        Window.close()

    # Replaces every image with a blank image
    def resetBoard(self):
        for actor in self.children[0].children:
            actor.source = TransparentId

    def addActor(self, location, type):
        for actor in self.children[0].children:
            if (actor.id == location):
                actor.source = type

    def removeActor(self, location):
        for actor in self.children[0].children:
            if (actor.id == location):
                actor.source = TransparentId

    def playerMove(self, movement):

        if movement == 'forward':
            self.playerForward()
        else:
            self.playerBackward()

    def playerForward(self):  # just find the location of the player
        print('you have moved the player forwards')
        for actor in main.children[0].children:  # loops through all actors
            if ('Player' in actor.source):
                # if an actors source has the word plater in it

                actor.moveForward()  # (players/ICON_Player.jpg) > name of player
                return

    def playerBackward(self):
        print('you have moved the player backwards')
        for actor in self.children[0].children:
            if ('Player' in actor.source):
                actor.moveBackward()
                return

    def playerRotate(self, direction):
        print('you have rotated the player ' + direction)
        for actor in self.children[0].children:
            if ('Player' in actor.source):
                actor.rotateDirection(direction)
                return

    def getAdjacentTiles(self, actor,diagonals=False):
        transformations = []
        if diagonals:
            transformations = [-1, 1, 7, -7, -6, 6, -8, 8] #3x3 grid with the actor in the middle
        else:
            transformations = [-1, 1, 7, -7]
        left_edge = [1+x for x in range(0,43,7)]
        right_edge = [7+x for x in range(0,43,7)]
        locations = []

        if actor.number_as_int() in right_edge:
            for i in transformations:
                if i not in [1, -6, 8] and G.has_node(actor.number_as_int() + i):
                    locations.append(actor.number_as_int() + i)
        elif actor.number_as_int() in left_edge:
            for j in transformations and G.has_node(actor.number_as_int() + j):
                if j not in [-1, -8, 6]:
                    locations.append(actor.number_as_int() + j)
        else:
            for k in transformations:
                if G.has_node(actor.number_as_int() + k):
                    locations.append(actor.number_as_int() + k)

        return locations



    """
    Hunt Player
    """


    def huntPlayer(self):
        global difficulty
        global turn
        #print('turn is ' + str(turn) + ', so moving twice will be ' + str(turn % 2 == 0))
        # getting the bear actor
        bear = None
        player = None
        fish = None
        if victory:
            return

        for b in self.children[0].children:
            if 'Bear' in b.source:
                bear = b
            if 'Player' in b.source:
                player = b
            if 'Goal' in b.source:
                fish = b
        shortest_path_from_bear_to_fish = nx.shortest_path(G, source=bear.number_as_int(), target=fish.number_as_int())

        if difficulty == 'easy':
            bear_loc = bear.number_as_int()
            possible_locs = self.getAdjacentTiles(bear)
            bear.eatActor(random.choice(possible_locs))

        if difficulty == 'medium':

            if len(shortest_path_from_bear_to_fish) > 2:
                print(str(shortest_path_from_bear_to_fish))
                bear.eatActor(shortest_path_from_bear_to_fish[1])
            else:
                surrounding_fish_locs = self.getAdjacentTiles(fish, True)
                surrounding_bear_locs = self.getAdjacentTiles(bear)#check
                common_locations = list(set(surrounding_bear_locs).intersection(surrounding_fish_locs))
                for loc in common_locations:
                    if str(loc) in fish.id:
                        common_locations.remove(loc)
                if player.number_as_int() in surrounding_bear_locs:
                    bear.eatActor(player.number_as_int())
                else:
                    bear.eatActor(random.choice(common_locations))


        if (difficulty == 'hard'):
            shortest_path_from_bear_to_player = nx.shortest_path(G, source=bear.number_as_int(),
                                                               target=player.number_as_int())
            if len(shortest_path_from_bear_to_fish) >= len(shortest_path_from_bear_to_player): #bear is closer to player)
                bear.eatActor(shortest_path_from_bear_to_player[1])
            else: #bear is closer to the fish
                if len(shortest_path_from_bear_to_player) == 2:
                #bear is right next to fish, but won't eat it, so it
                # moves towards the player instead
                    bear.eatActor(shortest_path_from_bear_to_player[1])
                else:
                    bear.eatActor(shortest_path_from_bear_to_fish[1])




"""
Actor Class
"""


class Actor(ButtonBehavior, AsyncImage):  # creates an actor class

    def __init__(self, *args, **kwargs):
        AsyncImage.__init__(self, *args, **kwargs)
        self.number = ''.join(i for i in self.id if i.isdigit())
        G.add_node(self.number)

    def remove_node(self):
        G.remove_node(self.number)

    def number_as_int(self):
        return int(self.number)

    def on_press(self):  # when button is pressed
        print('pressed' + str(self.id))

    # ////////////////////////////////////////////////////////////////////////////
    # //						        	Move Actor 							//
    # ////////////////////////////////////////////////////////////////////////////

    """
    Forward/Backward
    """

    def moveForward(self):  # find out which image is on the screen
        # there are different images for the player based on the direction they are facing

        if ('90' in self.source):  # right
            self.moveRight()
            main.huntPlayer()

            return
        elif ('180' in self.source):  # down
            self.moveDown()
            main.huntPlayer()
            return
        elif ('270' in self.source):  # left
            self.moveLeft()
            main.huntPlayer()
            return
        else:  # up
            self.moveUp()
            main.huntPlayer()
            return

    def moveBackward(self):
        if ('90' in self.source):
            self.moveLeft()
            main.huntPlayer()
            return
        elif ('180' in self.source):
            self.moveUp()
            main.huntPlayer()
            return
        elif ('270' in self.source):
            self.moveRight()
            main.huntPlayer()
            return
        else:
            self.moveDown()
            main.huntPlayer()
            return

    """
    Left/Right/Up/Down
    """


    def moveRight(self):  # strafe
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) + 1


        if (next % main.children[0].cols == 1):
            print('cant move, at the right wall')
            c.send_packet(PacketType.commandResponse, b"lose")
            return
        else:
            nextPos[0] += x_constant
            self.move(next)


    def moveLeft(self):  # strafe
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) - 1


        if (next % main.children[0].cols == 0):
            print('cant move, at the left wall')
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:
            nextPos[0] -= x_constant
            self.move(next)


    """
    move
    """


    def moveUp(self):
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) - main.children[0].cols

        if (next < 0):
            print('cant move, at the top wall')
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:
            nextPos[1] -= y_constant
            self.move(next)


    def moveDown(self):
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) + main.children[0].cols


        if (next > main.children[0].rows * main.children[0].cols):
            print('cant move, at the bottom wall')
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:

            nextPos[1] += y_constant
            self.move(next)


    # gets called in all the directional moves
    def move(self, next):
        actor = main.findActor(next)  # gets the with id value next
        if (actor.source == TransparentId):
            # if next spot is clear
            temp = self.source
            self.source = actor.source
            actor.source = temp

            if 'Player' in actor.source:
                print('sending continue 1')
                move_arm()
                c.send_packet(PacketType.responseCommand, b"continue")

            return
        if ('Bear' in actor.source):
            self.source = TransparentId
            c.send_packet(PacketType.responseCommand, b"lose")

        elif ('Goal' in actor.source and 'Player' in self.source):  # if you next location is the fish
            actor.source = self.source
            self.source = TransparentId
            print('you win')

            move_arm()

            victory = True
            c.send_packet(PacketType.responseCommand, b"win")
            return
        elif ('Player' in self.source and 'Igloo' in actor.source):
            print('you hit an obstacle')
            c.send_packet(PacketType.responseCommand, b"lose")
            return  # can't move...you lose
        elif ('Player' in self.source and 'Jewel' in actor.source):
            print('you hit an obstacle')
            c.send_packet(PacketType.responseCommand, b"lose")
            return  # can't move...you lose

    def eatActor(self,next):
        actor = main.findActor(next)
        if 'Player' in actor.source:
            actor.source = TransparentId
            self.move(next)
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:
            self.move(next)


# ////////////////////////////////////////////////////////////////////////////
# //						        	Rotate Actor 				    	//
# ////////////////////////////////////////////////////////////////////////////

    def rotateDegrees(self, location, degrees):
        if (sm.current != 'main'): return
        for actor in main.children[0].children:
            if (actor.id == location and 'Player' in actor.source):
                if (degrees == 0 or degrees == 360 or degrees % 90 != 0):
                    actor.source = 'players/ICON_Player.jpg'
                    print('sending continue 2')
                    c.send_packet(PacketType.responseCommand, b"continue")
                elif (degrees > 360):
                    actor.source = 'players/ICON_Player_' + str(degrees % 360) + '.jpg'
                    print('sending continue 3')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    actor.source = 'players/ICON_Player_' + str(degrees) + '.jpg'
                    print('sending continue 4')
                    c.send_packet(PacketType.responseCommand, b"continue")


    def rotateDirection(self, direction):
        if (sm.current != 'main'): return



        if (direction == 'left' and self.source == 'players/ICON_Player.jpg'):  # if main icon
            self.source = 'players/ICON_Player_270.jpg'

            print('sending continue 5')
            rotate_arm(direction)

            c.send_packet(PacketType.responseCommand, b"continue")
            return
        elif (direction == 'right' and self.source == 'players/ICON_Player.jpg'):  # if main icon
            self.source = 'players/ICON_Player_90.jpg'

            print('sending continue 6')
            rotate_arm(direction)

            c.send_packet(PacketType.responseCommand, b"continue")
            return
        else:
            degree = int(self.source.strip(string.ascii_letters + string.punctuation))

            if (direction == 'left'):
                angle = str(((degree + 270) % 360))

                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                    print('sending continue 8')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
                    print('sending continue 9')
                    c.send_packet(PacketType.responseCommand, b"continue")
                
                rotate_arm(direction)

            else:
                angle = str(((degree + 90) % 360))
                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                    print('sending continue 10')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
                    print('sending continue 11')
                    c.send_packet(PacketType.responseCommand, b"continue")
                
                rotate_arm(direction)


Window.clearcolor = (0.1, 0.1, 0.1, 1)  # (WHITE)

"""
Create grid/actors
"""

# creates a 9 * 9 grid
grid = GridLayout(id='grid', cols=7, rows=7, padding=[415, 150, 415, 150], spacing=1.5)

# sets the background image
bg = AsyncImage(source='images/BGnew.jpg', size_hint=[1, 1])
for i in range(0, grid.cols * grid.rows):  # adds the transparent image to all 81 boxes
    b = Actor(id='actor' + str(i + 1), source=TransparentId, size_hint=[1, 1])
    grid.add_widget(b)

main = MainScreen(name='main')  # creates a main screen
main.add_widget(bg)  # adds background to the screen
main.add_widget(grid)  # adds grid to the scren


sm.add_widget(main)

"""
Run
"""

if __name__ == "__main__":
    commands = threading.Thread(target=communication)
    commands.start()
    try:
        MyApp().run()

    except KeyboardInterrupt:
        print("here")
        c.close_server()
