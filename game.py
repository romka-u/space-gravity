
from player import Player
from gameutil import dist, place
from drawutil import fill_gradient
from bullet import Bullet
from options import Options
from image_holder import ImageHolder
from generators import generate_round
from pygame.locals import *

import pygame
import math

try:
    import android
except:
    android = None

class Game(object):

    class Boxes: pass

    def __init__(self):
        self.players = [Player((180, 0, 0)), Player((0, 0, 180))]
        self.first_player = 0

        self.init_round()
        self.images = ImageHolder()

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

        self.is_power_box_tapped = False
        self.is_field_tapped = False


    def init_round(self):
        generate_round(self)

        self.active_player = self.first_player
        self.first_player = 1 - self.active_player

        self.bullet = None
    

    def move_objects(self):
        if self.bullet is not None:
            if not self.bullet.is_visible_far():
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

            for planet in self.planets:
                d = dist(planet, self.bullet)
                if d < planet.rad:
                    self.bullet = None
                    self.active_player ^= 1
                    return

            for player in self.players:
                if dist(player, self.bullet) < Player.PLAYER_RAD:
                    self.bullet = None
                    self.init_round()
                    if android:
                        android.vibrate(1)
                    return
                    # score 1 point to active_player


    def draw(self, screen):
        """for player in self.players:
            by_angle = lambda an: (player.x + math.cos(an) * Player.PLAYER_RAD,
                                   player.y + math.sin(an) * Player.PLAYER_RAD)

            an = player.heading
            points = [by_angle(an), by_angle(an+2.7), by_angle(an-2.7)]
            pygame.draw.polygon(screen, player.color, points, 2)"""

        coord = lambda x, y: (int(x), int(y))
        scale = 1
        if self.bullet is not None and\
           not self.bullet.is_visible_near() and\
           self.bullet.is_visible_far():
            scale = 3
            coord = lambda x, y: (
                int(x / 3 + Options.Video.view_width / 3.0),
                int(y / 3 + Options.Video.height / 3.0)
            )

        for player in self.players:
            angle = -player.heading / math.pi * 180
            rotated = pygame.transform.rotozoom(self.images.spaceship, angle, 1.0 / scale)
            rect = rotated.get_rect()
            rect.center = coord(player.x, player.y)
            screen.blit(rotated, rect)

        for planet in self.planets:
            pygame.draw.circle(screen, (0, 20 + planet.density * 2, 0),
                coord(planet.x, planet.y), planet.rad / scale)

        if self.bullet is not None:
            pygame.draw.circle(screen, (255, 255, 255),
                coord(self.bullet.x, self.bullet.y), 3 / scale)

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

        pygame.draw.rect(screen, (255, 0, 64),
            self.Boxes.fire_button_box, 1)

        pygame.draw.rect(screen, (64, 0, 255),
            self.Boxes.extra_button_box, 1)


    def process_tap(self, coord):
        pl = self.players[self.active_player]
        self.was_motion = False
        self.last_x, self.last_y = coord[0], coord[1]

        if coord[0] >= Options.Video.view_width:
            # tap at the panel
            if self.Boxes.power_box.collidepoint(coord):
                self.is_power_box_tapped = True
                pygame.mouse.get_rel()

            if self.Boxes.fire_button_box.collidepoint(coord):
                self.try_fire()
        else:
            # tap at the field
            self.is_field_tapped = True
            pygame.mouse.get_rel()


    def process_up(self, coord):
        if not self.was_motion:
            pl = self.players[self.active_player]
            if self.is_field_tapped:
                x, y = self.last_x, self.last_y
                pl.heading = math.pi / 2 - math.atan2(x - pl.x, y - pl.y)

            if self.is_power_box_tapped:
                pl.set_power((self.Boxes.power_box.bottom - coord[1]) * 1.0\
                             / self.Boxes.power_box.height)
        

        self.is_power_box_tapped = False
        self.is_field_tapped = False
        self.was_motion = False;


    def process_motion(self):
        rel = pygame.mouse.get_rel()
        pl = self.players[self.active_player]
        self.was_motion = True

        if self.is_power_box_tapped:
            dy = rel[1]
            if dy < -2: dy = -2
            if dy > 2: dy = 2
            pl.change_power(-0.02 * dy)

        if self.is_field_tapped:
            if abs(rel[0]) > abs(rel[1]):
                delta = rel[0]
                if math.sin(pl.heading) > 0: delta = -delta
            else:
                delta = rel[1]
                if math.cos(pl.heading) < 0: delta = -delta

            pl.heading += delta * 0.002


    def process_key(self, key):
        pl = self.players[self.active_player]
        if key == K_LEFT: pl.heading -= 0.037
        if key == K_RIGHT: pl.heading += 0.037
        if key == K_UP: pl.change_power(+0.05)
        if key == K_DOWN: pl.change_power(-0.05)
        if key == K_SPACE: self.try_fire()


    def try_fire(self):
        pl = self.players[self.active_player]
        if self.bullet is None:
            self.bullet = Bullet(pl.x + math.cos(pl.heading) * Player.PLAYER_RAD,
                                 pl.y + math.sin(pl.heading) * Player.PLAYER_RAD,
                                 pl.heading, pl.power)
