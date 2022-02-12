import pygame
from octagon.utils import load_console, get_setting, play_music, set_global_defaults, set_resolution
import globs


def init():
    pygame.freetype.init()
    pygame.mixer.init()

    # sys.stdout = open('./data/chat.txt', 'w')
    utils.load_console()

    # if music present play the music
    if utils.get_setting('background_music'):
        utils.play_music("menu")
        pygame.mixer.music.set_volume(utils.get_setting('volume') / 10)

    utils.set_global_defaults()
    utils.set_resolution()
    globs.titlescreen = True


def window():
    window = utils.setup_window()
    return window


def quit():
    # sys.stdout.close()
    utils.save_console()
