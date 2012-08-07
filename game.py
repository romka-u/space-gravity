
from player import Player
from gameutil import dist, place
from drawutil import fill_gradient
from planet import Planet
from bullet import Bullet
from options import Options
from pygame.locals import *

import random
import pygame
import math

class Game(object):

    PLANETS_GAP = 30
    PLAYERS_GAP = 115

    class Boxes: pass

    def __init__(self):
        self.players = [Player((180, 0, 0)), Player((0, 0, 180))]
        self.first_player = 0

        self.init_round()

        # Init panel coordinates
        width = Options.Video.full_width - Options.Video.view_width - 3
        height = Options.Video.height
        sep_x = Options.Video.view_width + 3
        sep_y1 = int(0.2 * height)
        sep_y2 = int(0.4 * height)

        self.Boxes.power_box = Rect(
            sep_x + 3,
            sep_y2 + 3,
            width - 6,
            height - sep_y2 - 6
        )

        self.Boxes.fire_button_box = Rect(
            sep_x + 3,
            3,
            width - 6,
            sep_y1 - 6
        )

        self.Boxes.extra_button_box = Rect(
            sep_x + 3,
            sep_y1 + 3,
            width - 6,
            sep_y2 - sep_y1 - 6
        )


    def init_round(self):
        self.gen_planets()
        self.gen_players()

        self.active_player = self.first_player
        self.first_player = 1 - self.active_player

        self.bullet = None

    
    def gen_planets(self):
        planets_count = random.randint(4, 8)
        planets_count = 1
        while True:
            self.planets = [Planet()
                            for _ in xrange(planets_count)]

            p = self.planets
            if all(dist(p[i], p[j]) >
                   p[i].rad + p[j].rad + self.PLANETS_GAP
                   for i in xrange(planets_count)
                   for j in xrange(i)): break


    def gen_players(self):
        for ind, pl in enumerate(self.players):
            while True:
                place(pl)
                p = self.planets
                if any(dist(pl, self.players[i]) <
                       pl.rad + self.players[i].rad + self.PLAYERS_GAP
                       for i in xrange(ind)): continue
                if all(dist(pl, p[i]) >
                       pl.rad + p[i].rad + self.PLANETS_GAP
                       for i in xrange(len(p))): break


    def move_objects(self):
        if self.bullet is not None:
            if not self.bullet.is_visible():
                self.bullet = None
                self.active_player ^= 1
                return

            ndx, ndy = 0, 0
            for planet in self.planets:
                d = dist(planet, self.bullet)
                if d < planet.rad:
                    self.bullet = None
                    self.active_player ^= 1
                    return
                angle_to_planet = math.atan2(planet.y - self.bullet.y,
                                             planet.x - self.bullet.x)
                d = d ** 1.8
                ndx += math.cos(angle_to_planet) * planet.force / d
                ndy += math.sin(angle_to_planet) * planet.force / d

            self.bullet.turn(ndx/320, ndy/320)
            self.bullet.move()

            for player in self.players:
                if dist(player, self.bullet) < Player.PLAYER_RAD:
                    self.bullet = None
                    self.init_round()
                    return
                    # score 1 point to active_player


    def draw(self, screen):
        for planet in self.planets:
            pygame.draw.circle(screen, (0, 20 + planet.density * 2, 0),
                (planet.x, planet.y), planet.rad)

        for player in self.players:
            by_angle = lambda an: (player.x + math.cos(an) * Player.PLAYER_RAD,
                                   player.y + math.sin(an) * Player.PLAYER_RAD)

            an = player.heading
            points = [by_angle(an), by_angle(an+2.7), by_angle(an-2.7)]
            pygame.draw.polygon(screen, player.color, points, 2)

        if self.bullet is not None:
            pygame.draw.circle(screen, (255, 255, 255),
                (int(self.bullet.x), int(self.bullet.y)), 3)

        # draw panel
        pygame.draw.line(screen, (255, 255, 255),
            (Options.Video.view_width, 0),
            (Options.Video.view_width, Options.Video.height),
            2)

        # draw pretty gradient as power
        half_box = Rect(
            self.Boxes.power_box.topleft,
            (self.Boxes.power_box.width, self.Boxes.power_box.height / 2)
        )

        fill_gradient(screen, half_box, (255, 0, 0), (255, 255, 0))
        half_box.centery += self.Boxes.power_box.height / 2
        fill_gradient(screen, half_box, (255, 255, 0), (0, 255, 0))

        pl = self.players[self.active_player]
        coeff = pl.get_rest_power_coeff()
        empty_box = Rect(
            self.Boxes.power_box.topleft,
            (self.Boxes.power_box.width, int(self.Boxes.power_box.height * coeff))
        )

        pygame.draw.rect(screen, (0, 0, 0), empty_box)

        pygame.draw.rect(screen, (255, 255, 255),
            self.Boxes.power_box, 1)

        pygame.draw.rect(screen, (128, 0, 255),
            self.Boxes.fire_button_box, 1)

        pygame.draw.rect(screen, (255, 0, 128),
            self.Boxes.extra_button_box, 1)


    def process_tap(self, coord):
        pl = self.players[self.active_player]
        x, y = coord[0], coord[1]
        pl.heading = math.pi / 2 - math.atan2(x - pl.x, y - pl.y)


    def process_key(self, key):
        pl = self.players[self.active_player]
        if key == K_LEFT: pl.heading -= 0.037
        if key == K_RIGHT: pl.heading += 0.037
        if key == K_UP: pl.change_power(+0.05)
        if key == K_DOWN: pl.change_power(-0.05)
        if key == K_SPACE:
            if self.bullet is None:
                self.bullet = Bullet(pl.x + math.cos(pl.heading) * Player.PLAYER_RAD,
                                     pl.y + math.sin(pl.heading) * Player.PLAYER_RAD,
                                     pl.heading, pl.power)
