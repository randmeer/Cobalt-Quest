import pygame, threading
from data import utils, globals, title_screen, menu, level_selection, level1

# def updateMusic():
#    pygame.mixer.init()
#
#    test = utils.getSetting('background_music')
#    while True:
#        if test != utils.getSetting('background_music'):
#            pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)
#        test = utils.getSetting('background_music')
#
#
# musicthread = threading.Thread(target=updateMusic, daemon=True)
#
# if utils.getSetting('background_music') == "true":
#    utils.playTheme()
#    pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)
#    musicthread.start()

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

    run = True
    # main game loop
    while run:
        print(" ")
        print("MAIN LOOP ROUND START")
        clock.tick(60)

        # go through every pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # game state manager
        if globals.quitgame:
            run = False
            print("DETECTED ORDER TO QUIT GAME")

        else:
            if globals.titlescreen:
                title_screen.showTitleScreen()
            elif globals.menu:
                menu.showMenu()
            elif globals.level_selection:
                level_selection.showLevelSelection()
            elif globals.level1:
                level1.playLevel1()
            else:
                print("yeah so there is no current state u f**ked up")
            print("CYCLED TROUGH CURRENT STATES")

        print("MAIN LOOP ROUND END")
        print(" ")

    print(" ")
    print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
