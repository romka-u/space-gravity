
from gameutil import place
from random import randint

class Planet:
    
    def __init__(self):
        MIN_PLANET_RAD = 15
        MAX_PLANET_RAD = 180
        self.rad = randint(MIN_PLANET_RAD, MAX_PLANET_RAD)
        self.density = randint(20, 50)
        self.force = self.rad ** 2 * self.density
        place(self)
