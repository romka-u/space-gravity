
import pygame
import os


class ImageHolder(object):

    def __init__(self):
        self.spaceship = self.load("spaceship_small.png")


    def load(self, filename):
        return pygame.image.load(os.path.join("img", filename))
