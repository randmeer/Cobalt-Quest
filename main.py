import pygame
import rndebug
import utils
import level_selection
import level1
import title_screen
import menu
import globals

if __name__ == '__main__':
    # if music present play the music
    if utils.getSetting('background_music'):
        utils.playTheme()
        pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)

    print(utils.getSetting('volume'))

    utils.setGlobalDefaults()
    globals.titlescreen = True
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
        if globals.quitgame:
            run = False
            print("DETECTED ORDER TO QUIT GAME")
        elif globals.titlescreen:
            title_screen.showTitleScreen()
        elif globals.menu:
            menu.showMenu()
        elif globals.level_selection:
            level_selection.showLevelSelection()
        elif globals.level1:
            level1.playLevel1()
        elif globals.rndebug:
            rndebug.showRNDebug()
        else:
            print("yeah so there is no current state u f**ked up")

        print("CYCLED TROUGH CURRENT STATES")
        print("MAIN LOOP ROUND END")
        print(" ")

    print(" ")
    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
