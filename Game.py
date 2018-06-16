""" Main game logic. Where the magic happens. """

import pygame

# from sys import executable, argv
# from os import execl
import sys
import logging

import Display
import Player
from Input import Input
from Room import Dungeon
import Menu
import Audio
import functions

GAME_ICON = 'slithering_python.png'  # 'player_down1.png'


CONTINUE_GAME = 0
RESTART_GAME = 1
QUIT_GAME = 2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(
            pygame.transform.scale(functions.load_image(GAME_ICON), (32, 32)))
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

        # Finishing up
        # print("GAME OVER")
        # self._log.info('GAME OVER')
        # functions.printPlayerStats()
        # self.restart()

    # def restart(self):
    #     self._log.debug('restart')
    #     execl(
    #         executable, executable, *argv
    #     )  # TODO: do this properly, otherwise it will crash and burn badly

    def runGame(self):
        self.playerObj = Player.Player()
        dungeonObj = Dungeon(self.playerObj, 10)
        menuObject = Menu.Menu(self.playerObj, dungeonObj)
        self.playerObj.dungeonObj = dungeonObj  # temporary, need a better way to pass dungeon info to playerobj
        dungeonObj.playerObj = self.playerObj  #This line and the last are hella confusing....
        dungeonObj.menuObject = menuObject
        self._log.debug('Finished initializations for runGame')

        while True:
            if functions.paused:
                functions.pauseMenu()
                functions.paused = False
            if functions.gameTimer == 30:
                functions.gameTimer = 0
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

            functions.updateItems(self.playerObj)
            functions.updateCoins(self.playerObj)

            if self.playerObj.isDead:
                self._log.info('Player %s is dead', self.playerObj.name)
                return RESTART_GAME

            pygame.display.update()
            Display.FPSCLOCK.tick(Display.FPS)
            functions.gameTimer += 1


if __name__ == '__main__':
    """ For non-networked gameplay """
    logging.basicConfig(filename='Python-Game.log', level=logging.DEBUG)
    from time import strftime
    logging.info('Beginning of logging for run starting at %s',
                 strftime("%Y-%m-%d %H:%M:%S"))

    # TODO: cli arguments
    if len(sys.argv) > 1:
        functions.DEBUG = int(sys.argv[1])

    # TODO: this is not properly resetting the game
    #   There is global state with enemies, rooms, and such that isn't getting reset
    while True:
        game = Game()
        _status = game.run()
        if _status == RESTART_GAME:
            print("GAME OVER")
            logging.info('GAME OVER')
            functions.printPlayerStats()
            del game
        elif _status == QUIT_GAME:
            break
        else:
            break

    pygame.quit()
    logging.debug('Finished Game\n\n\n')
    # TODO: exit codes other than the implied 0
