
from player import Player
from gameutil import dist, place
from drawutil import fill_gradient
from bullet import Bullet
from options import Options
from image_holder import ImageHolder
from bonus import Bonus
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
        self.players = [Player("red"), Player("blue")]
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

        # for pl in self.players:
        #     pl.bonustype = None

        self.bullet = None


    def end_round(self, loser):
        winner = 1 - self.players.index(loser)
        self.players[winner].score += 1

        self.active_player ^= 1
        if android:
            android.vibrate(1)

        self.init_round()


    def move_objects(self):
        """
        Moves bonuses and bullets.
        Checks whether bullet has collided with some other object
        """
        if self.bonus is not None:
            b = self.bonus
            b.dwh += b.delta
            if b.dwh == b.DELTA_MAX: b.delta = -b.DELTA
            if b.dwh == -b.DELTA_MAX: b.delta = b.DELTA

        if self.bullet is not None:
            if not self.bullet.is_visible_far():
                self.bullet = None
                self.active_player ^= 1
                return

            ndx, ndy = 0, 0
            for planet in self.planets:
                d = dist(planet, self.bullet)
                angle_to_planet = math.atan2(planet.y - self.bullet.y,
                                             planet.x - self.bullet.x)
                d = d ** 1.8
                ndx += math.cos(angle_to_planet) * planet.force / d
                ndy += math.sin(angle_to_planet) * planet.force / d

            self.bullet.turn(ndx/320, ndy/320)
            self.bullet.move()

            for planet in self.planets:
                d = dist(planet, self.bullet)

                # check if the bullet is near the planet
                if d < planet.rad:

                    # if player has used BonusType.ENLARGE
                    if self.bullet.bonustype == Bonus.BonusType.ENLARGE:
                        planet.rad += planet.rad / 3
                        for player in self.players:
                            if dist(planet, player) < planet.rad + player.rad:
                                self.end_round(loser=player)
                                return
                                # score point

                    # if player has used BonusType.SHRINK
                    if self.bullet.bonustype == Bonus.BonusType.SHRINK:
                        planet.rad -= planet.rad / 3

                    # recalc planet force just in case
                    planet.force = planet.rad ** 2 * planet.density

                    # kill bullet and change player
                    self.bullet = None
                    self.active_player ^= 1
                    return

            for player in self.players:
                gap = 0
                if self.bullet.bonustype == Bonus.BonusType.ELECTRO and\
                    player != self.bullet.owner:
                    gap = 30
                if dist(player, self.bullet) < Player.PLAYER_RAD + gap:
                    self.end_round(loser=player)
                    return

            if self.bonus is not None:
                d = dist(self.bonus, self.bullet)
                if d <= self.bonus.rad + 1:
                    self.players[self.active_player].bonustype = self.bonus.type
                    self.bonus = None
                    self.bullet = None
                    self.active_player ^= 1
                    return


    def draw(self, screen):
        """
        Draw everything in game, such as panel, players, planets, bullets, bonuses, status bar.
        """

        pl = self.players[self.active_player]
        
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
            rotated = pygame.transform.rotozoom(
                self.images.spaceship[player.color], angle, 1.0 / scale)
            rect = rotated.get_rect()
            rect.center = coord(player.x, player.y)
            screen.blit(rotated, rect)

        for planet in self.planets:
            scaled = pygame.transform.scale(self.images.planets[planet.type], 
                (planet.rad * 2 / scale + 1, planet.rad * 2 / scale + 1))
            rect = scaled.get_rect()
            rect.center = coord(planet.x, planet.y)
            screen.blit(scaled, rect)

        if self.bonus is not None:
            b = self.bonus
            dw = b.dwh / 10
            dh = -dw
            rect = pygame.Rect(
                coord(b.x - b.rad - dw, b.y - b.rad - dh),
                ((b.rad + dw) * 2 / scale, (b.rad + dh) * 2 / scale)
            )
            # print rect
            # print b.x, b.y, b.rad, b.dwh, "->", dw, dh
            pygame.draw.ellipse(screen, Bonus.color(self.bonus.type), rect)

        if self.bullet is not None:
            bullet_color = (255, 255, 255)
            if self.bullet.bonustype is not None:
                bullet_color = Bonus.color(self.bullet.bonustype)
            pygame.draw.circle(screen, bullet_color,
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
        
        if pl.bonustype is not None:
            pygame.draw.rect(screen, Bonus.color(pl.bonustype),
                self.Boxes.extra_button_box, 1)

            circle_rad = int(self.Boxes.extra_button_box.width * 0.5 * 0.8)
            pygame.draw.circle(screen, Bonus.color(pl.bonustype),
                self.Boxes.extra_button_box.center, circle_rad)


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

            if pl.bonustype is not None and\
                self.Boxes.extra_button_box.collidepoint(coord):
                self.try_fire(pl.bonustype)
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
                pl.set_power((self.Boxes.power_box.bottom - self.last_y) * 1.0\
                             / self.Boxes.power_box.height)
        

        self.is_power_box_tapped = False
        self.is_field_tapped = False
        self.was_motion = False


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


    def try_fire(self, bonustype=None):
        pl = self.players[self.active_player]
        if self.bullet is None:
            self.bullet = Bullet(pl.x + math.cos(pl.heading) * Player.PLAYER_RAD,
                                 pl.y + math.sin(pl.heading) * Player.PLAYER_RAD,
                                 pl.heading, pl.power, bonustype, pl)
            if bonustype is not None: pl.bonustype = None