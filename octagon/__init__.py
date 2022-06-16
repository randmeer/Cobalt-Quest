import pygame

from octagon.utils import load_console, get_setting, play_music, set_resolution, var


def init():
    pygame.freetype.init()
    pygame.mixer.init()
    pygame.display.init()

    # sys.stdout = open('./data/chat.txt', 'w')
    utils.load_console()

    # if music present play the music
    if utils.get_setting('background_music'):
        utils.play_music("menu")
        pygame.mixer.music.set_volume(utils.get_setting('volume') / 10)

    utils.set_resolution()


def window(title):
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load('./resources/textures/icon.png'))
    if var.fullscreen:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(var.res_size)


def quit():
    # sys.stdout.close()
    utils.save_console()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
