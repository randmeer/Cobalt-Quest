import pygame

from utils import globs, playSound, setGlobalDefaults, rta_dual, mousepos
from utils.images import overlay_texture, victory_texture, defeat_texture
from render.elements import button
from render import gui


def pause_screen(window, background):
    playSound('click')
    setGlobalDefaults()

    pause = gui.GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="center", relwidth=0.4, relheight=0.1, textcontent="RESUME", relpos=(0.5, 0.44)),
        button.Button(anchor="center", relwidth=0.4, relheight=0.1, textcontent="BAck TO MENU", relpos=(0.5, 0.62)),
        button.Button(anchor="bottomright", relwidth=0.4, relheight=0.1, textcontent="SETTINGS", relpos=(0.95, 0.95))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if pause.buttongroup[0].rect.collidepoint(mp):
                        run = False
                    if pause.buttongroup[1].rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    if pause.buttongroup[2].rect.collidepoint(mp):
                        settings(window=window, background=background)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        pause.draw(window=window)
        if globs.exittomenu:
            run = False
    playSound('click')


def end_screen(window, mainsurf, end):
    # THIS IS OUTDATED WATCH OUT AAAAAAAAA
    setGlobalDefaults()
    if end == "victory":
        playSound('victory')
    if end == "defeat":
        playSound('defeat')
    victory = pygame.transform.scale(victory_texture, (rta_dual(1, 1)))
    defeat = pygame.transform.scale(defeat_texture, (rta_dual(1, 1)))
    overlay = pygame.transform.scale(overlay_texture, (rta_dual(1, 1)))
    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.44))
    replay_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Replay", relpos=(0.05, 0.62))
    buttongroup.add(backtomenu_button, replay_button)
    overlay.set_alpha(2)
    window.blit(overlay, (0, 0))
    main_surface = pygame.Surface(rta_dual(1, 1))
    if end == "victory":
        main_surface.blit(victory, (0, 0))
    elif end == "defeat":
        main_surface.blit(defeat, (0, 0))
    main_surface.set_alpha(20)
    clock = pygame.time.Clock()
    i = 0
    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()
        i += 1
        if i < 32:
            window.blit(main_surface, (0, 0))
            pygame.display.update()
        elif i == 32:
            main_surface.set_alpha(255)
            window.blit(main_surface, (0, 0))
            for x in buttongroup:
                x.update()
                x.draw(window=window)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN and i > 64:
                if event.button == globs.LEFT:
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globs.exittomenu = True
                        globs.exittomenu = True
                    if replay_button.rect.collidepoint(mousepos):
                        run = False
                        globs.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.exittomenu = True
        for x in buttongroup:
            x.update()
            x.draw(window=window)
        pygame.display.update()
    playSound('click')


def settings(window, background):
    setGlobalDefaults()
    buttongroup = pygame.sprite.Group()

    settings = gui.GUI(background=background, overlay=128, buttons=[
        button.Button(anchor="bottomright", relwidth=0.4, relheight=0.1, textcontent="SAVE AND RETURN", relpos=(0.95, 0.95))])

    playSound('click')
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    pass
                    if settings.buttongroup[0].rect.collidepoint(mp):
                        run = False

                    # elif 190 < posY < 220 and 300 < posX < 450:
                    #    settings['background_music'] = not settings['background_music']
                    #    save_to_json(settings, "data")
                    # elif 220 < posY < 250 and 300 < posX < 450:
                    #    if settings['volume'] >= 10:
                    #        settings['volume'] = 0
                    #    settings['volume'] += 1
                    #    save_to_json(settings, "data")
                    # elif 250 < posY < 280 and 300 < posX < 450:
                    #    if settings['skin'] == "3lia03":
                    #        settings['skin'] = "Rande"
                    #    elif settings['skin'] == "Rande":
                    #        settings['skin'] = "3lia03"
                    #    save_to_json(settings, "data")
                    # elif 280 < posY < 310 and 300 < posX < 450:
                    #    print("test4")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        #draw(background, buttongroup, window)
        settings.draw(window=window)
    playSound('click')