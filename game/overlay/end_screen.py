import pygame

from octagon.utils import mp_screen, img, var, play_sound
from octagon.gui import button, image
from octagon import gui

from game import globs

victory = pygame.transform.scale(img.misc["overlay"]["victory"], var.SIZE)
defeat = pygame.transform.scale(img.misc["overlay"]["defeat"], var.SIZE)


def end_screen(window, background, end):
    # TODO: end screen textures
    globs.set_global_defaults()
    images = []
    if end == "victory":
        play_sound('victory')
        images.append(image.Image(image=img.misc["overlay"]["victory"], anchor="center", relpos=(0.5, 0.25)))
    if end == "defeat":
        play_sound('defeat')
        images.append(image.Image(image=img.misc["overlay"]["defeat"], anchor="center", relpos=(0.5, 0.25)))
    end_gui = gui.GUI(background=background, overlay=128, images=images, buttons=[
        button.Button(relsize=(0.413, 0.1), anchor="midtop", text="Back to Menu", relpos=(0.5, 0.525)),
        button.Button(relsize=(0.413, 0.1), anchor="midtop", text="Replay", relpos=(0.5, 0.65))])

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
                    if end_gui.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    if end_gui.buttongroup[1].rect.collidepoint(mp):
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.exittomenu = True
        end_gui.draw(window=window)
    play_sound('click')
