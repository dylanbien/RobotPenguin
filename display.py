from kivy.config import Config

Config.set('graphics', 'resizable', False)

import os
os.environ["DISPLAY"] = ":0.0"
import string
import random
import socket
import sys
import math
import DeltaArm
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from time import sleep
from kivy.uix.behaviors import ButtonBehavior
import networkx as nx
G = nx.Graph()

from kivy.uix.widget import Widget


# ////////////////////////////////////////////////////////////////
# //	                		Set Up			    			//
# ////////////////////////////////////////////////////////////////

difficulty = 'easy'
locPenguin = 1 #sets starting location of the penguin
locGoal = [81,81,81] #location of the fish

sm = ScreenManager()
Window.size = (1920, 1080)
Window.fullscreen = True
TransparentId = 'icons/ICON_Transparent.png'



arm = DeltaArm.DeltaArm(0, 1, 2) #creates arm
arm.home_all() #homes it
current = [0,0, -1.34]
direction = 0

# ////////////////////////////////////////////////////////////////
# //	                		Server			    			//
# ////////////////////////////////////////////////////////////////
import enum
from dpea_p2p import Client
from apscheduler.schedulers.background import BackgroundScheduler

class PacketType(enum.Enum):
    NULL = 0
    difficulty = 1
    move = 2
    commandResponse = 3

#         |Server IP     |Port |Packet enum
c = Client("172.17.21.2", 5001, PacketType)
c.connect()

def check_server():

    if c.recv_packet() == (PacketType.difficulty, b"easy"):
        reset('easy')
    elif c.recv_packet() == (PacketType.difficulty, b"medium"):
        reset('medium')
    elif c.recv_packet() == (PacketType.difficulty, b"hard"):
        reset('hard')

    if recv_packet() == (PacketType.move, b"forward"):
        main.playerForward()
    elif recv_packet() == (PacketType.move, b"backward"):
        main.playerBackward()
    elif recv_packet() == (PacketType.move, b"left"):
        main.playerRotate('left')
    elif recv_packet() == (PacketType.move, b"right"):
        main.playerRotate('right')


check_server = BackgroundScheduler()
check_server.add_job(check_server, 'interval', seconds = .001)

# ////////////////////////////////////////////////////////////////
# //	               		Reset Function			    		//
# ////////////////////////////////////////////////////////////////


def reset(dif):

    difficulty = dif

    print('now is ' + difficulty)
    
    grid.clear_widgets()
    
   
    #sets possible locations of the obstacles
    allObstacles = [
    [3,4, 5, 6],
    [27, 28,40 ,41],
    [66, 79],
    [43, 44, 57],
    [80, 79, 72],
    [33, 34, 46, 47],
    [10, 23, 36],
    [61,62,74,75],
    [66,67],
    [25, 38, 51]#,
    #[52, 65, 78 ],

    ]

    assignedObstacleLocations = []

    for i in range(0, grid.cols * grid.rows): #resets all 81 grids to transparent
        b = Actor(id='actor' + str(i + 1), source=TransparentId, size_hint=[1, 1])
        grid.add_widget(b)

    for temp in allObstacles:
        y = random.randint(0, len(temp)-1) #get random in in each array
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
    
    actorGoal =   main.findActor(assignedGoal) # assigns goal id
    print('goal is ' + str((assignedGoal)))
    actorGoal.source = 'icons/ICON_Goal.jpg'

        
    actorPenguin = main.findActor(locPenguin)   #places penguin                
    print('player is ' + str(locPenguin))
    actorPenguin.source = 'players/ICON_Player_180.jpg'


    for actor in main.children[0].children:
        if (actor.id == 'actor' + str(locPenguin)): #places penguin
            print('player is ' + str(locPenguin))
            #actor.source = 'players/ICON_Player_180.jpg'

        if (actor.id == 'actor' + str(assignedGoal)):  # assigns goal id to actor + obstacle
            print('goal is ' + str((locGoal)))
            #actor.source = 'icons/ICON_Goal.jpg'


    actors = list(main.children[0].children)[::-1]#reverses in correct order
    for x in range(1, 81):
        if actors[x].number_as_int() in [55,46,37,28,19,10,1]:  # edge numbers
            x = x + 1
        G.add_edge(actors[x-1].number_as_int(), actors[x].number_as_int())

    for j in range(1, 45):
        if actors[j].number_as_int() in [9, 27, 45]:  # edge numbers
            j = j + 9
        G.add_edge(actors[j].number_as_int(), actors[j+9].number_as_int())

    for k in range(45,72):
        G.add_edge(actors[k].number_as_int(), actors[k+9].number_as_int())

    #print("Test: Finding shortest path from 1 to 29 -  " + str(nx.shortest_path(G, source=1, target=29)))



    for actor in main.children[0].children:

        for i in assignedObstacleLocations:

            if (actor.id == 'actor' + str(i)):  # assigns jewels id to actor + obstacle
                print('jewel/igloo is ' + str(i))
                if (i%2 == 0):
                    actor.source = 'icons/ICON_Igloo.jpg'

                else:
                    actor.source = 'icons/ICON_Jewel.jpg'
                
    arm.move_to_point(0,0, -1.34)

