
import pygame
import os


class ImageHolder(object):

    def __init__(self):
        self.spaceship = {"red": self.load("spaceship_small_red.png"),
                          "blue": self.load("spaceship_small_blue.png")}

        planets_names = ["planet2.gif", "planet6.png",
            "planet3.gif", "planet4.gif", "planet5.png"]
        self.planets = [self.load(pl) for pl in planets_names]


    def load(self, filename):
        return pygame.image.load(os.path.join("img", filename))
