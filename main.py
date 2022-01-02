import pygame

import utils
from utils import globs
import sys

"""
How the File Sytem works:

logic: scripts chaning the state of the game
    floor: floor (ingame) logic
    gui: all user infaces and ingame overlays
    
render:  scripts displaying the state of the game
    elements: user interface elements
    sprites: ingame sprites
    camera: ingame rendering script
    gui: user interface template
    
resources: final non-script files like images, audio, json

data: variable non-script files like settings, savegames, chat

utils: useful functions
    globs: global variables
    img: globs, but with textures
    texture: texture template class

"""


if __name__ == '__main__':
    pygame.freetype.init()
    pygame.mixer.init()

    #sys.stdout = open('./data/chat.txt', 'w')
    utils.load_console()

    # if music present play the music
    if utils.get_setting('background_music'):
        utils.play_music("menu")
        pygame.mixer.music.set_volume(utils.get_setting('volume') / 10)

    utils.set_global_defaults()
    utils.set_resolution()
    globs.titlescreen = True

    window = utils.setup_window()

    from logic.gui import menu, title_screen, map, dungeon
    from logic.floor import Floor

    # main game loop
    run = True
    while run:

        # event iteration
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # game state manager
        if globs.quitgame:
            run = False
        elif globs.titlescreen:
            title_screen.show_title_screen(window=window)
        elif globs.menu:
            menu.show_menu(window=window)
        elif globs.map:
            map.show_map(window=window)
        elif globs.dungeon:
            dungeon.show_dungeon(window=window, dungeon=globs.dungeon_str)
        elif globs.floor:
            globs.floor_str = "entrance"
            floor = Floor(window=window)
            floor.load()
            floor.start_loop()
        else:
            print("yeah so there is no current state u f**ked up")
            run = False
    #sys.stdout.close()
    utils.save_console()
