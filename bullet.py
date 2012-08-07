
from options import Options
import math

class Bullet(object):

    def __init__(self, x, y, heading, speed):
        self.x, self.y = x, y
        self.dx = math.cos(heading) * speed
        self.dy = math.sin(heading) * speed


    def turn(self, ndx, ndy):
        self.dx += ndx
        self.dy += ndy


    def move(self):
        self.x += self.dx
        self.y += self.dy
        

    def is_visible(self):
        return self.x > 0 and self.y > 0 and\
               self.x < Options.Video.view_width and\
               self.y < Options.Video.height
