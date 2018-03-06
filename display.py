# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
import string
import random
import socket
import sys
from kivy.app import App
from kivy.uix import togglebutton
from kivy.uix.widget import Widget
from kivy.uix.image import Image
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
from kivy.uix.behaviors import ButtonBehavior

# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////

player_location = 1
sm = ScreenManager()

class MyApp(App):
	def build(self):
		return sm

#Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)
		
def quitAll():
	quit()
	

# ////////////////////////////////////////////////////////////////////////////
# //	DECLARE APP, MAINSCREEN, ACTOR CLASSES/METHODS AND SCREENMANAGER	//				
# //					 		LOAD KIVY FILE								//			
# ////////////////////////////////////////////////////////////////////////////
		
# all args are passed in string form. locations are 'actor1', 'actor2', 'actor3', etc. types are 'ICON_Igloo.png', 'ICON_Wrench.png', etc.
class MainScreen(Screen):
	def exitProgram(self, obj):
		App.get_running_app().stop()
		Window.close()
	def resetBoard(self):
		for actor in self.children[0].children:
			actor.source = 'ICON_Gray.png'
	def addActor(self, location, type): 
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = type
	def removeActor(self, location):
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = 'ICON_Gray.png'
	def test(self, dt):
		for actor in self.children[0].children:
			if (actor.source != 'ICON_Gray.png'):
				actor.random()
	def playerForward(self):
		print('you have moved the player forwards or something')
		for actor in self.children[0].children:
			if ('Player' in actor.source):
				actor.moveForward()
	
	def playerBackward(self):
		print('you have moved the player backwards or something')
		for actor in self.children[0].children:
			if ('Player' in actor.source):
				actor.moveBackward()
				
				
class Actor(ButtonBehavior, Image):
	def on_press(self):
		print('pressed')
		
	def test(self, dt):
		if ('Player' not in self.source): return
		self.rotate(self.id, 90*random.randint(0, 3))
		self.moveForward()
		
	def moveForward(self):
		if ('90' in self.source): self.moveRight()
		elif ('180' in self.source): self.moveDown()
		elif ('270' in self.source): self.moveLeft()
		else: self.moveUp()
	
	def moveBackward(self):
		if ('90' in self.source): self.moveLeft()
		elif ('180' in self.source): self.moveUp()
		elif ('270' in self.source): self.moveRight()
		else: self.moveDown()
			
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
	
	def rotate(self, location, degrees):
		for actor in main.children[0].children:
			if (actor.id == location and 'Player' in actor.source):
				if (degrees == 0 or degrees % 90 != 0): actor.source = 'ICON_Player.png'
				elif (degrees >= 360): actor.source = 'ICON_Player_' + str(degrees%360) + '.png'
				else: actor.source = 'ICON_Player_' + str(degrees) + '.png'
		
	def moveRight(self): #strafe
		next = int(self.id.strip(string.ascii_letters)) + 1
		if (next % main.children[0].cols == 1):
			return #should turn/rotate right eventually or something or other
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Gray.png'):
				temp = self.source; self.source = actor.source; actor.source = temp
	
	def moveLeft(self): #strafe
		next = int(self.id.strip(string.ascii_letters)) - 1
		if (next % main.children[0].cols == 0):
			return #should turn/rotate left eventually or something or other
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Gray.png'):
				temp = self.source; self.source = actor.source; actor.source = temp
	
	def moveUp(self):
		next = int(self.id.strip(string.ascii_letters)) - main.children[0].rows
		if (next < 0):
			return #should up/down methods rotate?
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Gray.png'):
				temp = self.source; self.source = actor.source; actor.source = temp
	
	def moveDown(self):
		next = int(self.id.strip(string.ascii_letters)) + main.children[0].rows
		if (next > main.children[0].rows*main.children[0].cols):
			return
		for actor in main.children[0].children:
			if (actor.id == 'actor' + str(next) and actor.source == 'ICON_Gray.png'):
				temp = self.source; self.source = actor.source; actor.source = temp
			
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
		
# ////////////////////////////////////////////////////////////////
# //					 CREATE GRID/ACTORS 					//
# ////////////////////////////////////////////////////////////////
grid = GridLayout(id = 'grid', cols = 9, rows = 9, minimum_size = [300, 300], padding = 10, spacing = 1)
for i in range (0, grid.cols*grid.rows):
	b = Actor(id = 'actor' + str(i+1), source = 'ICON_Gray.png', size_hint = [None, None])
	grid.add_widget(b)

main = MainScreen(name = 'main')
main.add_widget(grid)
sm.add_widget(main)
for actor in main.children[0].children:
	if (actor.id == 'actor32'):
		actor.source = 'ICON_Player.png'
		
	if (actor.id == 'actor17'):
		actor.source = 'ICON_Wrench.png'
		
# ////////////////////////////////////////////////////////////////
# //						 SOCKET				 				//
# ////////////////////////////////////////////////////////////////

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.17.17.116', 10009)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
	# Wait for a connection
	print('waiting for a connection')
	connection, client_address = sock.accept()
	try:
		print('connection from', client_address)
		data = connection.recv(16)
		getattr(main, data)() #playerForward, playerBackward
		print ('received this: ' + data)
		connection.sendall(data)

	finally:
		# Clean up the connection
		connection.close()
		
# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

#MyApp().run()