# ////////////////////////////////////////////////////////////////
# //	               		MyApp creation			    		//
# ////////////////////////////////////////////////////////////////
    
class MyApp(App):
    
    def build(self):
       #Clock.schedule_interval(obey, .1)
        return sm

    def quitAll():
        quit()


# ////////////////////////////////////////////////////////////////////////////
# //						    	Main Screen 							//
# ////////////////////////////////////////////////////////////////////////////

class MainScreen(Screen):


    def findActor(self, ActorIndex):
        return self.children[0].children[len(self.children[0].children) - ActorIndex]
    
    def exitProgram(self):
        App.get_running_app().stop()
        Window.close()

    #Replaces every image with a blank image
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

# ////////////////////////////////////////////////////////////////////////////
# //						    	Player move 							//
# ////////////////////////////////////////////////////////////////////////////

    def playerForward(self): #just find the location of the player
        print('you have moved the player forwards')
        for actor in main.children[0].children: #loops through all actors
            if ('Player' in actor.source): #if an actors source has the word plater in it
                actor.moveForward() #(players/ICON_Player.jpg) > name of player
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

# ////////////////////////////////////////////////////////////////////////////
# //						    	Hunt Player 							//
# ////////////////////////////////////////////////////////////////////////////

    def huntPlayer(self):
        global difficulty
        global turn
        print('turn is ' + str(turn) + ', so moving twice will be ' + str(turn % 2 == 0))
        #getting the bear actor
        bear = None
        for b in self.children[0].children:
            if 'Bear' in b.source:
                bear = b


        if difficulty == 'easy':
            bear_loc = bear.number_as_int()
            possible_locs = [(bear_loc+x) for x in [1, -1, 13, -13]]
            

        if (difficulty == 'hard'):
            print('difficulty is hard')
            for hunter in self.children[0].children:
                if ('Bear' in hunter.source):
                    hunter.goTowards();
                    break
        else:
            for hunter in self.children[0].children:
                if ('Bear' in hunter.source):
                    hunter.goTowards();
                    break

# ////////////////////////////////////////////////////////////////////////////
# //						    	Actor Class 							//
# ////////////////////////////////////////////////////////////////////////////

class Actor(ButtonBehavior, Image): #creates an actor class

    def __init__(self,*args,**kwargs):
        Image.__init__(self,*args,**kwargs)
        self.number = ''.join(i for i in self.id if i.isdigit())
        if(('Transparent' in self.source) or ('Player' in self.source)):
            G.add_node(self.number)

    def remove_node(self):
        G.remove_node(self.number)

    def number_as_int(self):
        return int(self.number)

    def on_press(self): #when button is pressed
        print('pressed' + str(self.id))

