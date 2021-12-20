import pygame

import utils
from utils import globs
import sys
"""
How the File Sytem works:

The logic folder contains scripts chaning the state of the game.
The render folder contains scripts displaying the state of the game.
The utils folder contains useful functions used by multiple scripts in different folders.
The resources folder contains non-script files and read by logic scripts.
The data folder contains non-script files and is read and written by scripts.
main.py is the script initializing and supervising all the action
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
        print(" ")
        print("MAIN LOOP ROUND START")

        # event iteration
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # game state manager
        if globs.quitgame:
            run = False
            print("DETECTED ORDER TO QUIT GAME")
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
        print("MAIN LOOP ROUND END")
    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
    #sys.stdout.close()
    utils.save_console()
