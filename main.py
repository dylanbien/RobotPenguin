# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////


from kivy.app import App
from kivy.uix import togglebutton
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import *


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


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////


blueIsOn = False
redIsOn = False
unpaused = True
blueDirection = 0
blueSpeed = 0
redDirection = 0
redSpeed = 0
whiteDirection = 0
whiteSpeed = 500


# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////


def update(color):
# TURNS ON/OFF BY COLOR CONDITIONALLY
    # BLUE
    if color == 'B' or 'ALL':
        if blueIsOn and unpaused and blueSpeed != 0:
            blue.run(blueDirection, blueSpeed)
        else:
            blue.free()
    # RED
    if color == 'R' or 'ALL':
        if redIsOn and unpaused and redSpeed != 0:
            red.run(redDirection, redSpeed)
        else:
            red.free()
    # WHITE
    if color == 'W' or 'ALL':
        if whiteIsOn and unpaused:
            white.run(whiteDirection, whiteSpeed)
        else:
            white.free()

def stopAll():
# FREES ALL STEPPERS WITHOUT CHANGING SPEED/DIRECTION VALUES
    # BLUE
    blue.free()
    # RED
    red.free()
    # WHITE
    white.free()

def setSpeed(color, val):
# SETS 'color' STEPPER SPEED TO 'val'
    # BLUE
    if color == 'B':
        global blueSpeed
        blueSpeed = val
    # RED
    if color == 'R':
        global redSpeed
        redSpeed = val
    # WHITE speed is hardcoded

def setDirection(color):
# SETS 'color' STEPPER DIRECTION
    # BLUE
    if color == 'B':
        global blueDirection
        if blueDirection == 0:
            blueDirection = 1
        else: #blueDirection == 1
            blueDirection = 0
    # RED
    if color == 'R':
        global redDirection
        if redDirection == 0:
            redDirection = 1
        else: #redDirection == 1
            redDirection = 0
    # WHITE
    if color == 'W':
        global whiteDirection
        if whiteDirection == 0:
            whiteDirection = 1
        else: #whiteDirection == 1
            whiteDirection = 0

def quitAll():
    stopAll()
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


# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////


class MainScreen(Screen):

# //                  BUTTON/SLIDER ACTIONS                     //
    def exitProgram(self, instance):
        quitAll()

    def sliderAction(self, color, val):
    # FOR BLUE AND RED SLIDERS
        setSpeed(color, val)
        update(color)

    def directionButtonAction(self, color):
    # FOR BLUE AND RED DIRECTION BUTTONS
        setDirection(color)
        update(color)

    def offOnButtonAction(self, color):
    # FOR BLUE AND RED OFF/ON BUTTONS
        update(color)

    def pauseUnpauseButtonAction(self):
    # FOR PAUSE/UNPAUSE BUTTON
        if unpaused:
            update('ALL')
        else:
            stopAll()

# //                     TOGGLE TEXT                            //
    def blueToggleText(self, state):
        global blueIsOn
        if state == 'down':
            blueIsOn = True
            return 'ON'
        else: #state == 'normal'
            blueIsOn = False
            return 'OFF'

    def redToggleText(self, state):
        global redIsOn
        if state == 'down':
            redIsOn = True
            return 'ON'
        else: #state == 'normal'
            redIsOn = False
            return 'OFF'

    def whiteToggleText(self, state):
        global whiteIsOn
        if state == 'down':
            whiteIsOn = True
            return 'ON'
        else: #state == 'normal'
            whiteIsOn = False
            return 'OFF'

    def pauseToggleText(self, state):
        global unpaused
        if state == 'down':
            unpaused = False
            return 'UNPAUSE'
        else: #state == 'normal'
            unpaused = True
            return 'PAUSE'

# POPUP /////////////////////////////////////////////////
    def callPopup (self):
        layout = FloatLayout(size_hint = (0.5, 0.5))
        popup = Popup(title = 'QUIT SPIROGRAPH',
            size_hint = (0.3, 0.23),
            auto_dismiss = True,
            title_size = 30,
            title_align = 'center',
            content = layout)
        yesButton = Button(text = 'YES',
            size_hint = (0.46, 0.8),
            font_size = 20,
            pos = (700, 445))

        noButton = Button(text = 'NO',
            size_hint = (0.46, 0.8),
            font_size = 20,
            pos = (965, 445))
        confirmationLabel = Label(text = 'Are you sure you want to quit?',
            pos = (685, 515),
            font_size = 20)

        yesButton.bind(on_press = self.quitAction)
        noButton.bind(on_press = popup.dismiss)

        layout.add_widget(yesButton)
        layout.add_widget(noButton)
        layout.add_widget(confirmationLabel)

        popup.open()

sm.add_widget(MainScreen(name = 'main'))


# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
