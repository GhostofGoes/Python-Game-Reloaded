import pygame

global FPSCLOCK, DISPLAYSURF, FPS


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (22, 226, 15)


pygame.init()
FPS = 30 # frames per second
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Game')

	