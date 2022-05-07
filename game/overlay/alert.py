import pygame

from octagon.utils import var, mp_screen, play_sound
from octagon.gui import label, button, GUI

from game import globs


def alert(window, background, message, color=(0, 0, 0), question=False, question_keyword="OK"):
    globs.set_global_defaults()
    play_sound('alert')
    labels = []
    buttons = []
    for i in range(len(message)):
        labels.append(label.Label(text=message[i], relpos=(0.5, 0.1*i+0.5-0.1*len(message)), anchor="center"))

    if question:
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text=question_keyword, relpos=(0.35, 0.6)))
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.65, 0.6)))
    else:
        buttons.append(button.Button(anchor="center", relsize=(0.1, 0.1), text="OK", relpos=(0.5, 0.6)))

    alert_gui = GUI(background=background, overlay=200, labels=labels, overlaycolor=color, buttons=buttons)
    alert_gui.draw(window=window)
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    if alert_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        if question:
                            play_sound('click')
                            return True
                    if question:
                        if alert_gui.buttongroup[1].rect.collidepoint(mp):
                            play_sound('click')
                            return False
        alert_gui.draw(window=window)
    play_sound('click')
