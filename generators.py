
from planet import Planet
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
        if check_difficulty(game.planets, game.players): break
      

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


def check_difficulty(planets, players):
    x1, y1 = players[0].x, players[0].y
    x2, y2 = players[1].x, players[1].y
    c = dist(players[0], players[1])
    A, B = y2-y1, x1-x2
    C = -x1 * A - y1 * B

    good = False
    for p in planets:
        a = dist(players[0], p)
        b = dist(players[1], p)
        if a*a + c*c < b*b or b*b + c*c < a*a: continue
        d = math.fabs(A * p.x + B * p.y + C) / math.sqrt(A*A + B*B)

        if d < Const.CLOSE_DISTANCE + p.rad:
            good = True
            break

    return good