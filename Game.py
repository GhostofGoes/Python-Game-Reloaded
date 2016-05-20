'''
Move with left right up down arrow keys
Shoot with a s d w keys
'''

import pygame
from pygame import joystick
import sys
import os
import math
import random
from pygame.locals import *
import Display
import SpriteAnimation
import Player
import Input
import Room
import Enemy
import Weapon
import Combat
import functions
import time
import Spawnner
import Menu
import Inventory
import Beats
#		
# START GAME
#	
items = []
GlobalInventorySys = Inventory.Inventory(1, items)



def main():
	# If any controllers are connected, initialize and enumerate all of them
	controllers = []
	if joystick.get_count():
		print joystick.get_count(), "joysticks detected"
		joystick.init()
		controllers = [joystick.Joystick(x) for x in range(joystick.get_count())]
		Input.listControllers(controllers) # For testing purposes
			
	gameNotOver = True	
	while gameNotOver:
		gameNotOver = runGame()
	print "GAME OVER"
	functions.printPlayerStats()
	os.execl(sys.executable, sys.executable, *sys.argv) # Glorious hack

def restart():
	main()
		
def attack(count, attacker, defender):
	pygame.draw.aaline(Display.DISPLAYSURF, Display.BLACK, (attacker.collisionx, attacker.collisiony), (attacker.weaponx, attacker.weapony+count), 1)

	'''We should consider getting a draw down, 
	background, then loot, then spawners, then enemies, then player?'''
	
def runGame():

	CombatSys = Combat.Combat()
	playerObj = Player.Player()
	dungeonObj = Room.Dungeon(playerObj, 10)
	menuObject = Menu.Menu(playerObj, dungeonObj)
	playerObj.dungeonObj = dungeonObj # temporary, need a better way to pass dungeon info to playerobj
	dungeonObj.playerObj = playerObj
	dungeonObj.menuObject = menuObject
	
	while True:
		# check for key input
		Input.checkForInputs(playerObj, menuObject)
		dungeonObj.update() 
		dungeonObj.update() # duplicate?
		menuObject.update()
		
		playerObj.update()
		playerObj.updateColliders()
		
		if dungeonObj.returnCurrentRoom().hasSpawners:
			for spawnner in dungeonObj.returnCurrentRoom().spawnnerlist:
				spawnner.drawSpawnner()
				spawnner.update()
				if functions.objCollision(playerObj, spawnner):
					CombatSys.attack(playerObj, spawnner)
				if spawnner.isDead:
					dungeonObj.returnCurrentRoom().spawnnerlist.remove(spawnner)
		if dungeonObj.returnCurrentRoom().hasSpawners:
			for enemy in dungeonObj.returnCurrentRoom().enemylist:
				enemy.drawSelf()
				enemy.updateColliders()
				enemy.drawCollider()
				enemy.chaseObj(playerObj)
				if playerObj.isAttacking:
					if functions.objCollision(playerObj, enemy):
						CombatSys.attack(playerObj, enemy)
				if enemy.isDead == True:
					dungeonObj.returnCurrentRoom().enemylist.remove(enemy)
					 


		if functions.worldInventory:
			for item in functions.worldInventory:
				#print "%s" % (item.name)
				item.drawAsLoot()
					
		if functions.worldCoins:
			for coin in functions.worldCoins:
				coin.drawSelf()
				if functions.objCollision(playerObj, coin) == True:
					print "pickup coin"
					functions.worldCoins.remove(coin)
					coin.pickup()
					
			
		# check if the player is alive
		if playerObj.isDead:
			return False

		# draw stuff		
		pygame.display.update()
		Display.FPSCLOCK.tick(Display.FPS)

#
#	END GAME
#

if __name__ == '__main__':
	main()
		
#TODO: redirect stderr to file for logging/debugging purposes