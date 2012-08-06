
from random import randint
from options import Options
import math

def place(entity):
    entity.x = rand_pos(0, Options.Video.width, entity.rad)
    entity.y = rand_pos(0, Options.Video.height, entity.rad)


def rand_pos(low, high, rad):
    assert(low + rad <= high - rad)
    return randint(low + rad, high - rad)


def dist(entity1, entity2):
    return math.sqrt((entity1.x - entity2.x) ** 2 +
                     (entity1.y - entity2.y) ** 2)
