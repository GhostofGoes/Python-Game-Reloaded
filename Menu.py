import pygame
import logging

import Display
from functions import load_image


class Menu:
    #info bar stuff
    infobar_sprite = load_image('infobar.png')
    full_heart_sprite = load_image('100_heart.png')
    threequarters_heart_sprite = load_image('75_heart.png')
    half_heart_sprite = load_image('50_heart.png')
    onequarter_heart_sprite = load_image('25_heart.png')

    # weapons
    axe_sprite = load_image('axe.png')

    # Dialogue
    dialogue_sprite = load_image('dialoguebox.png')

    def __init__(self, playerObj, dungeonObj):
        self.dialogue = ""
        self.playerObj = playerObj
        self.dungeonObj = dungeonObj
        self.showText = False
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Menu Initialized')

    def update(self):
        self.drawMenu()
        self.drawHearts()
        self.drawMap()
        if self.dialogue != "":
            self.logger.debug('Displaying dialogue: %s', self.dialogue)
            self.displayDialogue()

    def activateText(self):
        self.showText = True
        self.logger.debug('Activating menu')

    def displayDialogue(self):
        pygame.draw.rect(
            Display.DISPLAYSURF, Display.RED,
            pygame.Rect(0, Display.DIALOGUE_BOX_START, Display.SCREEN_WIDTH,
                        Display.GAME_SCREEN_START))
        Display.DISPLAYSURF.blit(
            self.dialogue_sprite,
            pygame.Rect(0, Display.DIALOGUE_BOX_START, Display.SCREEN_WIDTH,
                        Display.GAME_SCREEN_START))

        myfont = pygame.font.SysFont("monospace", 15)
        for x in range(0, len(self.dialogue), 61):
            text = myfont.render(self.dialogue[x:x + 61], 1, Display.WHITE)
            Display.DISPLAYSURF.blit(
                text, (15, Display.DIALOGUE_BOX_START + 10 + 15 * x / 61))

    def drawMenu(self):
        Display.DISPLAYSURF.blit(
            self.infobar_sprite,
            pygame.Rect(0, 0, Display.SCREEN_WIDTH, Display.GAME_SCREEN_START))
        self.drawHearts()
        Display.DISPLAYSURF.blit(
            self.axe_sprite,
            pygame.Rect(280, 18, Display.TILE_SIZE, Display.TILE_SIZE))

        myfont = pygame.font.SysFont("monospace", 15)
        scoretext = myfont.render("Score = " + str(self.playerObj.score), 1,
                                  Display.RED)
        roomtext = myfont.render(
            "Room = " + str(self.dungeonObj.currRoomIndex), 1, Display.RED)
        healthtext = myfont.render("Health =" + str(self.playerObj.health), 1,
                                   Display.RED)

        Display.DISPLAYSURF.blit(scoretext, (450, 10))
        Display.DISPLAYSURF.blit(roomtext, (450, 20))
        Display.DISPLAYSURF.blit(healthtext, (450, 30))

    def drawMap(self):
        currentRoom = self.dungeonObj.returnCurrentRoom()
        for room in self.dungeonObj.returnListRooms():
            if room == currentRoom:
                pygame.draw.rect(Display.DISPLAYSURF, Display.YELLOW,
                                 (380 + room.x * 8, 40 + room.y * 8, 6, 6))
            else:
                pygame.draw.rect(Display.DISPLAYSURF, Display.RED,
                                 (380 + room.x * 8, 40 + room.y * 8, 6, 6))

    def drawHearts(self):
        healthBits = self.playerObj.health
        x = 0
        y = 5
        while healthBits > 0:
            if healthBits >= 4:
                Display.DISPLAYSURF.blit(self.full_heart_sprite,
                                         pygame.Rect(x * 29 + 5, y, 29, 24))
            elif healthBits == 3:
                Display.DISPLAYSURF.blit(self.threequarters_heart_sprite,
                                         pygame.Rect(x * 29 + 5, y, 29, 24))
            elif healthBits == 2:
                Display.DISPLAYSURF.blit(self.half_heart_sprite,
                                         pygame.Rect(x * 29 + 5, y, 29, 24))
            elif healthBits == 1:
                Display.DISPLAYSURF.blit(self.onequarter_heart_sprite,
                                         pygame.Rect(x * 29 + 5, y, 29, 24))
            else:
                return
            x += 1
            healthBits -= 4
