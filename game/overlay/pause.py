import pygame

from octagon.utils import var, mp_screen, play_sound
from octagon.gui import button, GUI, Overlay

from game import globs
from game.overlay import settings


# TODO: rework as OOP 

class Pause(Overlay):
    def __init__(self, window, background, arguments):
        super().__init__(window, background, arguments)
        self.add_button(text="Resume", relpos=(0.5, 0.35), anchor="center")
        self.add_button(text="Settings", relpos=(0.5, 0.5), anchor="center")
        self.add_button(text="Back to Menu", relpos=(0.5, 0.65), anchor="center")


def pause_screen(window, background):
    play_sound('click')

    pause_gui = GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="center", relsize=(0.4, 0.1), text="RESUME", relpos=(0.5, 0.35)),
        button.Button(anchor="center", relsize=(0.4, 0.1), text="BACK TO MENU", relpos=(0.5, 0.65)),
        button.Button(anchor="center", relsize=(0.4, 0.1), text="SETTINGS", relpos=(0.5, 0.5))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
        if globs.quitgame:
            run = False
        if run:
            pause_gui.draw(window=window)

    play_sound('click')
