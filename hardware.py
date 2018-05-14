# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
import DeltaArm
from kivy.config import Config
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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from time import sleep
import socket
import sys
import ip

da = DeltaArm.DeltaArm(0,1,2)

def obey(self, retry = 5):
	data = ''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ip.server_address
	print('connecting to {} port {}'.format(*server_address))
	sock.connect(server_address)
	print('i am hardware.py')
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

def send(command, retry = 2):
	history.append(command)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = ip.server_address
	print('main connecting to {} port {}'.format(*server_address))
	
	try:
		# Send data
		sock.connect(server_address)
		message = command.encode()
		print('sending {!r}'.format(message))
		sock.sendall(message)
		
	except OSError:
		# Retry if retried less than two times
		if(retry >= 0):
			send(command, retry - 1)
		
	finally:
		print('please clap')
		sock.close()
		

# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////

class MainScreen(Screen):

	def exitProgram(self, obj):
		App.get_running_app().stop()
		Window.close()
	def playerAction(self, command):
		send(command)
	def queueAction(self, command):
		queue(command)
	def executeAction(self):
		execute()
	def pauseAction(self):
		pause()
	def clearAction(self):
		clear()

sm = ScreenManager()

class MyApp(App):
	def build(self):
		return sm

def quitAll():
	quit()
		
main = MainScreen(name = 'main')
sm.add_widget(main)



# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

MyApp().run()
