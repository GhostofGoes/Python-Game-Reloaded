""" Music and audio stuff """

import logging

from pygame.mixer import music

import Utils


class GameAudio:
    def __init__(self):
        self.volume = 1
        self.music = []
        self._logger = logging.getLogger(__name__)

    def update(self):
        pass

    def set_volume(self, volume):
        self._logger.info('Setting volume to %d', volume)
        music.set_volume(volume)
        self.volume = volume

    def load_music(self, song_path):
        self._logger.info('Loading song from %s', song_path)
        music.load(song_path)
        self.music.append(song_path)

    def play_next_song(self):
        self._logger.info('Playing next song in queue')
        if Utils.DEBUG == 2:
            return
        else:
            music.play(-1)

    def play_random_song(self):
        self._logger.info('Playing a random song')
        # TODO: implement
