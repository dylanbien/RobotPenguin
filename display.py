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
x_constant = .02  # work on
y_constant = .02

Motor1 = DeltaArm.MotorConfig.createMotor(0, 120, -1750, -26750)
Motor2 = DeltaArm.MotorConfig.createMotor(1, 240, -980, -26800)
Motor3 = DeltaArm.MotorConfig.createMotor(2, 360, -2000, -27000)
DeltaArmConfig = DeltaArm.DeltaArmConfig.createConfig(12.5 / 12.0, 17.8 / 12.0, 7.5 / 12.0, 6.148 / 12.0, 0)

arm = DeltaArm.DeltaArm(Motor1, Motor2, Motor3, DeltaArmConfig)

arm.home_all()  # homes it
arm.move_to_point_in_straight_line(0, 0, -1.34, .01)
currentPos = [0, 0, -1.34]
nextPos = [0, 0, -1.34]

count = 0

# def rotate_arm():
def wait():
    while arm.movement_complete() == False:
        pass
    print('done movng') 
    

def move_arm():
    global count
    count += 1
    if count %2 == 0:
        arm.move_to_point_in_straight_line(0, 0, -1.4, .01)
    else:
        arm.move_to_point_in_straight_line(-.55, -.35, -1.4, .01)
    
    wait()
    
    '''
    global nextPos
    global currentPos

    currentPos[2] -= .25  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    currentPos[2] += .25  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up

    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move to new position

    nextPos[2] -= .25  # change z value
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move down
    nextPos[2] += .25
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move up

    wait()

    currentPos = Cloning(nextPos)
    '''

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

    
    
    global currentPos
    global nextPos
    
    #arm.home_all()  # homes it
    #arm.move_to_point_in_straight_line(0, 0, -1.34, .01)
    #currentPos = [0, 0, -1.34]
    #nextPos = [0, 0, -1.34]
    # sets possible locations of the obstacles
    allObstacles = [
        [2, 3, 4, 5],
        [15, 16, 24, 25],
        [20, 21],
        [28, 37],
        [31, 40, 41, 42],
        [35, 44],
        [47],
        

    ]

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
    actorGoal.source = '/ICON_Goal.jpg'

    actorPenguin = maiiconsn.findActor(locPenguin)  # places penguin
    print('player is ' + str(locPenguin))
    actorPenguin.source = 'players/ICON_Player_180.jpg'

    actors = list(main.children[0].children)[::-1]  # reverses in correct order
    #for x in range(1, 81):
        #if actors[x].number_as_int() in [55, 46, 37, 28, 19, 10, 1]:  # edge numbers
       #     x = x + 1
       # G.add_edge(actors[x - 1].number_as_int(), actors[x].number_as_int())

    #for j in range(1, 45):
       # if actors[j].number_as_int() in [9, 27, 45]:  # edge numbers
        #    j = j + 9
       # G.add_edge(actors[j].number_as_int(), actors[j + 9].number_as_int())

    #for k in range(45, 72):
       # G.add_edge(actors[k].number_as_int(), actors[k + 9].number_as_int())

    # print("Test: Finding shortest path from 1 to 29 -  " + str(nx.shortest_path(G, source=1, target=29)))

    for actor in main.children[0].children:

        for i in assignedObstacleLocations:

            if (actor.id == 'actor' + str(i)):  # assigns jewels id to actor + obstacle
                if (i % 2 == 0):
                    actor.source = 'icons/ICON_Igloo.jpg'

                else:
                    actor.source = 'icons/ICON_Jewel.jpg'

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
        print('movemnt' + movement)
        if movement == 'forward':
            self.playerForward()
        else:
            self.playerBackward()

    def playerForward(self):  # just find the location of the player
        print('you have moved the player forwards')
        for actor in main.children[0].children:  # loops through all actors
            if ('Player' in actor.source):  # if an actors source has the word plater in it
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


    """
    Hunt Player
    """


    def huntPlayer(self):
        global difficulty
        global turn
        print('turn is ' + str(turn) + ', so moving twice will be ' + str(turn % 2 == 0))
        # getting the bear actor
        bear = None
        for b in self.children[0].children:
            if 'Bear' in b.source:
                bear = b

        if difficulty == 'easy':
            bear_loc = bear.number_as_int()
            possible_locs = [(bear_loc + x) for x in [1, -1, 13, -13]]

        if (difficulty == 'hard'):
            print('difficulty is hard')
            for hunter in self.children[0].children:
                if ('Bear' in hunter.source):
                    hunter.goTowards()
                    break
        else:
            for hunter in self.children[0].children:
                if 'Bear' in hunter.source:
                    hunter.goTowards()
                    break


"""
Actor Class
"""


