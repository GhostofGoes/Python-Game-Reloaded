"""Main entrypoint to start the game."""

import sys
import logging

import pygame

import Game
import Utils



# TODO: need a name for this game...
# TODO: license


def main():
    logging.basicConfig(filename='Python-Game.log', level=logging.DEBUG)
    from time import strftime
    logging.info('Beginning of logging for run starting at %s',
                 strftime("%Y-%m-%d %H:%M:%S"))

    # TODO: cli arguments
    if len(sys.argv) > 1:
        Utils.DEBUG = int(sys.argv[1])

    # TODO: this is not properly resetting the game
    #   There is global state with enemies, rooms, and such that isn't getting reset
    # TODO: refactor this with networking in mind
    while True:
        game = Game.Game()
        _status = game.run()
        if _status == Game.RESTART_GAME:
            print("GAME OVER")
            logging.info('GAME OVER')
            Utils.printPlayerStats()
            del game
        elif _status == Game.QUIT_GAME:
            break
        else:
            break

    pygame.quit()
    logging.debug('Finished Game\n\n\n')
    # TODO: exit codes other than the implied 0


if __name__ == '__main__':
    main()