# ////////////////////////////////////////////////////////////////////////////
# //						        	Move Actor 							//
# ////////////////////////////////////////////////////////////////////////////

    def moveForward(self): #find out which image is on the screen
        #there are different images for the player based on the direction they are facing 
        
        if ('90' in self.source): #right
            self.moveRight()
            #main.huntPlayer()
            
            return
        elif ('180' in self.source): #down
            self.moveDown()
            #.huntPlayer()
            return
        elif ('270' in self.source): #left
            self.moveLeft()
            #main.huntPlayer()
            return
        else:                        #up
            self.moveUp()
            #main.huntPlayer()
            return

    def moveBackward(self):
        if ('90' in self.source):
            self.moveLeft()
            #main.huntPlayer()
            return
        elif ('180' in self.source):
            self.moveUp()
            #main.huntPlayer()
            return
        elif ('270' in self.source):
            self.moveRight()
            #main.huntPlayer()
            return
        else:
            self.moveDown()
            #main.huntPlayer()
            return
   
    def rotateDegrees(self, location, degrees):
        if (sm.current != 'main'): return
        for actor in main.children[0].children:
            if (actor.id == location and 'Player' in actor.source):
                if (degrees == 0 or degrees == 360 or degrees % 90 != 0):
                    actor.source = 'players/ICON_Player.jpg'
                elif (degrees > 360):
                    actor.source = 'players/ICON_Player_' + str(degrees % 360) + '.jpg'
                else:
                    actor.source = 'players/ICON_Player_' + str(degrees) + '.jpg'
    
    def rotateDirection(self, direction):
        if (sm.current != 'main'): return
        
        print( 'direction = '  + direction)
        print( 'source = ' + self.source)
        if (direction == 'left' and self.source == 'players/ICON_Player.jpg'): #if main icon
            self.source = 'players/ICON_Player_270.jpg'
            print ('degree = 270')
            return
        elif (direction == 'right' and self.source == 'players/ICON_Player.jpg'): #if main icon
            self.source = 'players/ICON_Player_90.jpg'
            print ('degree = 90')
            return
        else:
            degree = int(self.source.strip(string.ascii_letters + string.punctuation))
            print ('degree = ' + str(degree))
            if (direction == 'left'):
                angle = str(((degree + 270) % 360))
                print('new angle = ' + angle)
                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                else: 
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
            else:
                angle = str(((degree + 90) % 360))
                print('new angle = ' + angle)
                if (angle == '0'):
                    self.source = 'players/ICON_Player.jpg'
                else: 
                    self.source = 'players/ICON_Player_' + angle + '.jpg'
                
            
    def moveRight(self):  # strafe
        if (sm.current != 'main'): return
        
        next = int(self.id.strip(string.ascii_letters)) + 1
        print(str(next))
        
        if (next % main.children[0].cols == 1):
            print('cant move, at the right wall')
            return
        else:
            self.move(next)

    def moveLeft(self):  # strafe
        if (sm.current != 'main'): return
        
        next = int(self.id.strip(string.ascii_letters)) - 1
        print(str(next))
        
        if (next % main.children[0].cols == 0):
            print('cant move, at the left wall')
            return
        else:
            self.move(next)

    def moveUp(self):
        if (sm.current != 'main'): return
        
        next = int(self.id.strip(string.ascii_letters)) - main.children[0].cols
        print(next)
        
        if (next < 0):
            print('cant move, at the top wall')
            return
        else:
            self.move(next)

    def moveDown(self):
        if (sm.current != 'main'): return
        
        next = int(self.id.strip(string.ascii_letters)) + main.children[0].cols
        print(next)

        
        if (next > main.children[0].rows * main.children[0].cols):
            print('cant move, at the bottom wall')
            return
        else:
            self.move(next)


    #gets called in all the directional moves
    def move(self, next):
        
        actor = main.findActor(next) #gets the with id value next
        print(actor.id)
        assert actor.id == "actor" + str(next)
        
        print(actor.id+ 'pt 2')
        
        if (actor.source == TransparentId):
            print('can move') #if next spot is clear
            temp = self.source
            self.source = actor.source
            actor.source = temp
            #arm.move() move the arm based on how its facing...find in source name
            return
            
        elif ('Goal' in actor.source and 'Player' in self.source): #if you next location is the fish
            actor.source = self.source
            self.source = TransparentId
            print('you win')
            return 
                
                
        elif ('Player' in self.source and 'Igloo' in actor.source ):
            print('you hit an obstacle')
            return #can't move...you lose
    


Window.clearcolor = (0.1, 0.1, 0.1, 1)  # (WHITE)

# ////////////////////////////////////////////////////////////////
# //					 CREATE GRID/ACTORS                 	//
# ////////////////////////////////////////////////////////////////


#creates a 9 * 9 grid
grid = GridLayout(id='grid', cols=9, rows=9, padding=[340,0,340,0], spacing=1.5) 

#sets the background image
bg = Image(source='images/BG.jpg', size_hint=[1.1, 2])
for i in range(0, grid.cols * grid.rows): #adds the transparent image to all 81 boxes
    b = Actor(id='actor' + str(i + 1), source=TransparentId, size_hint=[1, 1])
    grid.add_widget(b)

main = MainScreen(name='main') #creates a main screen
main.add_widget(bg) #adds background to the screen
main.add_widget(grid) #adds grid to the scren

main.resetBoard()

sm.add_widget(main)

# ////////////////////////////////////////////////////////////////
# //				  Run main function                     	//
# ////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    try:
        check_server.start()
    except (KeyboardInterrupt, SystemExit):
        check_server.shutdown()
    MyApp().run()

