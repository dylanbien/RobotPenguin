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


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////


sm = ScreenManager()

bearIcon = Image(source = 'ICON_Bear.png',
                 keep_ratio = True,
                 size_hint = (1, 1))
gearIcon = Image(source = 'ICON_Gear.png')

board = GridLayout(cols = 2, row_force_default = True, row_default_height = 40)
board.add_widget(Button(text = 'mems', size_hint_x = None, width = 100))
board.add_widget(Button(text = 'hmm'))
board.add_widget(bearIcon)
board.add_widget(gearIcon)

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

sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
