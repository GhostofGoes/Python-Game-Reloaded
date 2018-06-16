import pygame

import Display
import Utils


class NPC:
    NPC_sprite = Utils.load_image('friendly.png')

    def __init__(self, x, y, roomObj, text):
        self.dialogue = text
        self.collisionx = x
        self.collisiony = y
        self.width = 48
        self.height = 48
        self.range = 48
        self.roomObj = roomObj

    def update(self):
        self.drawNPC()
        if self.checkPlayerCollision():
            self.roomObj.text = self.dialogue
        else:
            self.roomObj.text = ""

    def checkPlayerCollision(self):
        if Utils.objCollision(self, self.roomObj.playerObj):
            return True

    def drawNPC(self):
        pygame.draw.rect(
            Display.DISPLAYSURF, Display.BLUE,
            pygame.Rect(self.collisionx, self.collisiony, self.width,
                        self.height))
        Display.DISPLAYSURF.blit(
            self.NPC_sprite,
            pygame.Rect(self.collisionx, self.collisiony, self.width,
                        self.height))
