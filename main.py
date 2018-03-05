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
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
import socket
import sys


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////


sm = ScreenManager()

class MyApp(App):
    def build(self):
        return sm

Builder.load_file('main.kv')
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

Builder.load_file('main.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1) # (WHITE)

class MainScreen(Screen):

    def exitProgram(self, obj):
        App.get_running_app().stop()
        Window.close()

# ////////////////////////////////////////////////////////////////
# //                                                            //
# //                          POPUPS                            //
# //                                                            //
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
        Clock.schedule_once(leftPop.dismiss, 1.5)
        

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
        Clock.schedule_once(upPop.dismiss, 1.5)

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
        Clock.schedule_once(downPop.dismiss, 1.5)

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
        Clock.schedule_once(rightPop.dismiss, 1.5)

sm.add_widget(MainScreen(name = 'main'))
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('172.17.17.116', 10009)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
	# Send data
	message = b'foo.function()'
	print('sending {!r}'.format(message))
	sock.sendall(message)
	amount_received = 0
	amount_expected = len(message)

	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print('received {!r}'.format(data))

finally:
	print('closing socket')
	sock.close()

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

#MyApp().run()
