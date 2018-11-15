# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS	//
# ////////////////////////////////////////////////////////////////
from kivy.config import Config

Config.set('graphics', 'fullscreen', '0')
from kivy.app import App
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
from time import sleep
import socket
#import ip
#import hardwareip

commands = []
history = []


def queue(command):
    if (len(commands) >= 22): return

    commands.append(command)
    name = command.replace(' ', '')
    name.upper()

    if (len(commands) >= 12):
        mainImageQueue2.add_widget(Image(source='direction/' + name + '.jpg'))
        return

    mainImageQueue.add_widget(Image(source= 'direction/' + name + '.jpg'))


def execute():  # pause PLEASE
    global commands
    for command in commands:
        send(command)
        sleep(0.2)
    commands = []
    mainImageQueue.clear_widgets()
    mainImageQueue2.clear_widgets()

'''
def setDifficulty(difficulty)
   #
 
'''

'''
def send(command): #needs to be connected with the a server paul is writing
    #code must be added
'''


def pause():
    leftLay = FloatLayout(size_hint=(0.5, 0.5))
    leftPop = Popup(title='IN PROGRESS...',
                    size_hint=(0.240, 0.73),
                    auto_dismiss=False,
                    title_size=30,
                    title_align='center',
                    pos_hint={'x': 19.5 / Window.width,
                              'y': 157 / Window.height},
                    content=leftLay)

    leftImage = Image(source='cards/CARD_Left.jpg',
                      keep_ratio=True,
                      size_hint=(1.5, 1.945),
                      pos=(-78.95, 174.75))
    leftLay.add_widget(leftImage)

    leftPop.open()
    Clock.schedule_once(leftPop.dismiss, 5)


def clear():
    global commands
    if (len(commands) == 0): print('nothing to clear'); return
    mainImageQueue.remove_widget(mainImageQueue.children[0])
    del commands[len(commands) - 1]


# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER	            //
# //					 LOAD KIVY FILE		                    //
# ////////////////////////////////////////////////////////////////


screenManager = ScreenManager()

class MyApp(App):
    def build(self):
        return screenManager


