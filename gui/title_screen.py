import pygame

import utils
from utils import globs
from utils.images import background_texture, logo_texture


def showTitleScreen():
    print("TITLE SCREEN START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()
    rndebugAccess = 0

    def draw():
        og_surface = pygame.Surface(globs.SIZE)
        og_surface.blit(background_texture, (0, 0))
        og_surface.blit(logo_texture, (og_surface.get_width()/2-logo_texture.get_width()/2, og_surface.get_height()/2-logo_texture.get_height()/2))
        surface = pygame.transform.scale(og_surface, globs.res_size)
        window.blit(surface, (0, 0))
        pygame.display.update()
    draw()

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
