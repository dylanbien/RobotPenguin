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
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from time import sleep
from kivy.uix.behaviors import ButtonBehavior
import networkx as nx
import copy
import webbrowser

G = nx.Graph()

# from kivy.uix.widget import Widget

"""
Setup
"""

difficulty = 'easy'
chasing_player = False
cheat_code = 1

sm = ScreenManager()
Window.size = (1920, 1080)
Window.fullscreen = True
TransparentId = 'icons/ICON_Transparent.png'

"""
Arm Info
"""
x_constant = .1166
y_constant = .113

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
def endGame(result):
    global currentPos
    print(currentPos)
    arm.wait()
    currentPos[2] -= .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()
    arm.solenoid_down()
    sleep(.5)
    currentPos[2] += .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()
    sleep(.5)

    if result == 'win':
        c.send_packet(PacketType.responseCommand, b"win")
    elif result == 'lose':
        c.send_packet(PacketType.responseCommand, b"lose")
    if result == 'noTurns':
        return

    #G.clear()

def rotatorWait():
    while rotator.isBusy() == True:
        pass
    sleep(.5)

def rotate_arm(direction):
    global nextPos
    global currentPos

    currentPos[2] -= .178 # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()

    sleep(.1)

    currentPos[2] += .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()

    sleep(.1)

    print('running rotate arm ' + direction)

    if direction == 'left':
        rotator.move(200)
        print('rotating 200')
    else:
        rotator.move(-200)
        print('rotating -200')

    rotatorWait()

    sleep(.1)

    currentPos[2] -= .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()
    arm.solenoid_up()

    sleep(.1)

    currentPos[2] += .178 # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.solenoid_down()
    arm.wait()

    sleep(.3)

def move_arm():
   
    global nextPos
    global currentPos

    currentPos[2] -= .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move down
    arm.wait()
    arm.solenoid_down()

    sleep(.5)

    currentPos[2] += .178  # change z value
    arm.move_to_point_in_straight_line(currentPos[0], currentPos[1], currentPos[2], .01)  # move up
    arm.wait()
    sleep(.5)

    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move to new position
    arm.wait()

    sleep(.5)

    nextPos[2] -= .178  # change z value
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move down
    arm.wait()
    arm.solenoid_up()

    sleep(.5)

    nextPos[2] += .178
    arm.move_to_point_in_straight_line(nextPos[0], nextPos[1], nextPos[2], .01)  # move up
    arm.solenoid_down()
    arm.wait()

    sleep(.5)

    currentPos = copy.deepcopy(nextPos)

    sleep(1)
    
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
    if payload.decode("ascii") == 'outTurn':
        endGame('noTurn')
        return
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

def my_callback(dt):
    main.RefreshPopupDismiss()

def reset(dif):

    main.RefreshPopup()
    Clock.schedule_once(my_callback, 2)

    grid.do_layout()

    global difficulty
    difficulty = dif

    print('now is ' + difficulty)


    # sets possible locations of the obstacles
    easyObstacles = [
        [6, 9, 20, 21, 23, 25, 30, 32, 33, 34, 43, 45],
        [7, 9, 29, 30, 32, 33, 37, 42, 45, 47],
        [2, 7, 15, 16, 18, 20, 27, 34, 37, 45, 48],
        [5, 9, 10, 31, 33, 35, 43, 46],
        [7, 9, 18, 25, 30, 32, 42, 43, 47],
        [17, 27, 28, 39, 46]


    ]
    mediumObstacles = [
        [5, 9, 10, 12, 19, 20, 23, 24, 27, 32, 34, 35, 37, 39, 48],
        [6, 11, 13, 25, 27, 28, 32, 40, 45],
        [6, 9, 13, 29, 31, 33, 40],
        [6, 9, 27, 28, 32, 40, 43],
        [2, 7, 14, 15, 16, 17, 18, 19, 28, 33, 34, 35],
        [5, 10, 13, 16, 18, 24, 29, 32, 33, 37, 46]

    ]
    hardObstacles = [
        [4, 9, 13, 18, 19, 20, 22, 24, 32, 37, 39, 41],
        [7, 9, 18, 25, 30, 32, 34, 42, 43, 47],
        [5, 8, 9, 12, 19, 31, 32, 33, 34, 35],
        [2, 14, 15, 17, 19, 32, 34, 41, 44],
        [5, 9, 11, 13, 23, 27, 29, 33, 37, 39],
        [2, 10, 15, 18, 23, 30, 38, 41]

    ]

    main.resetBoard()

    main.addActor(1, 'players/ICON_Player_180.jpg')
    print('player is ' + str(1))

    main.addActor(49, 'icons/ICON_Goal.jpg')
    print('player is ' + str(1))

    if len(G.nodes()) > 0:
        G.clear()


    for x in range(1, 50):
        G.add_node(x)

    if (dif == 'easy'):

        temp = random.choice(easyObstacles)  # get random in in each array
        print('obstacles at')
        print(temp)
        for i in temp:

            if (i % 2 == 0):
                 main.addActor(i, 'icons/ICON_Igloo.jpg')

            else:
                 main.addActor(i, 'icons/ICON_Jewel.jpg')
            G.remove_node(i)


    if (dif == 'medium'):

        temp = random.choice(mediumObstacles)  # get random in in each array
        print('obstacles at')
        print(temp)
        for i in temp:

            if (i % 2 == 0):
                main.addActor(i, 'icons/ICON_Igloo.jpg')

            else:
                main.addActor(i, 'icons/ICON_Jewel.jpg')
            G.remove_node(i)

    if (dif == 'hard'):

        temp = random.choice(hardObstacles)  # get random in in each array
        print('obstacles at')
        print(temp)
        for i in temp:

            if (i % 2 == 0):
                main.addActor(i, 'icons/ICON_Igloo.jpg')

            else:
                main.addActor(i, 'icons/ICON_Jewel.jpg')
            G.remove_node(i)



    rows = [list(range(1, 8)), list(range(8, 15)), list(range(15, 22)), list(range(22, 29)), list(range(29, 36)),
            list(range(36, 43)), list(range(43, 50))]
    row_pairs = []
    for r in rows:
        for x in range(0, len(r) - 1):
            row_pairs.append((r[x], r[x + 1]))

    G.add_edges_from(row_pairs)

    #print(row_pairs)
    coloumn_pairs = []

    for c in range(1, 8):
        coloumn = list(range(c, 43 + c, 7))
        for x in range(0, len(coloumn) - 1):
            coloumn_pairs.append((coloumn[x], coloumn[x + 1]))

    G.add_edges_from(coloumn_pairs)

    #print("Test: Finding shortest path from 1 to 29 -  " + str(nx.shortest_path(G, source=1, target=29)))

    #print("--- " + str(G.nodes()))

    main.addActor(26, 'icons/ICON_Bear_2.jpg')


