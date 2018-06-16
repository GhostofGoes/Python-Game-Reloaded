""" Main game logic. Where the magic happens. """

import logging

import pygame

import Display
import Player
from Input import Input
from Room import Dungeon
import Menu
import Audio
import Utils

GAME_ICON = 'slithering_python.png'

CONTINUE_GAME = 0
RESTART_GAME = 1
QUIT_GAME = 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(
            pygame.transform.scale(Utils.load_image(GAME_ICON), (32, 32)))
        pygame.display.set_caption('Python-Game')
        self.playerObj = Player.Player()
        self.audioObj = Audio.GameAudio()
        self.inputObj = Input()
        self._log = logging.getLogger(__name__)
        self._log.debug('Initialized Game')

    def run(self):

        # Initialize Input and Audio
        self.inputObj.initialize_controllers()
        self.audioObj.load_music('music\Damnation.mp3')
        self.audioObj.play_next_song()
        # Run the game
        game_status = CONTINUE_GAME
        while game_status == CONTINUE_GAME:
            game_status = self.runGame()
        return game_status

    def runGame(self):
        self.playerObj = Player.Player()
        dungeonObj = Dungeon(self.playerObj, 10)
        menuObject = Menu.Menu(self.playerObj, dungeonObj)
        # TODO: temporary, need a better way to pass dungeon info to playerobj
        self.playerObj.dungeonObj = dungeonObj
        dungeonObj.playerObj = self.playerObj  # TODO: This line and the last are hella confusing....
        dungeonObj.menuObject = menuObject
        self._log.debug('Finished initializations for runGame')

        while True:
            if Utils.paused:
                Utils.pauseMenu()
                Utils.paused = False
            if Utils.gameTimer == 30:
                Utils.gameTimer = 0
                if self.playerObj.arrows < 10:
                    self.playerObj.arrows += 1
                    print("Magic quiver produced one arrow")
            self.inputObj.update(self.playerObj, menuObject)
            if self.inputObj.quit_requested:
                return QUIT_GAME
            elif self.inputObj.restart_requested:
                return RESTART_GAME

            dungeonObj.update()
            menuObject.update()
            self.playerObj.update()
            self.playerObj.rangedWeapon.update(self.playerObj)
            self.playerObj.updateColliders()
            self.audioObj.update()
            pygame.mouse.set_visible(False)

            if dungeonObj.returnCurrentRoom().hasSpawners:
                for spawnner in dungeonObj.returnCurrentRoom().spawnnerlist:
                    spawnner.drawSpawnner()
                    spawnner.update()
                    if spawnner.isDead:
                        dungeonObj.returnCurrentRoom().spawnnerlist.remove(
                            spawnner)
            if dungeonObj.returnCurrentRoom().hasSpawners:
                for enemy in dungeonObj.returnCurrentRoom().enemylist:
                    enemy.update()

            Utils.updateItems(self.playerObj)
            Utils.updateCoins(self.playerObj)

            if self.playerObj.isDead:
                self._log.info('Player %s is dead', self.playerObj.name)
                return RESTART_GAME

            pygame.display.update()
            Display.FPSCLOCK.tick(Display.FPS)
            Utils.gameTimer += 1
