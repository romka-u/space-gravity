import random

class Bonus(object):
	class BonusType(object):
		SHRINK = 1
		ENLARGE = 2
		ELECTRO = 3
		AIMING = 4
		TRIPLE = 5
 
		types = (SHRINK, ENLARGE, ELECTRO) #, AIMING, TRIPLE)
		colors = ((0, 128, 255), (128, 0, 255), (128, 255, 255), (128, 255, 0), (255, 128, 128))

	@staticmethod
	def color(type):
		return Bonus.BonusType.colors[Bonus.BonusType.types.index(type)]

	def __init__(self):
		self.type = random.choice(self.BonusType.types)
		self.rad = 10

		self.DELTA = 2
		self.DELTA_MAX = 26

		self.dwh = -self.DELTA_MAX
		self.delta = self.DELTA