class Actor(ButtonBehavior, AsyncImage):  # creates an actor class

    def __init__(self, *args, **kwargs):
        AsyncImage.__init__(self, *args, **kwargs)
        self.number = ''.join(i for i in self.id if i.isdigit())
        if (('Transparent' in self.source) or ('Player' in self.source)):
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
            # main.huntPlayer()

            return
        elif ('180' in self.source):  # down
            self.moveDown()
            # .huntPlayer()
            return
        elif ('270' in self.source):  # left
            self.moveLeft()
            # main.huntPlayer()
            return
        else:  # up
            self.moveUp()
            # main.huntPlayer()
            return

    def moveBackward(self):
        if ('90' in self.source):
            self.moveLeft()
            # main.huntPlayer()
            return
        elif ('180' in self.source):
            self.moveUp()
            # main.huntPlayer()
            return
        elif ('270' in self.source):
            self.moveRight()
            # main.huntPlayer()
            return
        else:
            self.moveDown()
            # main.huntPlayer()
            return

    """
    Left/Right/Up/Down
    """


    def moveRight(self):  # strafe
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) + 1
        print(str(next))

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
        print(str(next))

        if (next % main.children[0].cols == 0):
            print('cant move, at the left wall')
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:
            nextPos[0] += x_constant
            self.move(next)


    """
    move
    """


    def moveUp(self):
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) - main.children[0].cols
        print(next)

        if (next < 0):
            print('cant move, at the top wall')
            c.send_packet(PacketType.responseCommand, b"lose")
            return
        else:
            nextPos[1] += y_constant
            self.move(next)


    def moveDown(self):
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) + main.children[0].cols
        print(next)

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
        print(actor.id)
        assert actor.id == "actor" + str(next)

        if (actor.source == TransparentId):
            print('can move')  # if next spot is clear
            temp = self.source
            self.source = actor.source
            actor.source = temp
            print('sending continue')

            move_arm()

            c.send_packet(PacketType.responseCommand, b"continue")
            return

        elif ('Goal' in actor.source and 'Player' in self.source):  # if you next location is the fish
            actor.source = self.source
            self.source = TransparentId
            print('you win')

            move_arm()

            c.send_packet(PacketType.responseCommand, b"win")
            return


        elif ('Player' in self.source and 'Igloo' in actor.source):
            print('you hit an obstacle')
            return  # can't move...you lose


# ////////////////////////////////////////////////////////////////////////////
# //						        	Rotate Actor 				    	//
# ////////////////////////////////////////////////////////////////////////////

    def rotateDegrees(self, location, degrees):
        if (sm.current != 'main'): return
        for actor in main.children[0].children:
            if (actor.id == location and 'Player' in actor.source):
                if (degrees == 0 or degrees == 360 or degrees % 90 != 0):
                    actor.source = 'players/ICON_Player.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                elif (degrees > 360):
                    actor.source = 'players/ICON_Player_' + str(degrees % 360) + '.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    actor.source = 'players/ICON_Player_' + str(degrees) + '.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")


    def rotateDirection(self, direction):
        if (sm.current != 'main'): return

        print('direction = ' + direction)
        print('source = ' + self.source)
        if (direction == 'left' and self.source == 'players/ICON_Player.jpg'):  # if main icon
            self.source = 'players/ICON_Player_270.jpg'
            print('degree = 270')
            print('sending continue')
            move_arm()
            # rotate_arm()

            c.send_packet(PacketType.responseCommand, b"continue")
            return
        elif (direction == 'right' and self.source == 'players/ICON_Player.jpg'):  # if main icon
            self.source = 'players/ICON_Player_90.jpg'
            print('degree = 90')
            print('sending continue')
            move_arm()
            # rotate_arm()

            c.send_packet(PacketType.responseCommand, b"continue")
            return
        else:
            degree = int(self.source.strip(string.ascii_letters + string.punctuation))
            print('degree = ' + str(degree))
            if (direction == 'left'):
                angle = str(((degree + 270) % 360))
                print('new angle = ' + angle)
                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                move_arm()
                # rotate_arm()

            else:
                angle = str(((degree + 90) % 360))
                print('new angle = ' + angle)
                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                else:
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
                    print('sending continue')
                    c.send_packet(PacketType.responseCommand, b"continue")
                move_arm()
                # rotate_arm()


Window.clearcolor = (0.1, 0.1, 0.1, 1)  # (WHITE)

"""
Create grid/actors
"""

# creates a 9 * 9 grid
grid = GridLayout(id='grid', cols=7, rows=7, padding=[380, 150, 450, 150], spacing=1.5)

# sets the background image
bg = AsyncImage(source='images/BG.jpg', size_hint=[1, 1])
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
