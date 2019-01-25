'''
from kivy.config import Config
import time
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
'''
import random
#class locationRandomizer():
allObstaclesXX = [
            [2, 3],
            [11, 12],
            [15, 16],
            [20, 21],
            [25],
            [28, 37],
            [31, 40],
            [39, 41],
            [44, 45],
            [46, 33],
]

allObstacles = [
            [2, 3],
            [11, 12],
            [15, 16],
            [20, 21],
            [25],
            [28, 31],
            [33, 37],
            [39, 40],
            [41, 44],
            [45, 46],
]
# assignedObstacleLocations = []
#print("work?")
def locationRandomizer():
    assignedObstacleLocations = []
    for temp in allObstacles: # for temp in allObstaclesXX
        y = random.randint(0, len(temp) - 1)  # get random int in each array
        saved = temp[y]
        assignedObstacleLocations.append(saved)
        start = 2
        output = "p  "
        lastValue = 0
        for index in range(len(assignedObstacleLocations)):
            # print("=== " + str(start) + " " + str(value))
            value = assignedObstacleLocations[index]
            for i in range(start, value):
                output += "o  "
                if i % 7 == 0:
                    print(output)
                    output = ""
            output += "x  "
            if value % 7 == 0:
                print(output)
                output = ""
            start = value + 1
            lastValue = value
        for index in range(lastValue, 48):
            output += "o  "
        output += "f"
        print(output)
    print('obstacles at')
    print(assignedObstacleLocations)
    '''
    for i in range(len(assignedObstacleLocations)):
        if 2 in assignedObstacleLocations:
            print('p  x  o  o  o  o  o')
        if 3 in assignedObstacleLocations:
            print('p  o  x  o  o  o  o')
        if 11 in assignedObstacleLocations:
            print('o  o  o  x  o  o  o')
        if 12 in assignedObstacleLocations:
            print('o  o  o  o  x  o  o')
        if 15 in assignedObstacleLocations and 20 in assignedObstacleLocations:
            print('x  o  o  o  o  x  o')
        if 15 in assignedObstacleLocations and 21 in assignedObstacleLocations:
            print('x  o  o  o  o  o  x')
        if 16 in assignedObstacleLocations and 20 in assignedObstacleLocations:
            print('o  x  o  o  o  x  o')
        if 16 in assignedObstacleLocations and 21 in assignedObstacleLocations:
            print('o  x  o  o  o  o  x')
        if 25 in assignedObstacleLocations and 28 in assignedObstacleLocations:
            print('o  o  o  x  o  o  x')
        if 25 in assignedObstacleLocations and 28 not in assignedObstacleLocations:
            print('o  o  o  x  o  o  o')
        if 31 in assignedObstacleLocations and 33 in assignedObstacleLocations:
            print('o  o  x  o  x  o  o')
        if 31 in assignedObstacleLocations and 33 not in assignedObstacleLocations:
            print('o  o  x  o  o  o  o')
        if 31 not in assignedObstacleLocations and 33 in assignedObstacleLocations:
            print('o  o  o  o  x  o  o')
        if 31 not in assignedObstacleLocations and 33 not in assignedObstacleLocations:
            print('o  o  o  o  o  o  o')
        if 39 in assignedObstacleLocations and 37 not in assignedObstacleLocations and 40 not in assignedObstacleLocations:
            print('o  o  o  x  o  o  o')
        if 41 in assignedObstacleLocations and 37 not in assignedObstacleLocations and 40 not in assignedObstacleLocations:
            print('o  o  o  o  o  x  o')
        if 37 in assignedObstacleLocations and 39 in assignedObstacleLocations and 40 not in assignedObstacleLocations:
            print('o  x  o  x  o  o  o')
        if 37 in assignedObstacleLocations and 41 in assignedObstacleLocations and 40 not in assignedObstacleLocations:
            print('o  x  o  o  o  x  o')
        if 37 in assignedObstacleLocations and 40 in assignedObstacleLocations and 39 not in assignedObstacleLocations:
            print('o  x  o  o  x  x  o')
        if 37 not in assignedObstacleLocations and 39 in assignedObstacleLocations and 40 in assignedObstacleLocations:
            print('o  o  o  x  x  o  o')
        if 37 not in assignedObstacleLocations and 40 in assignedObstacleLocations and 41 in assignedObstacleLocations:
            print('o  o  o  o  x  x  o')
        if 37 in assignedObstacleLocations and 39 in assignedObstacleLocations and 40 in assignedObstacleLocations:
            print('o  x  o  x  x  o  o')
        if 44 in assignedObstacleLocations and 46 not in assignedObstacleLocations:
            print('o  x  o  o  o  o  f')
        if 45 in assignedObstacleLocations and 46 not in assignedObstacleLocations:
            print('o  o  x  o  o  o  f')
        if 44 in assignedObstacleLocations and 46 in assignedObstacleLocations:
            print('o  x  o  x  o  o  f')
        if 45 in assignedObstacleLocations and 46 in assignedObstacleLocations:
            print('o  o  x  x  o  o  f')
            
    for i in assignedObstacleLocations:

        if (actor.id == 'actor' + str(i)):  # assigns jewels id to actor + obstacle
            if (i % 2 == 0):
                actor.source = 'icons/ICON_Igloo.jpg'
                # actor.remove_node()

            else:
                actor.source = 'icons/ICON_Jewel.jpg'