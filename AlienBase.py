# Written with the help of Chat GPT4o

import random
from LightStrip import *

class AlienBase:
    def __init__(self, color=None):
        #Initialize the AlienBase with a color 
        if color:
            self._color = color
        else:
            colors = [WHITE, RED, YELLOW, BLUE]
            self._color = random.choice(colors)

    def getColor(self):
        #Return the color of the alien base
        return self._color

    def setColor(self, color):
        #Set a new color for the alien base
        self._color = color

