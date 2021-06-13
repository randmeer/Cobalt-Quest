import pygame
import utils
import globals
from utils import relToAbsDual

background_original = pygame.image.load("textures/background.png")
title_screen_original = pygame.image.load("textures/title_screen.png")

def showTitleScreen():
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    background = pygame.transform.scale(background_original, (globals.windowsize, globals.windowsize))
    title_screen = pygame.transform.scale(title_screen_original, (globals.windowsize, globals.windowsize))
    rndebugAccess = 0

    window.blit(background, (0, 0))
    window.blit(title_screen, (0, 0))
    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    while run:

        clock.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                globals.menu = True
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    None
                elif event.key == globals.KEY_R:
                    run = True
                # the following elifs let the user CMD-Q (mac) or ALT-F4 (windows)
                elif event.key == globals.COMMAND:
                    run = True
                elif event.key == globals.KEY_Q:
                    run = True
                elif event.key == globals.ALT:
                    run = True
                elif event.key == globals.KEY_F4:
                    run = True
                else:
                    globals.menu = True
                    run = False

            if event.type == pygame.VIDEORESIZE:
                w, h = pygame.display.get_surface().get_size()
                if w < 500 or h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((h, h), pygame.RESIZABLE)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                title_screen = pygame.transform.scale(title_screen_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(title_screen, (0, 0))
                pygame.display.update()
                globals.windowsize = h

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rndebugAccess = rndebugAccess + 1
        if not keys[pygame.K_r]:
            rndebugAccess = 0

        if rndebugAccess == 150:
            print("ACCESS GRANTED")
            globals.rndebug = True
            run = False

    utils.playSound('click')
    print("TITLE SCREEN END")
