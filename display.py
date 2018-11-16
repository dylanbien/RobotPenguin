from kivy.config import Config

Config.set('graphics', 'resizable', False)
import string
import random
import socket
import sys
import math
import DeltaArm
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from time import sleep
from kivy.uix.behaviors import ButtonBehavior


# ////////////////////////////////////////////////////////////////
# //			DECLARE APP CLASS AND SCREENMANAGER				//
# //					 LOAD KIVY FILE							//
# ////////////////////////////////////////////////////////////////
difficulty = 'easy'
canWin = False
turn = 0
justGeared = False
gears = []
highScore = 2
score = 0
sm = ScreenManager()
#Window.size = (1920, 1080)
Window.fullscreen = True




da = DeltaArm.DeltaArm(0, 1, 2) #creates arm
da.home_all() #homes it
current = (0, 0, 0)
direction = 0

class MyApp(App):
    def build(self):
       #Clock.schedule_interval(obey, .1)
        return sm

def quitAll():
    quit()


def reset(dif):
    global turn
    global difficulty
    global canWin
    global score
    global justGeared
    canWin = False
    justGeared = False
    print('difficulty was ' + difficulty)
    difficulty = dif
    print('now is ' + difficulty)
    turn = 0
    testIndex = 0
    score = 0
    grid.clear_widgets()
    possible = []
    test = random.sample(range(1, 82), 81)
    locPenguin = 1 #sets starting location of the penguin
    locGoal = [85,88,91]
    
  # banned = [locs[0] + 1, locs[0] - 1, locs[0] + 9, locs[0] - 9, locs[0] - 10, locs[0] - 8, locs[0] + 10,     locs[0] + 8,
          #    locs[0]] #8 spots around the penguin needs to be fixe


    edges = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 19, 28, 37, 46, 55, 64, 73, 74, 75, 76, 77, 78, 79, 80, 81, 18, 27, 36, 45,
             54, 63, 72]  # will sometimes contain locations of other things

    #sets possible locations of the obstacles
    allObstacles = [
    [3,4, 5, 6],
    [27, 28,30 ,31],
    [66, 79],
    [43, 44, 57],
    [81,82, 83, 84],
    [33, 34, 46, 47],
    [10, 23, 36],
    [61,62,74,75],
    [86,87],
    [25, 38, 51],
    [52, 65, 78 ],

    ]

    assignedObstacleLocations = []

    for i in range(0, grid.cols * grid.rows): #resets all 81 grids to transparent
        b = Actor(id='actor' + str(i + 1), source='icons/ICON_Transparent.png', size_hint=[1, 1])
        grid.add_widget(b)

    for x in allObstacles:
        y = random.randint(0, len(x)) #get random in in each array
        assignedObstacleLocations.append(y)
        #print(obstacles)

    assignedGoal = 0

    if (dif = 'easy')
        assignedGoal = locGoal[0]
    elif (dif = 'medium')
        assignedGoal = locGoal[1]
    elif (dif = 'hard')
        assignedGoal = locGoal[2]


    for actor in main.children[0].children:
        if (actor.id == 'actor' + str(locPenguin)): #places penguin
            print('player is ' + str(locPenguin))
            actor.source = 'players/ICON_Player.jpg'

        if (actor.id == 'actor' + assignedGoal):  # assigns goal id to actor + obstacle
            print('goal is ' + str((locGoal)))
            actor.source = 'icons/ICON_Goal.jpg'

        for i in assignedObstacleLocations:

            if (actor.id == 'actor' + str(i)):  # assigns jewels id to actor + obstacle
                print('jewel/wrench is ' + str(i))
                actor.source = 'icons/ICON_Igloo.jpg'


