# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
#all wrenches are jewels, 扳手皆為寶石
from kivy.config import Config
Config.set('graphics', 'resizable', False)
import string
import random
import socket
import sys
import re
import math
import time
from random import randint
from kivy.app import App
from kivy.uix import togglebutton
from kivy.uix.widget import Widget
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.loader import Loader
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.graphics import *
from functools import partial
from kivy.uix.behaviors import ButtonBehavior

# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////
difficulty = 'normal'
turn = 1
canWin = False
sm = ScreenManager()
Window.size = (939, 939)

class MyApp(App):
	def build(self):
		Clock.schedule_interval(obey, .1)
		return sm
def obey(self, retry = 5):
	data = ''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('172.17.17.116', 10009)
	print('connecting to {} port {}'.format(*server_address))
	sock.connect(server_address)
	print('i am display.py')
	sock.sendall(b'?')
	spaceReceived = False
	try:
		while (not spaceReceived):
			request = sock.recv(16).decode()
			data += request
			if (' ' in data): spaceReceived = True
	except OSError:
		if(retry >= 0): obey(retry - 1)
				
	if (data == 'bupkis '):
		return
	print('received {!r}'.format(data))
	if (data == 'forward '):
		main.playerForward()
	elif (data == 'backward '):
		main.playerBackward()
	elif (data == 'left '):
		main.playerRotate('left')
	elif (data == 'right '):
		main.playerRotate('right')
	else:
		print ('fail')
		return
		
def quitAll():
	quit()
	
def reset(dif):
	global turn
	global difficulty
	global canWin
	canWin = False
	print ('difficulty was ' + difficulty)
	difficulty = dif
	print ('now is ' + difficulty)
	turn = 1
	testIndex = 0
	grid.clear_widgets()
	possible = []
	test = random.sample(range(1, 82), 81)
	locs = random.sample(range(1, 82), 4)
	banned = [locs[0] + 1, locs[0] - 1, locs[0] + 9, locs[0] - 9, locs[0] - 10, locs[0] - 8, locs[0] + 10, locs[0] + 8, locs[0], locs[1], locs[2], locs[3]]
	edges = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 28, 37, 46, 55, 64, 73, 74, 75, 76, 77, 78, 79, 80, 81, 18, 27, 36, 45, 54, 63, 72] # will sometimes contain locations of other things
	obstacles = []
	
	while len(obstacles) < 3: 
		x = random.randint(1, 81)
		if x not in edges and x != locs[0]:
			obstacles.append(x)
			edges.append(x)
	print (obstacles)
		 
	for i in range (0, grid.cols*grid.rows):
		b = Actor(id = 'actor' + str(i+1), source = 'ICON_Transparent.png', size_hint = [None, None])
		grid.add_widget(b)
		
	for actor in main.children[0].children:
		if (actor.id == 'actor' + str(locs[0])):
			print ('player is ' + str(locs[0]))
			actor.source = 'ICON_Player.png'
			
		if (actor.id == 'actor' + str(obstacles[0])):
			print ('jewel/wrench is ' + str(obstacles[0]))
			actor.source = 'ICON_Jewel.png'
			
		if (actor.id == 'actor' + str(obstacles[1])):
			print ('igloo is ' + str(obstacles[1]))
			actor.source = 'ICON_Igloo.png'
		
		if (actor.id == 'actor' + str(obstacles[2])):
			print ('gear is ' + str(obstacles[2]))
			actor.source = 'ICON_Gear.png'
			
	while testIndex < 81:
		for actor in main.children[0].children:
			print ('test index first ' + str(testIndex) + ' number is ' + str(test[testIndex]))
			if ('Transparent' in actor.source and test[testIndex] not in banned and str(test[testIndex]) in actor.id): possible.append(test[testIndex]); break
		testIndex +=1			
	print (possible)
	if len(possible) > 0: pos = random.randint(0, len(possible) - 1)
	else: pos = 0
	print ('pos is ' + str(pos) + ', will be set here ' + str(possible[pos]))
	
	for actor in main.children[0].children:
		if (actor.id == 'actor' + str(possible[pos])): actor.source = 'ICON_Bear.png'; print ('have set'); break
		
	sm.current = 'main'
	

