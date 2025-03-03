import pygame

from octagon.utils import var, play_sound
from octagon.gui import label, button, GUI

from game import globs


def console(window, background):
    play_sound('alert')
    labels = []
    buttons = []
    labels.append(label.Label(text="> ", relpos=(0.1, 0.1), anchor="topleft", color=var.GRAYSHADES[2]))

    console_gui = GUI(background=background, overlay=200, labels=labels, buttons=buttons)
    console_gui.draw(window=window)
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pass"
                if event.key == pygame.K_RETURN:
                    return console_gui.labelgroup[0].text[2:]
                else:
                    key_str = pygame.key.name(event.key)
                    console_gui.labelgroup[0].text_input(key_str=key_str, fix_chars=2, max_chars=100)
        if globs.quitgame:
            run = False
        if run:
            console_gui.draw(window=window)
    play_sound('click')
    return "pass"
