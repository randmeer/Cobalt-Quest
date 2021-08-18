import pygame

import utils
from utils import globs

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

    # if music present play the music
    if utils.get_setting('background_music'):
        utils.play_music("menu")
        pygame.mixer.music.set_volume(utils.get_setting('volume') / 10)

    utils.set_global_defaults()
    utils.set_resolution()
    globs.titlescreen = True

    window = utils.setup_window()
    clock = pygame.time.Clock()

    from logic.gui import menu, title_screen, map, dungeon
    #from logic.floor import FloorTemplate

    # main game loop
    run = True
    while run:
        print(" ")
        print("MAIN LOOP ROUND START")
        clock.tick(60)

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
            #level = FloorTemplate(window=window)
            #level.start_loop()
        else:
            print("yeah so there is no current state u f**ked up")
            run = False
        print("MAIN LOOP ROUND END")

    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
