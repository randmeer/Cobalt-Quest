import pygame

from utils import globs, mousepos, setGlobalDefaults, playSound
from render.elements import button
from render import gui
from utils.images import background_menu_texture

def showLevelSelection(window):
    print("LEVEL SELECTION START")
    setGlobalDefaults()

    # create the lvl buttons and use a uneccessary compicated alorithm to align them in a 3x3 grid
    # TODO: replace this shit with a real map
    levelbuttons = []
    lvlrelposy = 0.23
    for i in range(9):
        lvlrelposx = 0.05 + 0.31 * (i - ((int(i / 3)) * 3))
        if i == 3 or i == 6:
            lvlrelposy += 0.25
        levelbutton = button.Button(relwidth=0.28, relheight=0.22, textcontent=f"LVL {i}", relpos=(lvlrelposx, lvlrelposy))
        levelbuttons.append(levelbutton)

    map = gui.GUI(background=background_menu_texture, overlay=128, buttons=[
        button.Button(anchor="topleft", relwidth=0.4, relheight=0.1, textcontent="BACK TO MENU", relpos=(0.05, 0.05)),
        levelbuttons[0]
    ])

    clock = pygame.time.Clock()
    run = True
    # main game loop
    while run:
        clock.tick(60)
        mp = mousepos()
        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if map.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.menu = True
                    if map.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.menu = True
        map.draw(window=window)
        #draw()
    playSound('click')
    print("LEVEL SELECTION END")
