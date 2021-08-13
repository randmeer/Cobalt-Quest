import pygame

from utils import globs, playSound, setGlobalDefaults, relToAbsDual2, mousepos
from utils.images import overlay_texture, victory_texture, defeat_texture
from render.sprites import button


def draw(background, buttongroup, window):
    og_surface = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
    overlay = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    # TODO: remake the pause gui with buttons and labels, including the "PAUSED" title
    og_surface.blit(background, (0, 0))
    og_surface.blit(overlay, (0, 0))
    for i in buttongroup:
        i.update()
        i.draw(window=og_surface)
    surface = pygame.transform.scale(og_surface, globs.res_size)
    window.blit(surface, (0, 0))
    pygame.display.update()


def pause_screen(window, background):
    playSound('click')
    setGlobalDefaults()
    buttongroup = pygame.sprite.Group()
    resumeplaying_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Resume", relpos=(0.05, 0.44))
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.62))
    settings_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    buttongroup.add(resumeplaying_button, backtomenu_button, settings_button)

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
                    if resumeplaying_button.rect.collidepoint(mp):
                        run = False
                    if backtomenu_button.rect.collidepoint(mp):
                        run = False
                        globs.exittomenu = True
                    #if 367 < posY < 432 and 26 < posX < 475:
                    #    globs.exittomenu = True
                    if settings_button.rect.collidepoint(mp):
                        settings(window=window, background=background)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        draw(background, buttongroup, window)
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
    victory = pygame.transform.scale(victory_texture, (relToAbsDual2(1, 1)))
    defeat = pygame.transform.scale(defeat_texture, (relToAbsDual2(1, 1)))
    overlay = pygame.transform.scale(overlay_texture, (relToAbsDual2(1, 1)))
    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.44))
    replay_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Replay", relpos=(0.05, 0.62))
    buttongroup.add(backtomenu_button, replay_button)
    overlay.set_alpha(2)
    window.blit(overlay, (0, 0))
    main_surface = pygame.Surface(relToAbsDual2(1, 1))
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
    saveandreturn_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="save and return", relpos=(0.05, 0.80))
    buttongroup.add(saveandreturn_button)

    # TODO: remake the settings gui with buttons and labels, including the "SETTINGS" title
    def update():
        pass
        # renderText(window, 'Backgr. Music:', (50, 190), globs.WHITE, 30)
        # renderText(window, 'Sound Volume:', (50, 220), globs.WHITE, 30)
        # renderText(window, 'Skin:', (50, 250), globs.WHITE, 30)
        # renderText(window, 'Nickname:', (50, 280), globs.WHITE, 30)
        # renderText(window, 'WWOPW v0.8 by Rande', (50, 310), globs.GRAY, 30)
        # renderText(window, str(settings['background_music']), (300, 190), globs.WHITE, 30)
        # renderText(window, str(settings['volume']), (300, 220), globs.WHITE, 30)
        # renderText(window, str(settings['skin']), (300, 250), globs.WHITE, 30)
        # renderText(window, 'None', (300, 280), globs.WHITE, 30)

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
                    if saveandreturn_button.rect.collidepoint(mp):
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
        draw(background, buttongroup, window)
    playSound('click')