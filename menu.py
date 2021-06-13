import pygame
import utils
import globals
from sprites import button
from utils import relToAbsDual

menu_original = pygame.image.load("textures/menu.png")
ez_original = pygame.image.load("textures/menu_mode_1.png")
notez_original = pygame.image.load("textures/menu_mode_2.png")
rip_original = pygame.image.load("textures/menu_mode_3.png")
background_original = pygame.image.load("textures/background.png")

def showMenu():
    print("MENU START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    background = pygame.transform.scale(background_original, (500, 500))
    menu = pygame.transform.scale(menu_original, (500, 500))
    ez = pygame.transform.scale(ez_original, (140, 190))
    notez = pygame.transform.scale(notez_original, (140, 190))
    rip = pygame.transform.scale(rip_original, (140, 190))
    buttongroup = pygame.sprite.Group()
    levelselection_button = button.Button(relwidth=0.9, relheight=0.135, textcontent="level selection", relpos=(0.05, 0.41))
    buttongroup.add(levelselection_button)

    # TODO: find easier way to get clicks on the difficulty button
    difficultyrect = ez.get_rect()
    difficultyrect.x = 26
    difficultyrect.y = 287

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(60)

        mousepos = pygame.mouse.get_pos()

        # event looper
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True

            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left button event
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    # print(posX, " ", posY)
                    if levelselection_button.rect.collidepoint(mousepos):
                        run = False
                        globals.level_selection = True
                    if difficultyrect.collidepoint(mousepos):
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
            # resize event
            if event.type == pygame.VIDEORESIZE:
                w, h = pygame.display.get_surface().get_size()
                if w < 500 or h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((h, h), pygame.RESIZABLE)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                for i in buttongroup:
                    i.resize()


        # draw window
        window.blit(background, (0, 0))
        window.blit(menu, (0, 0))
        #buttongroup.draw(window)
        levelselection_button.draw(window=window)

        if globals.difficulty == 1:
            window.blit(ez, (26, 287))
        elif globals.difficulty == 2:
            window.blit(notez, (26, 287))
        elif globals.difficulty == 3:
            window.blit(rip, (26, 287))

        pygame.display.update()

    utils.playSound('click')
    print("MENU END")
