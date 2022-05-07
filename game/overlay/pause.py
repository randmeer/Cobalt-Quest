import pygame

from octagon.utils import var, mp_screen, play_sound
from octagon.gui import button, GUI

from game import globs
from game.overlay.settings import show_settings


def pause_screen(window, background):
    play_sound('click')
    globs.set_global_defaults()

    pause_gui = GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="center", relsize=(0.4, 0.1), text="RESUME", relpos=(0.5, 0.44)),
        button.Button(anchor="center", relsize=(0.4, 0.1), text="BAck TO MENU", relpos=(0.5, 0.62)),
        button.Button(anchor="bottomright", relsize=(0.4, 0.1), text="SETTINGS", relpos=(0.95, 0.95))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    if pause_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                    if pause_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    if pause_gui.buttongroup[2].rect.collidepoint(mp):
                        show_settings(window=window, background=background)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pause_gui.draw(window=window)
        if globs.exittomenu:
            run = False
    play_sound('click')
