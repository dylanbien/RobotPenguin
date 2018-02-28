# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS						//
# ////////////////////////////////////////////////////////////////
import string
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


sm = ScreenManager()

class MyApp(App):
	def build(self):
		return sm

#Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)
		
def quitAll():
	quit()
	

# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////

class MyApp(App):
	def build(self):
		return sm

#Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)

# all args are passed in string form. locations are 'actor1', 'actor2', 'actor3', etc. types are 'ICON_Igloo.png', 'ICON_Wrench.png', etc.
class MainScreen(Screen):
	def exitProgram(self, obj):
		App.get_running_app().stop()
		Window.close()
	def resetBoard(self):
		for actor in self.children[0].children:
			actor.source = 'ICON_Wrench.png'
	def addImage(self, location, type): 
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = type
	def removeImage(self, location):
		for actor in self.children[0].children:
			if (actor.id == location):
				actor.source = 'ICON_Transparent.png'

class Actor(ButtonBehavior, Image):
	def on_press(self):
		main.removeImage('actor5')
		print('pressed')
		
	def moveRight(self):
		next = int(self.id.strip(string.ascii_letters)) + 1
		for id in main.ids:
			if (id == 'actor' + str(next) and root.ids[id].source == 'ICON_Transparent.png'):
				temp = self.source; self.source = root.ids[id].source, root.ids[id].source = temp
			
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

grid = GridLayout(id = 'grid', cols = 3, rows = 3, minimum_size = [300, 300], padding = 10, spacing = 1)
for i in range (9):
	b = Actor(id = 'actor' + str(i+1), source = 'ICON_Igloo.png', size_hint = [None, None])
	grid.add_widget(b)

main = MainScreen(name = 'main')
main.add_widget(grid)
sm.add_widget(main)
main.children[0].children[4].on_press = main.addImage('actor5', 'ICON_Gear.png')  

# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

MyApp().run()
