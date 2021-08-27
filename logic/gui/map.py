import pygame

from utils import globs, mp_screen, set_global_defaults, play_sound
from render.elements import button
from render import gui
from utils.images import bg_tx

def show_map(window):
    print("    LEVEL SELECTION START")
    set_global_defaults()

    # TODO: replace this shit with a real map
    # create the lvl buttons and use a uneccessary compicated alorithm to align them in a 3x3 grid
    levelbuttons = []
    lvlrelposy = 0.23
    for i in range(9):
        lvlrelposx = 0.05 + 0.31 * (i - ((int(i / 3)) * 3))
        if i == 3 or i == 6:
            lvlrelposy += 0.25
        levelbutton = button.Button(relsize=(0.28, 0.22), text=f"LVL {i}", relpos=(lvlrelposx, lvlrelposy))
        levelbuttons.append(levelbutton)

    map_gui = gui.GUI(background=bg_tx, overlay=128, buttons=[
        button.Button(anchor="topleft", relsize=(0.4, 0.1), text="BACK TO MENU", relpos=(0.05, 0.05)), levelbuttons[0]])

    clock = pygame.time.Clock()
    run = True
    # main game loop
    while run:
        clock.tick(60)
        mp = mp_screen()
        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if map_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.menu = True
                    if map_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.dungeon = True
                        globs.dungeon_str = "northern_plains"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.menu = True
        map_gui.draw(window=window)
    play_sound('click')
    print("LEVEL SELECTION END")
