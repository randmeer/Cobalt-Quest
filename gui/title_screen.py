import pygame

import utils
from utils import globs
from utils import relToAbsDual
from utils.images import background_texture, title_screen_texture


def showTitleScreen():
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    background = pygame.transform.scale(background_texture, relToAbsDual(1, 1))
    title_screen = pygame.transform.scale(title_screen_texture, relToAbsDual(1.78, 1))
    rndebugAccess = 0

    window.blit(background, (0, 0))
    window.blit(background, relToAbsDual(1, 0))
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
                background = pygame.transform.scale(background_texture, (relToAbsDual(1, 1)))
                title_screen = pygame.transform.scale(title_screen_texture, relToAbsDual(1.78, 1))
                window.blit(background, (0, 0))
                window.blit(background, relToAbsDual(1, 0))
                window.blit(title_screen, (1, 0))
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