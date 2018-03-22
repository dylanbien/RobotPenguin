# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////

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
commands = []
history = []
def queue(command):
	commands.append(command)
	name = command.replace(' ','')
	name.upper()
	imageQueue.add_widget(Image(source = name + '.png'))
	

def execute(): # pause PLEASE 제발
	global commands
	for command in commands:
		send(command)
		sleep(0.2)
	commands = []
	imageQueue.clear_widgets()

def send(command, retry = 2):
	history.append(command)
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = ('172.17.17.116', 10009)
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
		
def pause():
	leftLay = FloatLayout(size_hint = (0.5, 0.5))
	leftPop = Popup(title = 'IN PROGRESS...',
		size_hint = (0.240, 0.73),
		auto_dismiss = False,
		title_size = 30,
		title_align = 'center',
		pos_hint = { 'x' : 19.5 / Window.width,
					 'y' : 157 / Window.height},
		content = leftLay)

	leftImage = Image(source = 'CARD_Left.png',
					  keep_ratio = True,
					  size_hint = (1.5, 1.945),
					  pos = (-78.95, 174.75))
	leftLay.add_widget(leftImage)

	leftPop.open()
	Clock.schedule_once(leftPop.dismiss, 5)

	
# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////


sm = ScreenManager()

class MyApp(App):
	def build(self):
		return sm

Builder.load_file('main.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)

def quitAll():
	quit()

	
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

# ////////////////////////////////////////////////////////////////
# //															//
# //						  POPUPS							//
# //															//
# ////////////////////////////////////////////////////////////////

	def quitPopup (self): # QUIT POPUP
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
		
	def leftPopup (self): # LEFT POPUP
		leftLay = FloatLayout(size_hint = (0.5, 0.5))
		leftPop = Popup(title = 'IN PROGRESS...',
			size_hint = (0.240, 0.73),
			auto_dismiss = False,
			title_size = 30,
			title_align = 'center',
			pos_hint = { 'x' : 19.5 / Window.width,
						 'y' : 157 / Window.height},
			content = leftLay)

		leftImage = Image(source = 'CARD_Left.png',
						  keep_ratio = True,
						  size_hint = (1.5, 1.945),
						  pos = (-78.95, 174.75))
		leftLay.add_widget(leftImage)

		leftPop.open()
		Clock.schedule_once(leftPop.dismiss, .1)
		

	def upPopup (self): # UP POPUP
		upLay = FloatLayout(size_hint = (0.5, 0.5))
		upPop = Popup(title = 'IN PROGRESS...',
			size_hint = (0.240, 0.73),
			auto_dismiss = False,
			title_size = 30,
			title_align = 'center',
			pos_hint = { 'x' : 480 / Window.width,
						 'y' : 157.5 / Window.height},
			content = upLay)

		upImage = Image(source = 'CARD_Up.png',
						  keep_ratio = True,
						  size_hint = (1.5, 1.945),
						  pos = (381.75, 174.75))
		upLay.add_widget(upImage)

		upPop.open()
		Clock.schedule_once(upPop.dismiss, .1)

	def downPopup (self): # DOWN POPUP
		downLay = FloatLayout(size_hint = (0.5, 0.5))
		downPop = Popup(title = 'IN PROGRESS...',
			size_hint = (0.240, 0.73),
			auto_dismiss = False,
			title_size = 30,
			title_align = 'center',
			pos_hint = { 'x' : 940.5 / Window.width,
						 'y' : 157.5 / Window.height},
			content = downLay)

		downImage = Image(source = 'CARD_Down.png',
						  keep_ratio = True,
						  size_hint = (1.5, 1.945),
						  pos = (842.5, 174.75))
		downLay.add_widget(downImage)

		downPop.open()
		Clock.schedule_once(downPop.dismiss, .1)

	def rightPopup (self): # RIGHT POPUP
		rightLay = FloatLayout(size_hint = (0.5, 0.5))
		rightPop = Popup(title = 'IN PROGRESS...',
			size_hint = (0.240, 0.73),
			auto_dismiss = False,
			title_size = 30,
			title_align = 'center',
			pos_hint = { 'x' : 1401.5 / Window.width,
						 'y' : 157 / Window.height},
			content = rightLay)

		rightImage = Image(source = 'CARD_Right.png',
						  keep_ratio = True,
						  size_hint = (1.5, 1.945),
						  pos = (1303.5, 174.75))
		rightLay.add_widget(rightImage)

		rightPop.open()
		Clock.schedule_once(rightPop.dismiss, .1)
		
main = MainScreen(name = 'main')
imageQueue = BoxLayout(padding = 15, size_hint=(.925, None), height=150, pos_hint={'top': 1})


#for i in range(10):
	#queue.add_widget(Image(source='LEFT.png'))

main.add_widget(imageQueue)
sm.add_widget(main)



# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

MyApp().run()