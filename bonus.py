import random

class Bonus(object):
	class BonusType(object):
		SHRINK = 1
		ENLARGE = 2
		ELECTRO = 3
		AIMING = 4
		TRIPLE = 5

		types = (SHRINK, ENLARGE, ELECTRO, AIMING, TRIPLE)
		colors = ((0, 128, 255), (128, 0, 255), (128, 255, 255), (128, 255, 0), (255, 128, 128))

	def __init__(self):
		t = random.randint(0, len(self.BonusType.types)-1)
		self.type = self.BonusType.types[t]
		self.color = self.BonusType.colors[t]
		self.rad = 10

		self.DELTA = 2
		self.DELTA_MAX = 26

		self.dwh = -self.DELTA_MAX
		self.delta = self.DELTA