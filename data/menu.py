import pygame
from data import utils
from data import globals


def showMenu():
    print("MENU START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    menu_original = pygame.image.load("data/textures/menu.png")
    menu = pygame.transform.scale(menu_original, (500, 500))
    ez_original = pygame.image.load("data/textures/menu_mode_1.png")
    notez_original = pygame.image.load("data/textures/menu_mode_2.png")
    rip_original = pygame.image.load("data/textures/menu_mode_3.png")
    ez = pygame.transform.scale(ez_original, (140, 190))
    notez = pygame.transform.scale(notez_original, (140, 190))
    rip = pygame.transform.scale(rip_original, (140, 190))

    background = utils.background()

    clock = pygame.time.Clock()
    run = True
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
                # left button event
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    print(posX, " ", posY)
                    if 207 < posY < 272 and 26 < posX < 475:
                        run = False
                        globals.level_selection = True
                    if 287 < posY < 476 and 26 < posX < 165:
                        if not globals.difficulty >= 3:
                            globals.difficulty = globals.difficulty + 1
                        else:
                            globals.difficulty = 1
                        utils.playSound('click')
            # quit event
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.titlescreen = True

        # draw window
        window.blit(background, (0, 0))
        window.blit(menu, (0, 0))

        if globals.difficulty == 1:
            window.blit(ez, (26, 287))
        elif globals.difficulty == 2:
            window.blit(notez, (26, 287))
        elif globals.difficulty == 3:
            window.blit(rip, (26, 287))

        pygame.display.update()

    utils.playSound('click')
    print("MENU END")
