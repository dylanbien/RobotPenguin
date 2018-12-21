# ////////////////////////////////////////////////////////////////
# //					 IMPORT STATEMENTS	                    //
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
from kivy.core.window import Window

import socket
from kivy.core.audio import SoundLoader

commands = []
counter = 0
Window.fullscreen = 'auto'

# ////////////////////////////////////////////////////////////////
# /	            DECLARE queue and clear functions	            //
# ////////////////////////////////////////////////////////////////

def queue(command):
    global commands
    if (len(commands) >= 22): return

    commands.append(command)
    name = command.replace(' ', '')
    name.upper()

    if (len(commands) >= 12):
        mainImageQueue2.add_widget(Image(source='direction/' + name + '.jpg'))
        return

    mainImageQueue.add_widget(Image(source= 'direction/' + name + '.jpg'))

def clear():
    global commands
    if (len(commands) == 0): print('nothing to clear'); return
    mainImageQueue.remove_widget(mainImageQueue.children[0])
    del commands[len(commands) - 1]

def clearAll():
    global commands
    commands = []  # clears commands
    mainImageQueue.clear_widgets()  # resets image queue 1
    mainImageQueue2.clear_widgets()  # resets image queue 2
# ////////////////////////////////////////////////////////////////
# /	                     Server Creation**WORK ON    	        //
# ////////////////////////////////////////////////////////////////
import enum
from dpea_p2p import Server

import threading

class PacketType(enum.Enum):
    NULL = 0
    difficulty = 1
    move = 2
    rotate = 3
    responseCommand = 4


#         |Bind IP       |Port |Packet enum
s = Server("172.17.21.1", 5001, PacketType)
s.open_server()
print('waiting for connection')
s.wait_for_connection()
print('connected')

def handle_response_packet(payload):
    
    print("recieved " + payload.decode("ascii"))

    global counter

    if payload.decode("ascii") == "win":
        counter = 0
        clearAll()
        main.victoryPopup()

    elif payload.decode("ascii") == "lose":
        counter = 0
        clearAll()
        main.defeatPopup()

    elif payload.decode("ascii") == "continue":

        counter += 1

        if counter > (len(commands) - 1):
            print('out of turns')
            counter = 0
            clearAll()
            main.defeatPopup()
            return
            

        temp = commands[counter]


        if temp == 'forward ':
            print('sending forward')
            s.send_packet(PacketType.move, b"forward")
            print('sending backward')
        elif temp == 'backward ':
            s.send_packet(PacketType.move, b"backward")
        elif temp == 'left ':
            print('sending left')
            s.send_packet(PacketType.rotate, b"left")
        elif temp == 'right ':
            print('sending right')
            s.send_packet(PacketType.rotate, b"right")

def check_server(): #impliment from execute

    handlers = {PacketType.responseCommand: handle_response_packet
                }
    packet_type, payload = s.recv_packet()

    if packet_type in handlers:
        handlers[packet_type](payload)
    else:
        print("got unhandled packet!")

   
            
       
def setDifficulty(difficulty):
    if difficulty == 'easy':
        print('sending easy')
        s.send_packet(PacketType.difficulty, b"easy")
    if difficulty == 'medium':
        print('sending medium')
        s.send_packet(PacketType.difficulty, b"medium")
    if difficulty == 'hard':
        print('sending hard')
        s.send_packet(PacketType.difficulty, b"hard")

def runner():

    while True:
        check_server()
# ////////////////////////////////////////////////////////////////
# /	                DECLARE execute functions	                //
# ////////////////////////////////////////////////////////////////

def execute():  # Work on with server
    global counter
    counter = 0

    temp = commands[counter] #begins the first command (after we transition to check server)
    
    if temp == 'forward ':
        print('sending forward: execute')
        s.send_packet(PacketType.move, b"forward")
    elif temp == 'backward ':
        print('sending backward: execute')
        s.send_packet(PacketType.move, b"backward")
    elif temp == 'left ':
        print('sending left: execute')
        s.send_packet(PacketType.rotate, b"left")
    elif temp == 'right ':
        print('sending right: execute')
        s.send_packet(PacketType.rotate, b"right")



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

# ////////////////////////////////////////////////////////////////
# //				       Main Screen      		 		    //
# ////////////////////////////////////////////////////////////////

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

    def setNewGameScreen(self):
        clearAll()
        screenManager.current = 'newGame'

    def setTitleScreen(self):
        clearAll()
        screenManager.current = 'title'