'''
    while testIndex < 81: #goes through values 0-81
        for actor in main.children[0].children:
            print('test index first ' + str(testIndex) + ' number is ' + str(test[testIndex]))
            if ('Transparent' in actor.source and test[testIndex] not in banned and str(
                test[testIndex]) in actor.id): possible.append(test[testIndex]); break
        testIndex += 1
    print(possible)
'''

    if ('hard' in difficulty):  #places the players if difficulty is 'hard'
        for actor in main.children[0].children:
            if (actor.id == 'actor' + str(obstacles[3])):
                print('igloo is ' + str(obstacles[3]))
                actor.source = 'icons/ICON_Igloo.jpg'

            if (actor.id == 'actor' + str(obstacles[4])):
                print('igloo is ' + str(obstacles[4]))
                actor.source = 'icons/ICON_Igloo.jpg'

        if len(possible) > 0:
            pos = random.sample(range(0, len(possible)), 2)  # pos = random.randint(0, len(possible) - 1)
        else:
            pos = 0
        print('pos is ' + str(pos) + ', will be set here ' + str(possible[pos[0]]) + ' and' + str(possible[pos[1]]))

        for actor in main.children[0].children:
            if (actor.id == 'actor' + str(possible[pos[0]])): actor.source = 'ICON_Bear.jpg'; print('have set'); break
        for actor in main.children[0].children:
            if (actor.id == 'actor' + str(possible[pos[1]])): actor.source = 'ICON_Bear_2.jpg'; print('have set'); break
    else:
        if len(possible) > 0:
            pos = random.randint(0, len(possible) - 1)
        else:
            pos = 0
        print('pos is ' + str(pos) + ', will be set here ' + str(possible[pos]))

        for actor in main.children[0].children:
            if (actor.id == 'actor' + str(possible[pos])): actor.source = 'ICON_Bear.jpg'; print('have set'); break

    sm.current = 'main'

#Combined hardware.py functions
def obey_paul(data):
    
    #if (date =='easy'):
        self.reset('easy')
    #elif(date == 'medium'):
        self.reset('medium')
    #elif (date == 'hard'):
        self.reset('hard')
    
    if (data == 'forward '): #recieves forward
        if (direction % 360 == 0): #direction comes from how its facing (starts at 0)
            current[1] += 1
            da.move_to_point(current)
        elif (direction % 360 == 90):
            current[0] += 1
            da.move_to_point(current)
        elif (direction % 360 == 180):
            current[1] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 270):
            current[0] -= 1
            da.move_to_point(current)
            
            
        main.playerForward()

    elif (data == 'backward '): #recieves backwards
        if (direction % 360 == 0):
            current[1] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 90):
            current[0] -= 1
            da.move_to_point(current)
        elif (direction % 360 == 180):
            current[1] += 1
            da.move_to_point(current)
        elif (direction % 360 == 270):
            current[0] += 1
            da.move_to_point(current)

        main.playerBackward()

    elif (data == 'left '): #receives left
        direction += 270

        main.playerRotate('left')

    elif (data == 'right '): #revieves right

        direction += 90

        main.playerRotate('right')

    else:
        print('fail')
        return
#// DECLARE APP, MAINSCREEN, ACTOR CLASSES/METHODS AND SCREENMANAGER	//
# # ////////////////////////////////////////////////////////////////////////////
# # //	D						LOAD KIVY FILE								//
# ////////////////////////////////////////////////////////////////////////////

#These handle the visual component of all of the things that happen in the obey() function

# all args are passed in string form. locations are 'actor1', 'actor2', 'actor3', etc. types are 'ICON_Igloo.jpg', 'ICON_Wrench.jpg', etc.]

class MainScreen(Screen):
    def exitProgram(self):
        App.get_running_app().stop()
        Window.close()

    #Replaces every image with a blank image
    def resetBoard(self):
        for actor in self.children[0].children:
            actor.source = 'icons/ICON_Transparent.png'

    def addActor(self, location, type):
        for actor in self.children[0].children:
            if (actor.id == location):
                actor.source = type

    def removeActor(self, location):
        for actor in self.children[0].children:
            if (actor.id == location):
                actor.source = 'icons/ICON_Transparent.png'

    def test(self):
        for actor in self.children[0].children:
            if (actor.source != 'icons/ICON_Transparent.png'):
                actor.random()
    

   #the below move the actor
   #they get called in the obey function
   #tehy call functions in the actor class

 

    def playerForward(self):
        print('you have moved the player forwards or something')
        for actor in main.children[0].children:
            if ('Player' in actor.source):
                actor.moveForward()
                return

    def playerBackward(self):
        print('you have moved the player backwards or something')
        for actor in self.children[0].children:
            if ('Player' in actor.source):
                actor.moveBackward()
                return

    def playerRotate(self, direction):
        print('you have rotated the player ' + direction)
        for actor in self.children[0].children:
            if ('Player' in actor.source):
                actor.rotateDirection(direction)
                return
   #done with calls to actor



    def huntPlayer(self):
        global difficulty
        global turn
        print('turn is ' + str(turn) + ', so moving twice will be ' + str(turn % 2 == 0))
        if (difficulty == 'hard'):
            print('difficulty is hard')
            for hunter in self.children[0].children:
                if ('Bear' in hunter.source):
                    hunter.goTowards();
                    break
        else:
            for hunter in self.children[0].children:
                if ('Bear' in hunter.source):
                    hunter.goTowards();
                    break


