import pygame
import globs
import utils
import globs
from sprites import button
from utils import relToAbsDual

background_original = pygame.image.load("textures/background.png")
lvl_selection_original = pygame.image.load("textures/level_selection.png")

def showLevelSelection():
    print("LEVEL SELECTION START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    lvl_selection = pygame.transform.scale(lvl_selection_original, (globs.height, globs.height))
    background = pygame.transform.scale(background_original, (globs.height, globs.height))

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
    window.blit(background, relToAbsDual(1, 0))
    window.blit(lvl_selection, (0, 0))
    for i in buttongroup:
        i.update()
        i.draw(window=window)
    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    # main game loop
    while run:

        clock.tick(60)
        mousepos = pygame.mouse.get_pos()

        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True

            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globs.menu = True
                    if levelbuttons[0].rect.collidepoint(mousepos):
                        run = False
                        globs.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == globs.ESCAPE:
                    run = False
                    globs.menu = True

            if event.type == pygame.VIDEORESIZE:
                utils.resizeWindow(event.w, event.h)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                lvl_selection = pygame.transform.scale(lvl_selection_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(background, relToAbsDual(1, 0))
                window.blit(lvl_selection, (0, 0))
                for i in buttongroup:
                    i.update()
                    i.draw(window=window)
                pygame.display.update()

    utils.playSound('click')
    print("LEVEL SELECTION END")
