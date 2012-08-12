
class Player(object):

    PLAYER_RAD = 23
    MAX_BULLET_POWER = 10.0
    MIN_BULLET_POWER = 1.0
    TOTAL_POWER = MAX_BULLET_POWER - MIN_BULLET_POWER
    
    def __init__(self, color):
        self.x, self.y = 0, 0
        self.rad = self.PLAYER_RAD
        self.heading = 0
        self.power = 100
        self.color = color
        self.power = 4.5


    def get_rest_power_coeff(self):
        return (self.MAX_BULLET_POWER - self.power) / self.TOTAL_POWER


    def change_power(self, amount):
        self.power += amount
        self.fix_power()


    def set_power(self, coeff):
        self.power = self.MIN_BULLET_POWER + self.TOTAL_POWER * coeff
        self.fix_power()


    def fix_power(self):
        if self.power > self.MAX_BULLET_POWER:
            self.power = self.MAX_BULLET_POWER
        if self.power < self.MIN_BULLET_POWER:
            self.power = self.MIN_BULLET_POWER
