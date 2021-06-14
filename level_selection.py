import pygame
import utils
import globals
from sprites import button
from utils import relToAbsDual

background_original = pygame.image.load("textures/background.png")
lvl_selection_original = pygame.image.load("textures/level_selection.png")

def showLevelSelection():
    print("LEVEL SELECTION START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    lvl_selection = pygame.transform.scale(lvl_selection_original, (globals.windowsize, globals.windowsize))
    background = pygame.transform.scale(background_original, (globals.windowsize, globals.windowsize))

    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.05))
    buttongroup.add(backtomenu_button)

    # create the lvl buttons and use a uneccessary compicated alorithm to align them in a 3x3 grid
    levelbuttons = []
    lvlrelposy = 0.23
    for i in range(9):
        lvlrelposx = 0.05 + 0.31 * (i - ((int(i / 3))*3))
        if i == 3 or i == 6:
            lvlrelposy += 0.25
        levelbutton = button.Button(relwidth=0.28, relheight=0.22, textcontent=f"lvl {i}", relpos=(lvlrelposx, lvlrelposy))
        levelbuttons.append(levelbutton)
    for i in levelbuttons:
        buttongroup.add(i)

    # draw window
    window.blit(background, (0, 0))
    window.blit(lvl_selection, (0, 0))
    for i in buttongroup:
        i.update()
        i.draw(window=window)
    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()

        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True

            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globals.menu = True
                    if levelbuttons[0].rect.collidepoint(mousepos):
                        run = False
                        globals.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.menu = True

            if event.type == pygame.VIDEORESIZE:
                w, h = pygame.display.get_surface().get_size()
                if w < 500 or h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((h, h), pygame.RESIZABLE)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                lvl_selection = pygame.transform.scale(lvl_selection_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(lvl_selection, (0, 0))
                for i in buttongroup:
                    i.update()
                    i.draw(window=window)
                pygame.display.update()
                globals.windowsize = h

    utils.playSound('click')
    print("LEVEL SELECTION END")
