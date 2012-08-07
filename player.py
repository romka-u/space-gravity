
class Player(object):

    PLAYER_RAD = 25
    MAX_BULLET_POWER = 10.0
    MIN_BULLET_POWER = 1.0
    
    def __init__(self, color):
        self.x, self.y = 0, 0
        self.rad = self.PLAYER_RAD
        self.heading = 0
        self.power = 100
        self.color = color
        self.bonuses = []
        self.power = 2.5


    def get_rest_power_coeff(self):
        return (self.MAX_BULLET_POWER - self.power) /\
               (self.MAX_BULLET_POWER - self.MIN_BULLET_POWER)


    def change_power(self, amount):
        self.power += amount
        if self.power > self.MAX_BULLET_POWER:
            self.power = self.MAX_BULLET_POWER
        if self.power < self.MIN_BULLET_POWER:
            self.power = self.MIN_BULLET_POWER
