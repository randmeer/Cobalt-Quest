import pygame

from utils import globs, __init__, mousepos
from render.sprites import button
from utils.images import background_texture
from utils.__init__ import relToAbsDualHeight

def showLevelSelection():
    print("LEVEL SELECTION START")
    __init__.setGlobalDefaults()
    window = __init__.setupWindow()

    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.05))
    buttongroup.add(backtomenu_button)
    # create the lvl buttons and use a uneccessary compicated alorithm to align them in a 3x3 grid
    levelbuttons = []
    lvlrelposy = 0.23
    for i in range(9):
        lvlrelposx = 0.05 + 0.31 * (i - ((int(i / 3)) * 3))
        if i == 3 or i == 6:
            lvlrelposy += 0.25
        levelbutton = button.Button(relwidth=0.28, relheight=0.22, textcontent=f"lvl {i}", relpos=(lvlrelposx, lvlrelposy))
        levelbuttons.append(levelbutton)
    for i in levelbuttons:
        buttongroup.add(i)

    def draw():
        og_surface = pygame.Surface(globs.SIZE)
        og_surface.fill((0, 0, 0))
        og_surface.blit(background_texture, (0, 0))
        for i in buttongroup:
            i.update()
            i.draw(window=og_surface)
        surface = pygame.transform.scale(og_surface, globs.res_size)
        window.blit(surface, (0, 0))
        pygame.display.update()
    draw()

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
                    if backtomenu_button.rect.collidepoint(mp):
                        run = False
                        globs.menu = True
                    if levelbuttons[0].rect.collidepoint(mp):
                        run = False
                        globs.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.menu = True
            #if event.type == pygame.VIDEORESIZE:
            #    resize()
        draw()
    __init__.playSound('click')
    print("LEVEL SELECTION END")
