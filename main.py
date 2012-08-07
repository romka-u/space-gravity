#!/usr/local/bin/python2.7-32

import pygame
from pygame.locals import *

from options import Options
from game import Game
import sys

try:
    import android
except:
    android = None

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class SpaceGravityMain(object):

    def __init__(self, width=1024, height=768):
        pygame.init()

        Options.Video.view_width = int(width * 0.9)
        Options.Video.full_width = width
        Options.Video.height = height

        pygame.key.set_repeat(30, 30)

        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            android.map_key(android.KEYCODE_MENU, pygame.K_SPACE)
        
        self.game = Game()
        self.screen = pygame.display.set_mode((width, height))


    def main(self):

        clock = pygame.time.Clock()
        """This is the main loop of the game"""
        while True:

            if android:
                if android.check_pause():
                    android.wait_for_resume()

            clock.tick(70)
            # pygame.display.set_caption("FPS: %.3f" % clock.get_fps())
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

            if event.type == MOUSEBUTTONDOWN:
                self.game.process_tap(pygame.mouse.get_pos())

            if event.type == MOUSEBUTTONUP:
                self.game.process_up(pygame.mouse.get_pos())

            if event.type == MOUSEMOTION:
                self.game.process_motion()


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.game.draw(self.screen)
        pygame.display.flip()


# main procedure
def main():
    instance = SpaceGravityMain(800, 480)
    instance.main()

if __name__ == "__main__":
    main()
