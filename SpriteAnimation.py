import pygame
import Display

# http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images
class SpriteAnimation(pygame.sprite.Sprite):

	def __init__(self, sprites):
		super(SpriteAnimation, self).__init__()
		self.counter = 0
		self.images = sprites
		self.index = 0
		self.image = self.images[self.index]
		self.rect = pygame.Rect(5, 5, Display.TILE_SIZE, Display.TILE_SIZE)
	
	def update(self, x, y, flip, rotate):
		self.counter += 1 
		self.rect = pygame.Rect(x, y, 64, 64) 
		if self.counter > 10: # after ten clicks switch sprites
			self.counter = 0
			self.index += 1
			if self.index >= len(self.images):
				self.index = 0
			if flip:
				self.image = pygame.transform.flip(self.images[self.index], True, False)
			if rotate > 0:
				self.image = pygame.transform.rotate(self.images[self.index], rotate)
			else:
				self.image = self.images[self.index]
		self.draw(Display.DISPLAYSURF)
	
	def resetSpriteList(self):
		self.index = 0
		self.counter = 11
		
	def changeSprites(self, sprites):
		self.counter = 0
		self.index = 0
		self.images = sprites
		self.image = self.images[self.index]
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)
	
	