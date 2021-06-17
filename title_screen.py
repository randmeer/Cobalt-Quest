import pygame
import utils
import globs
import globs
from utils import relToAbsDual

background_original = pygame.image.load("textures/background.png")
title_screen_original = pygame.image.load("textures/title_screen.png")

def showTitleScreen():
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    background = pygame.transform.scale(background_original, (globs.height, globs.height))
    title_screen = pygame.transform.scale(title_screen_original, (globs.width, globs.height))
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
                globs.quitgame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                globs.menu = True
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == globs.KEY_R:
                    pass
                elif event.key == pygame.K_ESCAPE:
                    pass
                # the following elif's let the user CMD-Q (macOS) or ALT-F4 (windows)
                elif event.key == globs.COMMAND:
                    pass
                elif event.key == globs.KEY_Q:
                    pass
                elif event.key == globs.ALT:
                    pass
                elif event.key == globs.KEY_F4:
                    pass
                else:
                    globs.menu = True
                    run = False
            if event.type == pygame.VIDEORESIZE:
                utils.resizeWindow(event.w, event.h)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                title_screen = pygame.transform.scale(title_screen_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(title_screen, (0, 0))
                pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rndebugAccess = rndebugAccess + 1
        if not keys[pygame.K_r]:
            rndebugAccess = 0

        if rndebugAccess == 150:
            print("ACCESS GRANTED")
            globs.rndebug = True
            run = False

    utils.playSound('click')
    print("TITLE SCREEN END")
