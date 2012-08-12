
from gameutil import place
from random import randint
from options import Options

import math

class Planet:
    
    def __init__(self):
        MIN_PLANET_RAD = 15
        MAX_PLANET_RAD = int(math.sqrt(Options.Video.height * Options.Video.view_width / 70))
        self.rad = randint(MIN_PLANET_RAD, MAX_PLANET_RAD)
        self.density = randint(20, 50)
        self.force = self.rad ** 2 * self.density
        self.type = randint(0, 3)
        place(self)