class Actor(ButtonBehavior, Image): #creates an actor class

    def on_press(self): #when button is pressed
        print('pressed')

    def test(self):
        if ('Player' not in self.source): return
        self.rotate(self.id, 90 * random.randint(0, 3))
        self.moveForward()


  
    #below are called above in the main class

    
    def moveForward(self):
        if ('90' in self.source):
            self.moveRight(); main.huntPlayer(); return
        elif ('180' in self.source):
            self.moveDown(); main.huntPlayer(); return
        elif ('270' in self.source):
            self.moveLeft(); main.huntPlayer(); return
        else:
            self.moveUp(); main.huntPlayer(); return

    def moveBackward(self):
        if ('90' in self.source):
            self.moveLeft(); main.huntPlayer(); return
        elif ('180' in self.source):
            self.moveUp(); main.huntPlayer(); return
        elif ('270' in self.source):
            self.moveRight(); main.huntPlayer(); return
        else:
            self.moveDown(); main.huntPlayer(); return



    def loser(self, *args):
        app = App.get_running_app()
        app.root.current = "Loser"

    def random(self):
        if ('Player' not in self.source):
            return
        index = random.randint(1, 4)
        if index == 1:
            self.moveRight()
        elif index == 2:
            self.moveLeft()
        elif index == 3:
            self.moveUp()
        else:
            self.moveDown()
    '''
    def spawnGear(self):
        global gears
        unset = True
        while unset:
            x = random.randint(1, 81)
            for actor in main.children[0].children:
                if (str(81) in actor.id and 'Transparent' in actor.source and 81 not in gears):
                    actor.source = 'icons/ICON_Gear.jpg';
                    print('gear was set at actor ' + actor.id);
                    gears.append(81);
                    unset = False;
                    return

    def clearGear(self):
        for actor in main.children[0].children:
            if ('Gear' in actor.source): actor.source = 'icons/ICON_Transparent.png'
    '''
    def unflash(self, arg):
        if ('two' in arg):
            self.source = 'icons/ICON_Bear_2.jpg'
        else:
            self.source = 'icons/ICON_Bear.jpg'

    def rotateDegrees(self, location, degrees):
        if (sm.current != 'main'): return
        for actor in main.children[0].children:
            if (actor.id == location and 'Player' in actor.source):
                if (degrees == 0 or degrees == 360 or degrees % 90 != 0):
                    actor.source = 'icons/ICON_Player.jpg'
                elif (degrees > 360):
                    actor.source = 'icons/ICON_Player_' + str(degrees % 360) + '.jpg'
                else:
                    actor.source = 'icons/ICON_Player_' + str(degrees) + '.jpg'

    def rotateDirection(self, direction):
        if (sm.current != 'main'): return
        if (direction == 'left' and self.source == 'icons/ICON_Player.jpg'):
            self.source = 'icons/ICON_Player_270.jpg'
            return
        elif (direction == 'right' and self.source == 'icons/ICON_Player.jpg'):
            self.source = 'icons/ICON_Player_90.jpg'
            return
        else:
            degree = int(self.source.strip(string.ascii_letters + string.punctuation))
            if (direction == 'left'):
                self.source = 'icons/ICON_Player_' + str(((degree + 270) % 360)) + '.jpg'
            else:
                self.source = 'icons/ICON_Player_' + str(((degree + 90) % 360)) + '.jpg'
            if (self.source == 'icons/ICON_Player_0.jpg'): self.source = 'icons/ICON_Player.jpg'


    #gets called in all the directional moves
    def move(self, next):
        global canWin
        global score
        global highScore
        global justGoaled
        for actor in main.children[0].children:
            if (actor.id == 'actor' + str(next) and actor.source == 'icons/ICON_Transparent.png'):
                temp = self.source;
                self.source = actor.source;
                actor.source = temp;
                justGoaled = False;
                return
            elif (actor.id == 'actor' + str(
                    next) and 'Player' in actor.source and 'Bear' in self.source and sm.current != 'Winner'):
                actor.source = self.source;
                self.source = 'icons/ICON_Transparent.png'
                if (justGoaled): self.clearGoal()
                justGoaled = False
                print('you are a failure')
                Clock.schedule_once(self.loser, 1)
            # sm.current = 'Loser'
            elif (actor.id == 'actor' + str(
                    next) and 'Bear' in actor.source and 'Player' in self.source and sm.current != 'Winner'):
                if (justGoaled): self.clearGoal()
                justGoaled = False
                self.source = actor.source;
                actor.source = 'icons/ICON_Transparent.png'
                print('you are a failure')
                Clock.schedule_once(self.loser, 1)
            # sm.current = 'Loser'
            elif (actor.id == 'actor' + str(next) and 'Goal' in actor.source and 'Player' in self.source):
                actor.source = self.source;
                self.source = 'icons/ICON_Transparent.png'
                justGoaled = True
                canWin = True
                score += 1
                scoreLabel.text = 'Your score was ' + str(score) + '. High score: ' + str(highScore)
                self.spawnGoal();
                return
            elif (actor.id == 'actor' + str(next) and 'Jewel' in actor.source and 'Player' in self.source and canWin):
                justGoaled = False
                actor.source = self.source;
                self.source = 'icons/ICON_Transparent.png'
                if score > highScore: highScore = score; scoreLabel.text = 'Your score was ' + str(
                    score) + '. High score: ' + str(highScore)
                sm.current = 'Winner'



    
    #get called in move forward and move backwards

    
    def moveRight(self):  # strafe
        if (sm.current != 'main'): return
        next = int(self.id.strip(string.ascii_letters)) + 1
        if (next % main.children[0].cols == 1):
            return
        else:
            self.move(next)

    def moveLeft(self):  # strafe
        if (sm.current != 'main'): return
        next = int(self.id.strip(string.ascii_letters)) - 1
        if (next % main.children[0].cols == 0):
            return
        else:
            self.move(next)

    def moveUp(self):
        if (sm.current != 'main'): return
        next = int(self.id.strip(string.ascii_letters)) - main.children[0].rows
        print(next)
        if (next < 0):
            return
        else:
            self.move(next)

    def moveDown(self):
        if (sm.current != 'main'): return
        next = int(self.id.strip(string.ascii_letters)) + main.children[0].rows
        if (next > main.children[0].rows * main.children[0].cols):
            return
        else:
            self.move(next)