# ////////////////////////////////////////////////////////////////////////////
# //	DECLARE APP, MAINSCREEN, ACTOR CLASSES/METHODS AND SCREENMANAGER	//				
# //							LOAD KIVY FILE								//			
# ////////////////////////////////////////////////////////////////////////////
# all args are passed in string form. locations are 'actor1', 'actor2', 'actor3', etc. types are 'ICON_Igloo.png', 'ICON_Wrench.png', etc.
class MainScreen(Screen):
	def exitProgram(self, obj):
		App.get_running_app().stop()
		Window.close()
	def resetBoard(self):
		for actor in self.children[0].children:
			actor.source = 'ICON_Transparent.png'
	def addActor(self, location, type): 
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = type
	def removeActor(self, location):
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = 'ICON_Transparent.png'
	def test(self, dt):
		for actor in self.children[0].children:
			if (actor.source != 'ICON_Transparent.png'):
				actor.random()
	def playerForward(self):
		print('you have moved the player forwards or something')
		for actor in main.children[0].children:
			if ('Player' in actor.source):
				actor.moveForward()
				return
	
	def playerBackward(self):
		print('you have moved the player backwards or something')
		for actor in self.children[0].children:
			if ('Player' in actor.source):
				actor.moveBackward()
				return
	
	def playerRotate(self, direction):
		print('you have rotated the player ' + direction)
		for actor in self.children[0].children:
			if('Player' in actor.source):
				actor.rotateDirection(direction)
				return
				
	def huntPlayer(self):
		global difficulty
		global turn
		print ('turn is ' + str(turn) + ', so moving twice will be ' + str(turn % 2 == 0))
		if (difficulty == 'hard'):
			print ('difficulty is hard')
			if (turn % 2 == 0):
				for hunter in self.children[0].children:
					if ('Bear' in hunter.source): 
						hunter.goTowards(); break
				for hunter in self.children[0].children:
					if ('Bear' in hunter.source): 
						hunter.goTowards(); turn += 1; break;
			else:
				for hunter in self.children[0].children:
					if ('Bear' in hunter.source):
						hunter.goTowards(); turn += 1; break
		else:
			for hunter in self.children[0].children:
				if ('Bear' in hunter.source): 
					hunter.goTowards(); break
				
