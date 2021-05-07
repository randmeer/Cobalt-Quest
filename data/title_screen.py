import pygame
from data import utils
from data import globals


def showTitleScreen():
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    title_screen_original = pygame.image.load("data/textures/title_screen.png")
    title_screen = pygame.transform.scale(title_screen_original, (500, 500))
    background = utils.background()
    rndebugAccess = 0

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                globals.menu = True
                run = False
            if event.type == pygame.KEYDOWN:
                #print(event.key)
                if event.key == globals.ESCAPE:
                    None
                elif event.key == globals.KEY_R:
                    run = True
                # the following elifs let the user CMD-Q (mac) or ALT-F4 (windows)
                elif event.key == globals.COMMAND:
                    run = True
                elif event.key == globals.KEY_Q:
                    run = True
                elif event.key == globals.ALT:
                    run = True
                elif event.key == globals.KEY_F4:
                    run = True
                else:
                    globals.menu = True
                    run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rndebugAccess = rndebugAccess + 1
        if not keys[pygame.K_r]:
            rndebugAccess = 0

        if rndebugAccess == 150:
            print("ACCESS GRANTED")
            #rndebug.showRNDebug()
            globals.rndebug = True
            run = False

        window.blit(background, (0, 0))
        window.blit(title_screen, (0, 0))

        pygame.display.update()

    utils.playSound('click')
    print("TITLE SCREEN END")
