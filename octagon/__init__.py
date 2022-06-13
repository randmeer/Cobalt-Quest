import pygame

from octagon.utils import load_console, save_console, load_settings, get_setting, play_music, set_resolution, var


def init():
    pygame.freetype.init()
    pygame.mixer.init()
    pygame.display.init()

    # sys.stdout = open('./data/chat.txt', 'w')
    load_console()
    load_settings()
    set_resolution()

    # if music present play the music
    if get_setting('background_music'):
        play_music("menu")
        pygame.mixer.music.set_volume(get_setting('volume') / 10)


def window(title):
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load('./resources/textures/icon.png'))
    if var.fullscreen:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(var.res_size)


def quit():
    # sys.stdout.close()
    save_console()