class Actor(ButtonBehavior, Image):
	def on_press(self):
		print('pressed')
		
	def test(self, dt):
		if ('Player' not in self.source): return
		self.rotate(self.id, 90*random.randint(0, 3))
		self.moveForward()
		
	def moveForward(self):
		if ('90' in self.source): self.moveRight(); main.huntPlayer(); return
		elif ('180' in self.source): self.moveDown(); main.huntPlayer(); return
		elif ('270' in self.source): self.moveLeft(); main.huntPlayer(); return
		else: self.moveUp(); main.huntPlayer(); return
	
	def moveBackward(self):
		if ('90' in self.source): self.moveLeft(); main.huntPlayer(); return
		elif ('180' in self.source): self.moveUp(); main.huntPlayer(); return
		elif ('270' in self.source): self.moveRight(); main.huntPlayer(); return
		else: self.moveDown(); main.huntPlayer(); return
		
	def loser(self, *args):
		app = App.get_running_app()
		app.root.current = "Loser"
			
	def random(self):
		if ('Player' not in self.source):
			return
		index = random.randint(1,4)
		if index == 1:
			self.moveRight()
		elif index == 2:
			self.moveLeft()
		elif index == 3:
			self.moveUp()
		else:
			self.moveDown()
	
	def rotateDegrees(self, location, degrees):
		if (sm.current != 'main'): return
		for actor in main.children[0].children:
			if (actor.id == location and 'Player' in actor.source):
				if (degrees == 0 or degrees == 360 or degrees % 90 != 0): actor.source = 'ICON_Player.png'
				elif (degrees > 360): actor.source = 'ICON_Player_' + str(degrees%360) + '.png'
				else: actor.source = 'ICON_Player_' + str(degrees) + '.png'
				
	def rotateDirection(self, direction):
		if (sm.current != 'main'): return
		if (direction == 'left' and self.source == 'ICON_Player.png'): 
			self.source = 'ICON_Player_270.png'
			return
		elif (direction == 'right' and self.source == 'ICON_Player.png'):
			self.source = 'ICON_Player_90.png'
			return
		else:
			degree = int(self.source.strip(string.ascii_letters + string.punctuation))
			if (direction == 'left'): self.source = 'ICON_Player_' + str(((degree + 270) % 360)) + '.png'
			else: self.source = 'ICON_Player_' + str(((degree + 90) % 360)) + '.png'
			if (self.source == 'ICON_Player_0.png'): self.source = 'ICON_Player.png'
		
	def moveRight(self): #strafe
		global canWin
		if (sm.current != 'main'): return
		next = int(self.id.strip(string.ascii_letters)) + 1
		if (next % main.children[0].cols == 1):
			return
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Transparent.png'):
				temp = self.source; self.source = actor.source; actor.source = temp; return
			elif (actor.id == 'actor' + str(next) and 'Player' in actor.source and 'Bear' in self.source and sm.current != 'Winner'):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Bear' in actor.source and 'Player' in self.source and sm.current != 'Winner'):
				self.source = actor.source; actor.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Gear' in actor.source and 'Player' in self.source):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				canWin = True
			elif (actor.id == 'actor' + str(next) and 'Jewel' in actor.source and 'Player' in self.source and canWin):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				sm.current = 'Winner'
	
	def moveLeft(self): #strafe
		global canWin
		if (sm.current != 'main'): return
		next = int(self.id.strip(string.ascii_letters)) - 1
		if (next % main.children[0].cols == 0):
			return
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Transparent.png'):
				temp = self.source; self.source = actor.source; actor.source = temp; return
			elif (actor.id == 'actor' + str(next) and 'Player' in actor.source and 'Bear' in self.source and sm.current != 'Winner'):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Bear' in actor.source and 'Player' in self.source and sm.current != 'Winner'):
				self.source = actor.source; actor.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Gear' in actor.source and 'Player' in self.source):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				canWin = True
			elif (actor.id == 'actor' + str(next) and 'Jewel' in actor.source and 'Player' in self.source and canWin):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				sm.current = 'Winner'
	
	def moveUp(self):
		global canWin
		if (sm.current != 'main'): return
		next = int(self.id.strip(string.ascii_letters)) - main.children[0].rows
		print (next)
		if (next < 0):
			return 
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Transparent.png'):
				temp = self.source; self.source = actor.source; actor.source = temp; return
			elif (actor.id == 'actor' + str(next) and 'Player' in actor.source and 'Bear' in self.source and sm.current != 'Winner'):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Bear' in actor.source and 'Player' in self.source and sm.current != 'Winner'):
				self.source = actor.source; actor.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Gear' in actor.source and 'Player' in self.source):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				canWin = True
			elif (actor.id == 'actor' + str(next) and 'Jewel' in actor.source and 'Player' in self.source and canWin):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				sm.current = 'Winner'
	
	def moveDown(self):
		global canWin
		if (sm.current != 'main'): return
		next = int(self.id.strip(string.ascii_letters)) + main.children[0].rows
		if (next > main.children[0].rows*main.children[0].cols):
			return
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Transparent.png'):
				temp = self.source; self.source = actor.source; actor.source = temp; return
			elif (actor.id == 'actor' + str(next) and 'Player' in actor.source and 'Bear' in self.source and sm.current != 'Winner'):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Bear' in actor.source and 'Player' in self.source and sm.current != 'Winner'):
				self.source = actor.source; actor.source = 'ICON_Transparent.png'
				print ('you are a failure')
				Clock.schedule_once(self.loser, 1)
				#sm.current = 'Loser'
			elif (actor.id == 'actor' + str(next) and 'Gear' in actor.source and 'Player' in self.source):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				canWin = True
			elif (actor.id == 'actor' + str(next) and 'Jewel' in actor.source and 'Player' in self.source and canWin):
				actor.source = self.source; self.source = 'ICON_Transparent.png'
				sm.current = 'Winner'
		
	def goTowards(self): # if anyone wants to fix please feel free
		if (sm.current != 'main'): return
		prey = 0
		position = 0
		obstacles = []
		reverse = ''
		canX = True
		canY = True
		for actor in main.children[0].children:
			if ('Player' in actor.source): prey = 81 - main.children[0].children.index(actor)
		for hunter in main.children[0].children:
			if ('Bear' in hunter.source): position = 81 - main.children[0].children.index(hunter)
		for obstacle in main.children[0].children:
			if ('Player' not in obstacle.source and 'Bear' not in obstacle.source and 'Transparent' not in obstacle.source and 'Jewel' not in obstacle.source): loc = (81 - main.children[0].children.index(obstacle)); obstacles.append((loc % 9  if (loc % 9 != 0) else 9, math.ceil(loc / 9)))
		hunterCol = position % 9  if (position % 9 != 0) else 9 
		hunterRow = math.ceil(position / 9)
		preyCol = prey % 9 if (prey % 9 != 0) else 9
		preyRow =  math.ceil(prey / 9)
		#for tuple in obstacles: 
		#	if (tuple[0] == hunterCol + 1 or hunterCol - 1 and hunterRow == tuple[1]) and not ((tuple[0] == hunterCol + 1 and tuple[1] == hunterRow + 1) or (tuple[0] == hunterCol - 1 and tuple[1] == hunterRow - 1)): canX = False
		#for tuple in obstacles:
		#	if (tuple[1] == hunterRow + 1 or hunterRow - 1 and hunterCol == tuple[0]) and not ((tuple[0] == hunterCol + 1 and tuple[1] == hunterRow + 1) or (tuple[0] == hunterCol - 1 and tuple[1] == hunterRow - 1)): canY = False
		print ('obstacles are here:')
		print (obstacles)
		if (not canX and not canY and reverse): exec(reverse); return
		if (hunterRow > preyRow and canY):
			self.moveUp()
			reverse = 'self.moveDown()'
			return
		elif (hunterRow < preyRow and canY):
			self.moveDown()
			reverse = 'self.moveUp()'
			return
		else:
			if (hunterCol < preyCol and canX):
				self.moveRight()
				reverse = 'self.moveLeft()'
				return
			elif (hunterCol > preyCol and canX):
				self.moveLeft()
				reverse = 'self.moveRight()'
				return
			elif (hunterCol == preyCol and hunterRow == preyRow and sm.current != 'Winner'): print('lost through towards method'); Clock.schedule_once(self.loser, 1); #sm.current = 'Loser'
