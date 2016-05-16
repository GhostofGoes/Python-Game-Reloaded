import functions
import random
import Enemy
import Potions
import Weapon

ENEMYDROPRATE = 1
CHESTDROPRATE = 5
BOSSDROPRATE = 10



class Inventory:
	items = []
	coins = 0
	
	'''seemingly redundant, but because of how enemies are made, they will have different base items. 
	Therefore, pass their items in a list, to inventory for easier keeping and function stuff. ALso, drops'''
	def __init__(self, droprate, inventory):
		if (len(inventory) >0):
			for item in (inventory):
				self.items.append(item)
				
		self.coins = random.randint(droprate, int(droprate*2))
		if droprate >= 5:
			for extraCoin in range(5, droprate):
				self.coins += 5
			self.items.append(Weapon.MeleeWeapon())
			hp = Potions.Potion() #Create the potion
			hp.setToHealthPotion()
			self.items.append(hp)
		else:
			chanceHavePotion = random.randint(0,10)#1/10 chance for potion
			if chanceHavePotion %9 == 0:
				hp = Potions.Potion() #Create the potion
				hp.setToHealthPotion()
				self.items.append(hp)
	
	
	def printInventory(self):
		if (len(self.items) > 0):
			for item in (self.items):
				print "%s, in inventory" % (item.name)
				