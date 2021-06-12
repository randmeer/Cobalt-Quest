import pygame

import globals
import utils

lvl_selection_original = pygame.image.load("textures/level_selection.png")

def showLevelSelection():
    print("LEVEL SELECTION START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    # set backgrounds
    lvl_selection = pygame.transform.scale(lvl_selection_original, (500, 500))
    background = utils.background()

    clock = pygame.time.Clock()
    run = True
    # main game loop
    while run:

        clock.tick(60)
        # event looper
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True

            # code below is boilerplate code. Just make a buttonclass and check on every loop if the cursor has clicked in its hitbox.
            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    print(posX, " ", posY)
                    if 111 < posY < 189 and 26 < posX < 165:
                        run = False
                        globals.level1 = True
                    if 26 < posY < 92 and 26 < posX < 474:
                        run = False
                        globals.menu = True

            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.menu = True

        # draw window components
        window.blit(background, (0, 0))
        window.blit(lvl_selection, (0, 0))

        pygame.display.update()

    utils.playSound('click')
    print("LEVEL SELECTION END")
