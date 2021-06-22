import pygame

import globs
import level1
import level_selection
import menu
import rndebug
import title_screen
import utils

if __name__ == '__main__':
    # if music present play the music
    if utils.getSetting('background_music'):
        utils.playTheme()
        pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)

    print(utils.getSetting('volume'))

    utils.setGlobalDefaults()
    globs.titlescreen = True
    window = utils.setupWindow()
    clock = pygame.time.Clock()

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
            title_screen.showTitleScreen()
        elif globs.menu:
            menu.showMenu()
        elif globs.level_selection:
            level_selection.showLevelSelection()
        elif globs.level1:
            level1.playLevel1()
        elif globs.rndebug:
            rndebug.showRNDebug()
        else:
            print("yeah so there is no current state u f**ked up")

        print("CYCLED TROUGH CURRENT STATES")
        print("MAIN LOOP ROUND END")
        print(" ")

    print(" ")
    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