Builder.load_file('main.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # (WHITE)


def quitAll():
    quit()


class MainScreen(Screen):

    def exitProgram(self):
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

   


    # ////////////////////////////////////////////////////////////////         # //														//
    # //						    POPUPS						                    //  		#   //															//



    def quitPopup(self):  # QUIT POPUP
        quitLay = FloatLayout(size_hint=(0.5, 0.5))
        quitPop = Popup(title='QUIT GAME',
                        size_hint=(0.3, 0.23),
                        auto_dismiss=True,
                        title_size=30,
                        title_align='center',
                        content=quitLay)
        yesButton = Button(text='YES',
                           size_hint=(0.46, 0.8),
                           font_size=20,
                           pos=(700, 425))
        noButton = Button(text='NO',
                          size_hint=(0.46, 0.8),
                          font_size=20,
                          pos=(965, 425))
        confirmationLabel = Label(text='Are you sure you want to quit?',
                                  pos=(685, 487.5),
                                  font_size=20)

        yesButton.bind(on_release=self.exitProgram)
        noButton.bind(on_release=quitPop.dismiss)

        quitLay.add_widget(yesButton)
        quitLay.add_widget(noButton)
        quitLay.add_widget(confirmationLabel)

        quitPop.open()

    def leftPopup(self):  # LEFT POPUP
        leftLay = FloatLayout(size_hint=(0.5, 0.5))
        leftPop = Popup(title='IN PROGRESS...',
                        size_hint=(0.240, 0.73),
                        auto_dismiss=False,
                        title_size=30,
                        title_align='center',
                        pos_hint={'x': 19.5 / Window.width,
                                  'y': 157 / Window.height},
                        content=leftLay)

        leftImage = Image(source='cards/CARD_Left.jpg',
                          keep_ratio=True,
                          size_hint=(1.5, 1.945),
                          pos=(-78.95, 174.75))
        leftLay.add_widget(leftImage)

        leftPop.open()
        Clock.schedule_once(leftPop.dismiss, .1)

    def upPopup(self):  # UP POPUP
        upLay = FloatLayout(size_hint=(0.5, 0.5))
        upPop = Popup(title='IN PROGRESS...',
                      size_hint=(0.240, 0.73),
                      auto_dismiss=False,
                      title_size=30,
                      title_align='center',
                      pos_hint={'x': 480 / Window.width,
                                'y': 157.5 / Window.height},
                      content=upLay)

        upImage = Image(source='cards/CARD_Up.jpg',
                        keep_ratio=True,
                        size_hint=(1.5, 1.945),
                        pos=(381.75, 174.75))
        upLay.add_widget(upImage)

        upPop.open()
        Clock.schedule_once(upPop.dismiss, .1)

    def downPopup(self):  # DOWN POPUP
        downLay = FloatLayout(size_hint=(0.5, 0.5))
        downPop = Popup(title='IN PROGRESS...',
                        size_hint=(0.240, 0.73),
                        auto_dismiss=False,
                        title_size=30,
                        title_align='center',
                        pos_hint={'x': 940.5 / Window.width,
                                  'y': 157.5 / Window.height},
                        content=downLay)

        downImage = Image(source='cards/CARD_Down.jpg',
                          keep_ratio=True,
                          size_hint=(1.5, 1.945),
                          pos=(842.5, 174.75))
        downLay.add_widget(downImage)

        downPop.open()
        Clock.schedule_once(downPop.dismiss, .1)

    def rightPopup(self):  # RIGHT POPUP
        rightLay = FloatLayout(size_hint=(0.5, 0.5))
        rightPop = Popup(title='IN PROGRESS...',
                         size_hint=(0.240, 0.73),
                         auto_dismiss=False,
                         title_size=30,
                         title_align='center',
                         pos_hint={'x': 1401.5 / Window.width,
                                   'y': 157 / Window.height},
                         content=rightLay)

        rightImage = Image(source='cards/CARD_Right.jpg',
                           keep_ratio=True,
                           size_hint=(1.5, 1.945),
                           pos=(1303.5, 174.75))
        rightLay.add_widget(rightImage)

        rightPop.open()
        Clock.schedule_once(rightPop.dismiss, .1)

    def victoryPopup(self):  # victory POPUP
        victoryLay = FloatLayout(size_hint=(0.5, 0.5))
        victoryPop = Popup(title='Win',
                         content=Label(text='You Win!'),
                         size_hint=(None, None),
                         size=(400, 400),
                         auto_dismiss=False,
                         title_size=30,
                         title_align='center',
                         pos_hint={'x': 1401.5 / Window.width,
                                   'y': 157 / Window.height},
                         content=victoryLay)
        victoryPop.open()


    def defeatPopup(self):  # defeat POPUP
        defeatLay = FloatLayout(size_hint=(0.5, 0.5))
        defeatPop = Popup(title='Lose',
                           content=Label(text='You Lose!'),
                           size_hint=(None, None),
                           size=(400, 400),
                           auto_dismiss=False,
                           title_size=30,
                           title_align='center',
                           pos_hint={'x': 1401.5 / Window.width,
                                     'y': 157 / Window.height},
                           content=defeatLay)
        defeatPop.open()


<<<<<<< Updated upstream
#creates the different screens


mainImageQueue = BoxLayout(padding=15, size_hint=(.825, None), height=150, pos_hint={'top': .9875})
mainImageQueue2 = BoxLayout(padding=15, size_hint=(.825, None), height=150, pos_hint={'top': .85})
newGameImageQueue = BoxLayout(padding=15, size_hint=(.825, None), height=150, pos_hint={'top': .9875})


#border = Image(source='images/rectangle.png', allow_stretch=True, keep_ratio=False,
            #   pos=(Window.width * 0, Window.height * 1.4), size_hint_y=None, height=Window.height * .3,
             #  size_hint_x=None, width=Window.width * 1.975)



class NewGame(Screen):

    def setDif(self):
        screenManager.current = 'main'
        #setDifficulty(difficulty)

main = MainScreen(name='main')

newGame = NewGame(name='newGame')

main.add_widget(mainImageQueue)

main.add_widget(mainImageQueue2)
newGame.add_widget(newGameImageQueue)


screenManager.add_widget(main)
screenManager.add_widget(newGame)

screenManager.current= 'newGame'

#main.add_widget(border)


# ////////////////////////////////////////////////////////////////
# //						  RUN APP							//
# ////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    MyApp().run()
