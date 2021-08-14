import pygame

import utils
from utils import globs, rndebug


if __name__ == '__main__':
    pygame.freetype.init()
    pygame.mixer.init()

    # if music present play the music
    if utils.getSetting('background_music'):
        utils.play_music("menu")
        pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)

    utils.setGlobalDefaults()
    utils.set_resolution()
    globs.titlescreen = True

    window = utils.setupWindow()
    clock = pygame.time.Clock()

    from gui import title_screen, menu, level_selection
    from gui.level import LevelTemplate

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
            title_screen.showTitleScreen(window=window)
        elif globs.menu:
            menu.showMenu(window=window)
        elif globs.level_selection:
            level_selection.showLevelSelection(window=window)
        elif globs.level1:
            level = LevelTemplate(window=window)
            level.start_loop()
        elif globs.rndebug:
            rndebug.showRNDebug()
        else:
            print("yeah so there is no current state u f**ked up")

        print("CYCLED TROUGH CURRENT STATES")
        print("MAIN LOOP ROUND END")
        print(" ")

    print(" ")
    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