# ////////////////////////////////////////////////////////////////
# //															//
# //						  POPUPS							//
# //															//
# ////////////////////////////////////////////////////////////////

	def quitPop (self): # QUIT POPUP
		quitLay = FloatLayout(size_hint = (0.5, 0.5))
		quitPop = Popup(title = 'QUIT GAME',
			size_hint = (0.3, 0.23),
			auto_dismiss = True,
			title_size = 30,
			title_align = 'center',
			content = quitLay)
		yesButton = Button(text = 'YES',
			size_hint = (0.46, 0.8),
			font_size = 20,
			pos = (700, 425))
		noButton = Button(text = 'NO',
			size_hint = (0.46, 0.8),
			font_size = 20,
			pos = (965, 425))
		confirmationLabel = Label(text = 'Are you sure you want to quit?',
			pos = (685, 487.5),
			font_size = 20)
		
		yesButton.bind(on_release = self.exitProgram)
		noButton.bind(on_release = quitPop.dismiss)
		
		quitLay.add_widget(yesButton)
		quitLay.add_widget(noButton)
		quitLay.add_widget(confirmationLabel)

		quitPop.open()
		
		
#Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)
# ////////////////////////////////////////////////////////////////
# //					 CREATE GRID/ACTORS						//
# ////////////////////////////////////////////////////////////////
grid = GridLayout(id = 'grid', cols = 9, rows = 9, padding = 15, spacing = 1.5)
bg = Image(source = 'BG.png', size_hint = [1, 1])
for i in range (0, grid.cols*grid.rows):
	b = Actor(id = 'actor' + str(i+1), source = 'ICON_Transparent.png', size_hint = [None, None])
	grid.add_widget(b)

main = MainScreen(name = 'main')
main.add_widget(bg)
main.add_widget(grid)
sm.add_widget(main)
screen = Screen(name = "Winner")
youWinner = Image(source = 'winner.png')
screen.add_widget(youWinner)
loserScreen = Screen(name = "Loser")
youLoser = Image(source = 'loser.png')
loserScreen.add_widget(youLoser)
#bang = Video(source = 'bang.mp4', play = True)
#screen.add_widget(bang)
#bang님의 명복을 빌어요 T_T
winLabel = Label(text = 'You win!', font_size = 64, pos = (0, 400))
#korWinLabel = Label(text = '이기셨네요!', font_size = 32, pos = (0, 350), font_name = 'Malgun Gothic.ttf') 
loseLabel = Label(text = 'You lost.', font_size = 64, pos = (0, 400))
#korLoseLabel = Label(text = '지셨어요.', font_size = 32, pos = (0, 350), font_name = 'Malgun Gothic.ttf')
 
playAgainButton = Button(text = 'Play again?', size_hint = (0.2, 0.1), pos = (375, 0))
playAgainButton.bind(on_press = lambda x: reset('normal'))  

playAgainButtonHard = Button(text = 'Make it harder?', size_hint = (0.2, 0.1), pos = (700, 800))
playAgainButtonHard.bind(on_press = lambda x: reset('hard'))  

playAgainButtonLose = Button(text = 'Play again?', size_hint = (0.2, 0.1), pos = (375, 0))
playAgainButtonLose.bind(on_press = lambda x: reset('normal'))

screen.add_widget(winLabel)
#screen.add_widget(korWinLabel)
screen.add_widget(playAgainButton)
screen.add_widget(playAgainButtonHard)
loserScreen.add_widget(loseLabel)
#loserScreen.add_widget(korLoseLabel)
loserScreen.add_widget(playAgainButtonLose)
sm.add_widget(screen)
sm.add_widget(loserScreen)
for actor in main.children[0].children:
	if (actor.id == 'actor32'):
		actor.source = 'ICON_Player.png'
		
	if (actor.id == 'actor17'):
		actor.source = 'ICON_Igloo.png'
		
	if (actor.id == 'actor54'):
		actor.source = 'ICON_Gear.png'
		
	if (actor.id == 'actor80'):
		actor.source = 'ICON_Jewel.png'
	
	if (actor.id == 'actor74'):
		actor.source = 'ICON_Bear.png'
	

# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////
MyApp().run()