import pygame

from octagon.utils import var, play_sound
from octagon.gui import label, button, GUI

from game import globs


def console(window, background):
    globs.set_global_defaults()
    play_sound('alert')
    labels = []
    buttons = []
    labels.append(label.Label(text="> ", relpos=(0.1, 0.1), anchor="topleft", color=var.GRAYSHADES[2]))

    alert_gui = GUI(background=background, overlay=200, labels=labels, buttons=buttons)
    alert_gui.draw(window=window)
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(var.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "pass"
                if event.key == pygame.K_RETURN:
                    return alert_gui.labelgroup[0].text[2:]
                else:
                    key_str = pygame.key.name(event.key)
                    alert_gui.labelgroup[0].text_input(key_str=key_str, fix_chars=2, max_chars=100)
        alert_gui.draw(window=window)
    play_sound('click')
