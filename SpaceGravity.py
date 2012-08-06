#!/usr/local/bin/python2.7-32

import pygame
from pygame.locals import *

from options import Options
from game import Game
import sys

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class SpaceGravityMain(object):

    def __init__(self, width=1024, height=768):
        pygame.init()

        Options.Video.width = width
        Options.Video.height = height

        pygame.key.set_repeat(30, 30)
        
        self.game = Game()
        self.screen = pygame.display.set_mode((width, height))


    def main(self):

        clock = pygame.time.Clock()
        """This is the main loop of the game"""
        while True:
            clock.tick(70)
            pygame.display.set_caption("FPS: %.3f" % clock.get_fps())
            self.process_events()
            self.game.move_objects()
            self.draw()


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: sys.exit(0)
                self.game.process_key(event.key)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.game.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    instance = SpaceGravityMain(1024, 768)
    instance.main()
