
from planet import Planet
from bonus import Bonus
from gameutil import dist, place

import random
import math


class Const(object):
    PLANETS_GAP = 35
    CLOSE_DISTANCE = 10


def generate_round(game):
    while True:
        gen_planets(game)
        gen_players(game)
        gen_bonus(game)
        if check_difficulty(game.planets, game.players, game.bonus): break
      

def gen_planets(game):    
    planets_count = random.randint(4, 8)
    while True:
        game.planets = [Planet()
                        for _ in xrange(planets_count)]

        p = game.planets
        if all(dist(p[i], p[j]) >
               p[i].rad + p[j].rad + Const.PLANETS_GAP
               for i in xrange(planets_count)
               for j in xrange(i)): break


def gen_players(game):
    for ind, pl in enumerate(game.players):
        while True:
            place(pl)
            p = game.planets
            if any(dist(pl, game.players[i]) <
                   pl.rad + game.players[i].rad
                   for i in xrange(ind)): continue
            if all(dist(pl, p[i]) >
                   pl.rad + p[i].rad + Const.PLANETS_GAP
                   for i in xrange(len(p))): break

def gen_bonus(game):
    gen = True
    game.bonus = Bonus()
    while gen:
        gen = False
        place(game.bonus)

        for pl in game.players + game.planets:
            if dist(pl, game.bonus) < pl.rad + game.bonus.rad + 2:
                gen = True
                break

def check_difficulty(planets, players, bonus):
    def is_a_planet_between(planets, obj1, obj2):
        x1, y1 = obj1.x, obj1.y
        x2, y2 = obj2.x, obj2.y
        c = dist(obj1, obj2)
        A, B = y2-y1, x1-x2
        C = -x1 * A - y1 * B
        T = math.sqrt(A*A + B*B)

        good = False
        for p in planets:
            a = dist(obj1, p)
            b = dist(obj2, p)
            if a*a + c*c < b*b or b*b + c*c < a*a: continue
            d = math.fabs(A * p.x + B * p.y + C) / T

            if d < Const.CLOSE_DISTANCE + p.rad:
                good = True
                break

        return good

    """ Body of check_difficulty function """
    return is_a_planet_between(planets, players[0], players[1]) and\
           is_a_planet_between(planets, players[0], bonus) and\
           is_a_planet_between(planets, players[1], bonus)