
import pygame
import os


class ImageHolder(object):

    def __init__(self):
        self.spaceship = self.load("spaceship_small.png")

        planets_names = ["planet2.gif",
        	"planet3.gif", "planet4.gif", "planet5.jpg"]
        self.planets = [self.load(pl) for pl in planets_names]


    def load(self, filename):
        return pygame.image.load(os.path.join("img", filename))
