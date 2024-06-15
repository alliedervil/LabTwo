# Written with the help of Chat GPT4o

import time
import random
from StateModel import *
from Counters import *
from Displays import LCDDisplay 
from LightStrip import *
from Log import *
from Button import *
from Buzzer import *
from AlienBase import *
from Player import *

class GameController:

    def __init__(self):
        """
        Initialize the GameController with buttons, light strip, display, buzzer, 
        timer, alien base, and player. Also, set up the state model and transitions.
        """
        # Initialize buttons with their respective pins and colors
        self._button1 = Button(10, "white", buttonhandler=None)
        self._button2 = Button(11, "red", buttonhandler=None)
        self._button3 = Button(12, "yellow", buttonhandler=None)
        self._button4 = Button(13, "blue", buttonhandler=None)

        # Initialize the light strip with pin and number of LEDs
        self._lightstrip = LightStrip(pin=2, numleds=16)

        # Initialize the LCD display with I2C pins
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)

        # Initialize the buzzer with its pin
        self._buzzer = PassiveBuzzer(16)

        # Initialize a software timer with the game controller as the handler
        self._timer = SoftwareTimer(handler=self)

        # Initialize the alien base and player
        self._alienbase = AlienBase()
        self._player = Player()
        self._player.score = 0
        
        # Create an array to hold alien bases
        self._allbases = [None] * 3
        for x in range(3):
            self._allbases[x] = AlienBase()

        # Initialize the state model with states and debugging enabled
        self._model = StateModel(7, self, debug=True)
        
        # Add buttons to the state model
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        self._model.addButton(self._button3)
        self._model.addButton(self._button4)

        # Add timer to the state model
        self._model.addTimer(self._timer)
        
        # Define state transitions
        self._model.addTransition(0, [BTN1_PRESS, BTN2_PRESS, BTN3_PRESS, BTN4_PRESS], 1)
        self._model.addTransition(1, [BTN1_PRESS], 2)
        self._model.addTransition(2, [TIMEOUT], 1)
        self._model.addTransition(1, [BTN2_PRESS], 3)
        self._model.addTransition(3, [TIMEOUT], 1)
        self._model.addTransition(1, [BTN3_PRESS], 4)
        self._model.addTransition(4, [TIMEOUT], 1)
        self._model.addTransition(1, [BTN4_PRESS], 5)
        self._model.addTransition(5, [TIMEOUT], 1)
        self._model.addTransition(6, [TIMEOUT], 0)

    def shoot(self, color):
        """
        Handle the shooting mechanism in the game. If the shot color matches the last alien base,
        update the score and light strip accordingly.
        """
        if len(self._allbases) > 0:
            lastbase = self._allbases[len(self._allbases) - 1]
            if lastbase.getColor() == color:
                for x in range(0, 16 - len(self._allbases) + 1):
                    self._lightstrip.setPixel(x, color)
                    time.sleep(0.01)
                    self._lightstrip.setPixel(x, BLACK)
                self._allbases.pop()
                self._player.score += 1
                self._display.showText(f'Score: {self._player.score}')
                Log.d(f'Shot an alien base!')
            else:
                for x in range(0, 16 - len(self._allbases)):
                    self._lightstrip.setPixel(x, color)
                    time.sleep(0.01)
                    self._lightstrip.setPixel(x, BLACK)
                Log.d(f'Missed!')

    def restart(self):
        """
        Restart the game by resetting all bases and the player's score.
        """
        for x in range(len(self._allbases)):
            totalbases = self._allbases[x]
            if totalbases != None:
                self._lightstrip.setPixel(15 - x, BLACK, show=False)
        self._lightstrip.show()
        self._allbases = [None] * 3
        for x in range(3):
            self._allbases[x] = AlienBase()
        self._player.score = 0
        Log.d(f'Restarting Game')
    
    def addBases(self):
        """
        Add a new alien base to the game.
        """
        self._allbases.append(AlienBase())

    def showBases(self):
        """
        Display the alien bases on the light strip.
        """
        for x in range(len(self._allbases)):
            allbases = self._allbases[x]
            if allbases != None:
                self._lightstrip.setPixel(15 - x, allbases.getColor(), show=False)
        self._lightstrip.show()

    def run(self):
        """
        Run the state model to start the game.
        """
        self._model.run()

    def stateDo(self, state):
        """
        Define actions to be performed in each state.
        """
        if state == 0:
            pass 
        elif state == 1:
            time.sleep(1)
            self.addBases()
            self.showBases()
            if len(self._allbases) == 16:
                self._model.gotoState(6)
            Log.d(f'Adding Bases')

    def stateEntered(self, state, event):
        """
        Log state entry and perform specific actions for each state.
        """
        Log.d(f'State {state} Entered')
        if state == 0:
            self.restart()
            self._display.reset()
            self._display.showText('Press any button to start')
        
        elif state == 1:
            self.addBases()
            self.showBases()
            if len(self._allbases) == 16:
                self._model.gotoState(6)

        elif state == 2:
            Log.d(f'Shot white')
            self.shoot(WHITE)
            self._timer.start(1)
        
        elif state == 3:
            Log.d(f'Shot red')
            self.shoot(RED)
            self._timer.start(1)
        
        elif state == 4:
            Log.d(f'Shot yellow')
            self.shoot(YELLOW)
            self._timer.start(1)
        
        elif state == 5:
            Log.d(f'Shot blue')
            self.shoot(BLUE)
            self._timer.start(1)

        elif state == 6:
            self._display.reset()
            self._display.showText(f'FINAL SCORE: {self._player.score}')
            Log.d(f'Good Job!')
            self._timer.start(5)
            
    def stateLeft(self, state, event):
        """
        Log state exit and cancel the timer if necessary.
        """
        Log.d(f'State {state} exited')
        if state == 0:
            self._display.reset()
        elif state in (1, 2, 3, 4, 5, 6):
            self._timer.cancel()
        if state in (1, 2, 3, 4, 5):
            self._display.showText(f'Score: {self._player.score}')
    

if __name__ == '__main__':
    # Run the game controller when the script is executed
    GameController().run()