#needs to be fixed for harder levels
    def goTowards(self):  # if anyone wants to fix please feel free
        if (sm.current != 'main'): return
        global turn
        prey = 0
        position = 0
        bears = []
        obstacles = []
        reverse = ''
        canX = True
        canY = True
        for actor in main.children[0].children:
            if ('Player' in actor.source): prey = 81 - main.children[0].children.index(actor)
        for hunter in main.children[0].children:
            if ('Bear' in hunter.source): bears.append(81 - main.children[0].children.index(hunter))
        for hunter in main.children[0].children:
            if ('Bear_2' in hunter.source): bears.append(81 - main.children[0].children.index(hunter))
        print(bears)
        if (len(bears) > 1): turn += 1
        for obstacle in main.children[0].children:
            if (
                    'Player' not in obstacle.source and 'Bear' not in obstacle.source and 'Transparent' not in obstacle.source and 'Jewel' not in obstacle.source): loc = (
                        81 - main.children[0].children.index(obstacle)); obstacles.append(
                (loc % 9 if (loc % 9 != 0) else 9, math.ceil(loc / 9)))
        if (turn % 2 == 0):
            position = bears[0]
        else:
            position = bears[1]
        print('the bear is going to be here ' + str(position))
        print('the bears are here ' + str(bears))
        print('turn is ' + str(turn))
        hunterCol = position % 9 if (position % 9 != 0) else 9
        hunterRow = math.ceil(position / 9)
        preyCol = prey % 9 if (prey % 9 != 0) else 9
        preyRow = math.ceil(prey / 9)
        # for tuple in obstacles:
        #	if (tuple[0] == hunterCol + 1 or hunterCol - 1 and hunterRow == tuple[1]) and not ((tuple[0] == hunterCol + 1 and tuple[1] == hunterRow + 1) or (tuple[0] == hunterCol - 1 and tuple[1] == hunterRow - 1)): canX = False
        # for tuple in obstacles:
        #	if (tuple[1] == hunterRow + 1 or hunterRow - 1 and hunterCol == tuple[0]) and not ((tuple[0] == hunterCol + 1 and tuple[1] == hunterRow + 1) or (tuple[0] == hunterCol - 1 and tuple[1] == hunterRow - 1)): canY = False
        print('obstacles are here:')
        print(obstacles)
        prevPos = main.children[0].children[81 - position].source
        if (not canX and not canY and reverse): return  # exec(reverse); return
        if (hunterRow > preyRow and canY):
            main.children[0].children[81 - position].moveUp()
            print('moved up')
            reverse = 'main.children[0].children[81 - position].moveDown()'
        # return
        elif (hunterRow < preyRow and canY):
            main.children[0].children[81 - position].moveDown()
            print('moved down')
            reverse = 'main.children[0].children[81 - position].moveUp()'
        # return
        else:
            if (hunterCol < preyCol and canX):
                main.children[0].children[81 - position].moveRight()
                print('moved right')
                reverse = 'main.children[0].children[81 - position].moveLeft()'
            # return
            elif (hunterCol > preyCol and canX):
                main.children[0].children[81 - position].moveLeft()
                print('moved left')
                reverse = 'main.children[0].children[81 - position].moveRight()'
            # return
            elif (hunterCol == preyCol and hunterRow == preyRow and sm.current != 'Winner' and justGoaled):
                print('lost through towards method'); self.clearGoal(); Clock.schedule_once(self.loser,
                                                                                            1); return  # sm.current = 'Loser'
            elif (hunterCol == preyCol and hunterRow == preyRow and sm.current != 'Winner'):
                print('lost through towards method'); Clock.schedule_once(self.loser, 1); return
        if (prevPos == main.children[0].children[81 - position].source):
            if ('Bear_2' in main.children[0].children[81 - position].source):
                main.children[0].children[81 - position].source = 'icons/ICON_Bear_Flash.jpg'; Clock.schedule_once(
                    lambda dt: main.children[0].children[81 - position].unflash('two'), 0.1)
            else:
                main.children[0].children[81 - position].source = 'icons/ICON_Bear_Flash.jpg'; Clock.schedule_once(
                    lambda dt: main.children[0].children[81 - position].unflash('one'), 0.1)

