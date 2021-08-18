import pygame

from utils import globs, mousepos, set_global_defaults, play_sound
from render.elements import button, image, label
from render import gui
from utils.images import bg_gui_tx, logo_tx
from logic.gui.overlay import show_settings


def show_menu(window):
    print("    MENU START")
    set_global_defaults()

    menu_gui = gui.GUI(
        background=bg_gui_tx, overlay=128,
        buttons=[
            button.Button(anchor="topleft", relwidth=0.264, relheight=0.1, text="MAP", relpos=(0.225, 0.40)),
            button.Button(anchor="topright", relwidth=0.264, relheight=0.1, text="SHOP", relpos=(0.775, 0.40)),
            button.Button(anchor="topleft", relwidth=0.413, relheight=0.1, text="INVENTORY", relpos=(0.225, 0.525)),
            button.Button(anchor="topright", relwidth=0.116, relheight=0.1, text="?", relpos=(0.775, 0.525)),
            button.Button(anchor="topleft", relwidth=0.413, relheight=0.1, text="SETTINGS", relpos=(0.225, 0.65)),
            button.Button(anchor="topright", relwidth=0.116, relheight=0.1, text="?", relpos=(0.775, 0.65))],
        images=[
            image.Image(relpos=(0.5, 0.2), anchor="center", image=logo_tx)],
        labels=[
            label.Label(text=f"VERSION {globs.VERSION}", relpos=(0.01, 0.98), anchor="bottomleft", color=(12, 18, 26)),
            label.Label(text="RANDE STUDIOS", relpos=(0.01, 0.94), anchor="bottomleft", color=(12, 18, 26))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        if globs.quitgame:
            run = False
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if menu_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.map = True
                    if menu_gui.buttongroup[4].rect.collidepoint(mp):
                        show_settings(window=window, background=bg_gui_tx)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.titlescreen = True
        menu_gui.draw(window=window)
    play_sound('click')
    print("MENU END")
