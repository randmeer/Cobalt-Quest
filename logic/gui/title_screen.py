import pygame

from utils import globs, img, set_global_defaults, play_sound
from render import gui
from render.elements import label


def show_title_screen(window):
    set_global_defaults()

    title_screen_gui = gui.GUI(
        background=img.misc["background"]["menu"], overlay=192,
        labels=[
            label.Label(text="PRESS ANY KEY TO START", relpos=(0.5, 0.5), anchor="center", color=(255, 255, 255))])
    title_screen_gui.draw(window=window)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                globs.menu = True
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                    pass
                # the following statement lets the user use the CMD-Q (macOS) or ALT-F4 (windows) -shortcut.
                elif event.key == globs.COMMAND or event.key == pygame.K_q or event.key == globs.ALT or event.key == globs.KEY_F4:
                    pass
                else:
                    globs.menu = True
                    run = False
    play_sound('click')