#Begins arm stuff after initializing render

    arm.home_all()
    arm.wait()
    rotator.goUntilPress(0, 1, 5000)
    arm.move_to_point_in_straight_line(0, 0, -1.52, .01)
    arm.wait()
    sleep(1)
    arm.move_to_point_in_straight_line(-.385, -.3705, -1.52, .01)
    arm.wait()
    arm.solenoid_up()
    time.sleep(0.2)
    arm.move_to_point_in_straight_line(-.385, -.3705, -1.37, .01)
    arm.wait()
    arm.solenoid_down()



    global currentPos
    global nextPos

    currentPos = [-.385, -.3705, -1.37]
    nextPos = [-.385, -.3705, -1.37]
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

    def RefreshPopup(self):
        global RefreshPop
        RefreshLay = FloatLayout()
        RefreshPop = Popup(title='refreshing',
                         size_hint=(0.375, 0.26840490797),
                         auto_dismiss=False,
                         title_size=30,
                         title_align='center',
                         content=RefreshLay)
        RefreshPop.open()

    def RefreshPopupDismiss(self):
        global RefreshPop
        RefreshPop.dismiss()

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
        temp = "actor" + str(location)
        print(temp)
        for actor in self.children[0].children:
            if (actor.id == temp):
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

        global chasing_player
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
        if fish == None:
            return
        shortest_path_from_bear_to_fish = nx.shortest_path(G, source=bear.number_as_int(), target=fish.number_as_int())
        print('shortest path from bear to fish: ' + shortest_path_from_bear_to_fish)
        if difficulty == 'easy':
            #bear_loc = bear.number_as_int()
            possible_locs = self.getAdjacentTiles(bear)
            bear.eatActor(random.choice(possible_locs))

        if difficulty == 'medium':

            if len(shortest_path_from_bear_to_fish) > 2:
                #print(str(shortest_path_from_bear_to_fish))
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
                    if len(common_locations) != 0:
                        bear.eatActor(random.choice(common_locations))
                    else:
                        return


        if (difficulty == 'hard'):
            shortest_path_from_bear_to_player = nx.shortest_path(G, source=bear.number_as_int(),
                                                                target=player.number_as_int())

            if chasing_player:
                if player == None:
                    chasing_player = False
                    return
                else:
                    bear.eatActor(shortest_path_from_bear_to_player[1])
            if len(shortest_path_from_bear_to_fish) >= len(shortest_path_from_bear_to_player): #bear is closer to player)
                bear.eatActor(shortest_path_from_bear_to_player[1])
            else: #bear is closer to the fish
               # print(str(shortest_path_from_bear_to_player) + " --- ")
                if len(shortest_path_from_bear_to_fish) == 2:
                    #bear is right next to the fish, but won't eat it, so it starts to move towards the player
                    #print('--- ' + str(shortest_path_from_bear_to_player))
                    chasing_player = True
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
        #G.add_node(self.number)

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
        global cheat_code

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

        cheat_code += 1
        if cheat_code == 4:
            webbrowser.open('https://www.youtube.com/watch?v=TFIHfiDT1mU')
    """
    Left/Right/Up/Down
    """


    def moveRight(self):  # strafe
        global nextPos

        if (sm.current != 'main'): return

        next = int(self.id.strip(string.ascii_letters)) + 1


        if (next % main.children[0].cols == 1):
            print('cant move, at the right wall')
            endGame('lose')
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
            endGame('lose')
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
            endGame('lose')
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
            endGame('lose')
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
            grid.canvas.ask_update()

            if 'Player' in actor.source:
                print('sending continue 1')
                move_arm()
                c.send_packet(PacketType.responseCommand, b"continue")

            return
        if ('Bear' in actor.source):
            self.source = TransparentId
            endGame('lose')

        elif ('Goal' in actor.source and 'Player' in self.source):  # if you next location is the fish
            actor.source = self.source
            self.source = TransparentId
            print('you win')

            move_arm()

            victory = True
            endGame('win')
            return
        elif ('Player' in self.source and 'Igloo' in actor.source):
            print('you hit an obstacle')
            endGame('lose')
            return  # can't move...you lose
        elif ('Player' in self.source and 'Jewel' in actor.source):
            print('you hit an obstacle')
            endGame('lose')
            return  # can't move...you lose

    def eatActor(self,next):
        actor = main.findActor(next)
        if 'Player' in actor.source:
            actor.source = TransparentId
            self.move(next)
            endGame('lose')
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
grid = GridLayout(id='grid', cols=7, rows=7, padding=[550, 150, 550, 150], spacing=1.5)

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