# ////////////////////////////////////////////////////////////////   # //															//
# //						  POPUPS							// # //															//
    # ////////////////////////////////////////////////////////////////

    def quitPop(self):  # QUIT POPUP
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


# Builder.load_file('display.kv')
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # (WHITE)

# ////////////////////////////////////////////////////////////////
# //					 CREATE GRID/ACTORS	//
# ////////////////////////////////////////////////////////////////

#creates a 9 * 9 grid
grid = GridLayout(id='grid', cols=13, rows=7, padding=15, spacing=1.5) 


#sets the background image
bg = Image(source='images/BG.jpg', size_hint=[1, 1])

for i in range(0, grid.cols * grid.rows): #adds the transparent image to all 81 boxes
    b = Actor(id='actor' + str(i + 1), source='icons/ICON_Transparent.png', size_hint=[1, 1])
    grid.add_widget(b)

main = MainScreen(name='main') #creates a main screen
main.add_widget(bg) #adds background to the screen
main.add_widget(grid) #adds grid to the scren

sm.add_widget(main)
'''
#creates winner screen
screen = Screen(name="Winner")
youWinner = Image(source='winner/winner.jpg')
screen.add_widget(youWinner)

#creates loser screen
loserScreen = Screen(name="Loser")
youLoser = Image(source='loser/loser.jpg')
loserScreen.add_widget(youLoser)

#creates labels
winLabel = Label(text='You win!', font_size=64, pos=(0, 400))
scoreLabel = Label(text='', font_size=16, pos=(0, 350))
loseLabel = Label(text='You lost.', font_size=64, pos=(0, 400))

#Buttons should be put in main.py

playAgainButton = Button(text='Play again?', size_hint=(0.2, 0.1), pos=(Window.width * .4, 0))
playAgainButton.bind(on_press=lambda x: reset('normal'))

playAgainButtonHard = Button(text='Make it harder?', size_hint=(0.2, 0.1),
                             pos=(Window.width * .75, Window.height * .85))
playAgainButtonHard.bind(on_press=lambda x: reset('hard'))

playAgainButtonLose = Button(text='Play again?', size_hint=(0.2, 0.1), pos=(Window.width * .4, 0))
playAgainButtonLose.bind(on_press=lambda x: reset('normal'))

screen.add_widget(winLabel)
screen.add_widget(scoreLabel)
#screen.add_widget(playAgainButton)
#screen.add_widget(playAgainButtonHard)
loserScreen.add_widget(loseLabel)
#loserScreen.add_widget(playAgainButtonLose)
sm.add_widget(screen)
sm.add_widget(loserScreen)
'''

'''
for actor in main.children[0].children: #creates an array with the actors
    if (actor.id == 'actor1'):
        actor.source = 'players/ICON_Player.jpg'

    if (actor.id == 'actor17'):
        actor.source = 'icons/ICON_Igloo.jpg'

    if (actor.id == 'actor81'):
        actor.source = 'icons/ICON_Goal.jpg'

    if (actor.id == 'actor40'):
        actor.source = 'icons/ICON_Jewel.jpg'

    if (actor.id == 'actor54'):
        actor.source = 'icons/ICON_Bear.jpg'
'''

if __name__ == "__main__":
    MyApp().run()

