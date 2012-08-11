import random

class Bonus(object):
	class BonusType(object):
		SHRINK = 1
		ENLARGE = 2
		ELECTRO = 3
		AIMING = 4
		TRIPLE = 5

		TYPES = (SHRINK, ENLARGE, ELECTRO, AIMING, TRIPLE)

	def __init__(self):
		self.type = random.choice(self.BonusType.types)