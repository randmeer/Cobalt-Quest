import pygame

from octagon.state import State
from octagon.utils import load_console, save_console, load_settings, get_setting, play_music, set_resolution, var


def init():
    pygame.freetype.init()
    pygame.mixer.init()
    pygame.display.init()

    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION])

    # sys.stdout = open('./data/chat.txt', 'w')
    load_console()
    load_settings()
    set_resolution()

    # if music present play the music
    if get_setting('background_music'):
        play_music("menu")
        pygame.mixer.music.set_volume(get_setting('volume') / 10)


def window(title: str):
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load('./resources/textures/icon.png'))
    if var.fullscreen:

        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(var.res_size)


def run(window: pygame.Surface, states: dict[str, type[State]], start: str) -> None:
    """state handler"""

    if "quit" in states or any([key.startswith("back") for key in states]):
        raise Exception("'quit' and 'back' are reserved gamestates and will not be registered")

    queue = [start]

    while True:
        if queue[-1].startswith("back"):
            amount = queue[-1][4:]
            if amount == "":
                intamount = 1
            else:
                intamount = int(amount)
            queue = queue[:-2]
        state = queue[-1]

        print(queue)

        if state == "quit":
            break

        try:
            state_obj = states[state](window=window)
            print(type(state_obj))
            queue.append(state_obj._execute())
        except KeyError:
            raise Exception("No valid gamestate returned")


def quit():
    # sys.stdout.close()
    save_console()
