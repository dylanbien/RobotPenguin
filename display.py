# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////


sm = ScreenManager()

class MyApp(App):
    def build(self):
        return sm

Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)
		
def quitAll():
    quit()
	

# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////

class MyApp(App):
    def build(self):
        return sm

Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)

class MyButton(Button)
def move(self, event):
	self.event = event
	if (self.event == 'btn1')
		#DO STUFF HERE!!!! probably don't need that if statement btw


class MainScreen(Screen):
    def exitProgram(self, obj):
        App.get_running_app().stop()
        Window.close()

# ////////////////////////////////////////////////////////////////
# //                                                            //
# //                          POPUPS                            //
# //                                                            //
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

sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