# ////////////////////////////////////////////////////////////////
# //				       Main screens POPUPS		 		    //
# ////////////////////////////////////////////////////////////////


    def victoryPopup(self):  # victory POPUP
        victoryLay = FloatLayout(size_hint=(0.5, 0.5))
        victoryPop = Popup(title='VICTORY',
                           size_hint=(0.3, 0.23),
                           auto_dismiss=False,
                           title_size=30,
                           title_align='center',
                           content=victoryLay)
        victoryImage = Image(source='winner/winner.png',
                             keep_ratio=True,
                             size_hint=(1.5*1.15, 1.945*1.15),
                             pos=(545, 545))
        playAgainButton = Button(text='Play Again',
                            size_hint=(0.46, 0.8),
                            font_size=20,
                            pos=(760, 425))
        quitButton = Button(text='Quit',
                            size_hint=(0.46, 0.8),
                            font_size=20,
                            pos=(1110, 425))

        playAgainButton.bind(on_release=victoryPop.dismiss)
        playAgainButton.bind(on_release=MainScreen.setNewGameScreen)

        quitButton.bind(on_release=victoryPop.dismiss)
        quitButton.bind(on_release=MainScreen.setTitleScreen)

        victoryLay.add_widget(quitButton)
        victoryLay.add_widget(playAgainButton)
        victoryLay.add_widget(victoryImage)
        victoryPop.open()


    def defeatPopup(self):  # defeat POPUP
        defeatLay = FloatLayout(size_hint=(0.5, 0.5))
        defeatPop = Popup(title='DEFEAT',
                          size_hint=(0.3, 0.23),
                          auto_dismiss=False,
                          title_size=30,
                          title_align='center',
                          content=defeatLay)
        defeatImage = Image(source='loser/loser.png',
                            keep_ratio=True,
                            size_hint=(1.5*1.3, 1.945*1.3),
                            pos=(480, 530))
        playAgainButton = Button(text='Play Again',
                            size_hint=(0.46, 0.8),
                            font_size=20,
                            pos=(760, 425))
        quitButton = Button(text='Quit',
                            size_hint=(0.46, 0.8),
                            font_size=20,
                            pos=(1110, 425))

        playAgainButton.bind(on_release=defeatPop.dismiss)
        playAgainButton.bind(on_release=MainScreen.setNewGameScreen)

        quitButton.bind(on_release=defeatPop.dismiss)
        quitButton.bind(on_release=MainScreen.setTitleScreen)

        defeatLay.add_widget(quitButton)
        defeatLay.add_widget(playAgainButton)
        defeatLay.add_widget(defeatImage)
        defeatPop.open()

    def instructionPopup(self):  # instruction POPUP
        #instructionLay = FloatLayout(size_hint=(0.5, 0.5))
        instruction = FloatLayout()
        instructionPop = Popup(title='Instructions',
                               size_hint=(0.375, 0.26840490797),
                               auto_dismiss=False,
                               title_size=30,
                               title_align='center',
                               content=instruction)
        quitButton = Button(text='Dismiss',
                            size_hint=(0.23, 0.4),
                            font_size=20,
                            pos=(985, 400))
        instructionLabel = Label(text='Turn and maneuver the penguin to get to the fish as quickly as possible.\n \nSelect the order you want the penguin to turn and move in, then press \'go\'.\n \nYou can\'t go through mountains, so you\'ll have to go around them.\n \nWatch out for the bear! If it gets to you before you reach the fish, you lose.\n \nGood luck!',
                                 pos=(690, 560),
                                 font_size=24.5)

        quitButton.bind(on_release=instructionPop.dismiss)
        instruction.add_widget(quitButton)
        instruction.add_widget(instructionLabel)
        instructionPop.open()

# ////////////////////////////////////////////////////////////////
# //	       	    	  New Game screen			            //
# ////////////////////////////////////////////////////////////////

class NewGame(Screen):

    def setMainScreen(self, difficulty):

        dif = difficulty
        
        screenManager.current = 'main'
        setDifficulty(dif)

    def instructionPopup(self):  # instruction POPUP
        #instructionLay = FloatLayout(size_hint=(0.5, 0.5))
        instruction = FloatLayout()
        instructionPop = Popup(title='Instructions',
                               size_hint=(0.375, 0.26840490797),
                               auto_dismiss=False,
                               title_size=30,
                               title_align='center',
                               content=instruction)
        quitButton = Button(text='Dismiss',
                            size_hint=(0.23, 0.4),
                            font_size=20,
                            pos=(985, 400))
        instructionLabel = Label(text='Turn and maneuver the penguin to get to the fish as quickly as possible\n \nSelect the order you want the penguin to turn and move in, then press \'go\'.\n \nyou can\'t go through mountains, so you\'ll have to go around them\n \nwatch out for the bear! If it gets to you before you reach the fish, you lose\n \nGood luck!',
                                 pos=(690, 560),
                                 font_size=24.5)

        quitButton.bind(on_release=instructionPop.dismiss)
        instruction.add_widget(quitButton)
        instruction.add_widget(instructionLabel)
        instructionPop.open()


# ////////////////////////////////////////////////////////////////
# //	       	    	  Title screen			                //
# ////////////////////////////////////////////////////////////////


class TitleScreen(Screen):

    def setInstructionScreen(self):
        screenManager.current = 'instruction'

# ////////////////////////////////////////////////////////////////
# //		    	  Instruction screen   			            //
# ////////////////////////////////////////////////////////////////

class InstructionScreen(Screen):

    def setNewScreen(self):
        screenManager.current = 'newGame'

# ////////////////////////////////////////////////////////////////
# //		    	  Creates and adds screens			        //
# ////////////////////////////////////////////////////////////////

mainImageQueue = BoxLayout(padding=15, size_hint=(.825, None), height=150, pos_hint={'top': .9875})
mainImageQueue2 = BoxLayout(padding=15, size_hint=(.825, None), height=150, pos_hint={'top': .85})

title = TitleScreen(name='title')
instruction = InstructionScreen(name='instruction')
newGame = NewGame(name='newGame')
main = MainScreen(name='main')


main.add_widget(mainImageQueue)
main.add_widget(mainImageQueue2)

screenManager.add_widget(title)
screenManager.add_widget(instruction)
screenManager.add_widget(newGame)
screenManager.add_widget(main)

screenManager.current= 'title'

# ////////////////////////////////////////////////////////////////
# //				  RUN APP							        //
# ////////////////////////////////////////////////////////////////

if __name__ == "__main__":
    background = threading.Thread(target=runner)
    background.start()
    try:
        MyApp().run()
    except KeyboardInterrupt:
        print('here')
        s.close_connection()
        s.close_server()
