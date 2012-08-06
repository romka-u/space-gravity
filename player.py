
class Player(object):

    PLAYER_RAD = 25
    
    def __init__(self, color):
        self.x, self.y = 0, 0
        self.rad = self.PLAYER_RAD
        self.heading = 0
        self.power = 100
        self.color = color
        self.bonuses = []
