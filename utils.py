import json
import pygame
import pygame.freetype
import globals

victory_texture = pygame.image.load("textures/victory.png")
defeat_texture = pygame.image.load("textures/defeat.png")
overlay_texture = pygame.image.load("textures/overlay.png")
background_texture = pygame.image.load("textures/background.png")
settingsmenu_texture = pygame.image.load("textures/settings_menu.png")
pausemenu_texture = pygame.image.load("textures/pause_menu.png")

def absToRelDual(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = input_x / w
    output_y = input_y / h
    return output_x, output_y

def relToAbsDual(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = w * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)

def relToAbs(input_value):
    w, h = pygame.display.get_surface().get_size()
    output = h * input_value
    return int(output)

def absToRel(input_value):
    w, h = pygame.display.get_surface().get_size()
    output = input_value / h
    return output

def getSetting(setting):
    with open('data.json', 'r') as fr:
        settings = json.loads(fr.read())
    if setting == 'background_music':
        return settings['background_music']
    elif setting == 'volume':
        return settings['volume']
    elif setting == 'skin':
        return settings['skin']

def background():
    return pygame.transform.scale(background_texture, (500, 500))

def setGlobalDefaults():
    globals.quitgame = globals.exittomenu = globals.titlescreen = globals.menu = globals.level_selection = globals.rndebug = globals.level1 = False

def setGameDefaults():
    globals.victimbreakcooldownmax = 500 - 100 * globals.difficulty
    globals.victimsmissed = globals.victimskilled = 0
    # globals.victimspawns = (15 * globals.difficulty + globals.difficulty - 1)
    globals.victimspawns = 0
    globals.playerhealthpoints = (32 / globals.difficulty + globals.difficulty - 1)
    globals.maxcooldown = (60 / globals.difficulty)
    globals.damagecooldown = globals.maxcooldown
    globals.damageoverlaycooldown = 0
    globals.damagesum = 0
    globals.webs_left = 3
    globals.webcounter = 0

from sprites.web import Web

def generateWeb(webgroup):
    web = Web()
    webgroup.add(web)
    web.summon()
    globals.webcounter += 1
    return web

def setupWindow():
    pygame.init()
    window = pygame.display.set_mode((globals.windowsize, globals.windowsize), pygame.RESIZABLE)
    pygame.display.set_caption("WWOPW version " + globals.VERSION + " by Rande")
    return window

def renderText(window, text, position, color, size):
    font = pygame.freetype.Font("fonts/standart.otf", size)
    font.render_to(surf=window, dest=position, text=text, fgcolor=color)

def getTextRect(text, size):
    font = pygame.freetype.Font("fonts/standart.otf", size)
    return font.get_rect(text=text)

def renderIngameText(window):
    renderText(window, str(int(globals.playerhealthpoints)), relToAbsDual(0.07, 0.02), globals.WHITE, relToAbs(0.048))
    renderText(window, str(globals.victimspawns - globals.victimsmissed - globals.victimskilled + 1), relToAbsDual(0.254, 0.02), globals.WHITE, relToAbs(0.048))
    renderText(window, str(globals.victimskilled), relToAbsDual(0.43, 0.02), globals.WHITE, relToAbs(0.048))
    renderText(window, str(globals.victimsmissed), relToAbsDual(0.61, 0.02), globals.WHITE, relToAbs(0.048))
    renderText(window, str(globals.damagesum), relToAbsDual(0.79, 0.02), globals.WHITE, relToAbs(0.048))

def playSound(sound):
    pygame.mixer.init()
    if sound == 'click':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/click.wav"))
    elif sound == 'hit':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/hit.wav"))
    elif sound == 'hurt':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/hurt.wav"))
    elif sound == 'blockplace':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sounds/block_place.wav"))
    elif sound == 'swing':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("sounds/swing.wav"))
    elif sound == 'victory':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("sounds/victory.wav"))
    elif sound == 'defeat':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("sounds/defeat.wav"))

    pygame.mixer.Channel(1).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(2).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(3).set_volume(getSetting('volume') / 10)

def playTheme():
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/theme.wav")
    pygame.mixer.music.play(-1)

from sprites import button

def showPauseScreen(window, mainsurf):
    setGlobalDefaults()

    overlay = pygame.transform.scale(overlay_texture, (relToAbsDual(1, 1)))
    pausemenu = pygame.transform.scale(pausemenu_texture, (relToAbsDual(1, 1)))

    buttongroup = pygame.sprite.Group()
    resumeplaying_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Resume", relpos=(0.05, 0.44))
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.62))
    settings_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    buttongroup.add(resumeplaying_button, backtomenu_button, settings_button)

    window.blit(overlay, (0, 0))
    window.blit(pausemenu, (0, 0))
    for i in buttongroup:
        i.update()
        i.draw(window=window)
    pygame.display.update()

    playSound('click')

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.exittomenu = True
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    if resumeplaying_button.rect.collidepoint(mousepos):
                        run = False
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globals.exittomenu = True
                    if settings_button.rect.collidepoint(mousepos):
                        showSettings(window=window)
                        run = False
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
            if event.type == pygame.VIDEORESIZE:
                if event.w < 500 or event.h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((event.h, event.h), pygame.RESIZABLE)
                window.blit(pygame.transform.scale(mainsurf, relToAbsDual(1, 1)), (0, 0))
                window.blit(pygame.transform.scale(pausemenu_texture, relToAbsDual(1, 1)), (0, 0))
                for x in buttongroup:
                    x.update()
                    x.draw(window=window)
                pygame.display.update()
                globals.windowsize = event.h
    playSound('click')

def showEndScreen(window, mainsurf, end):
    setGlobalDefaults()

    if end == "victory":
        playSound('victory')
    if end == "defeat":
        playSound('defeat')

    victory = pygame.transform.scale(victory_texture, (relToAbsDual(1, 1)))
    defeat = pygame.transform.scale(defeat_texture, (relToAbsDual(1, 1)))
    overlay = pygame.transform.scale(overlay_texture, (relToAbsDual(1, 1)))

    buttongroup = pygame.sprite.Group()
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.44))
    replay_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Replay", relpos=(0.05, 0.62))
    buttongroup.add(backtomenu_button, replay_button)

    overlay.set_alpha(2)

    window.blit(overlay, (0, 0))

    main_surface = pygame.Surface(relToAbsDual(1, 1))

    if end == "victory":
        main_surface.blit(victory, (0, 0))
    elif end == "defeat":
        main_surface.blit(defeat, (0, 0))
    for x in buttongroup:
        x.update()
        x.draw(window=main_surface)
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
                globals.exittomenu = True
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN and i > 64:
                if event.button == globals.LEFT:
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globals.exittomenu = True
                    if replay_button.rect.collidepoint(mousepos):
                        run = False
                        globals.level1 = True
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.exittomenu = True
            if event.type == pygame.VIDEORESIZE:
                if event.w < 500 or event.h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((event.h, event.h), pygame.RESIZABLE)
                window.blit(pygame.transform.scale(mainsurf, relToAbsDual(1, 1)), (0, 0))
                window.blit(pygame.transform.scale(main_surface, relToAbsDual(1, 1)), (0, 0))
                for x in buttongroup:
                    x.update()
                    x.draw(window=window)
                pygame.display.update()
                globals.windowsize = event.h

    playSound('click')

def save_to_json(data, name):
    with open(f'{name}.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

def showSettings(window):
    setGlobalDefaults()

    with open('data.json', "r") as f:
        settings = json.loads(f.read())

    backgr = pygame.transform.scale(background_texture, (relToAbsDual(1, 1)))
    settingsmenu = pygame.transform.scale(settingsmenu_texture, (relToAbsDual(1, 1)))

    buttongroup = pygame.sprite.Group()
    saveandreturn_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="save and return", relpos=(0.05, 0.80))
    buttongroup.add(saveandreturn_button)

    # TODO: remake the settings gui with label-sprites
    def update():
        window.blit(backgr, (0, 0))
        window.blit(settingsmenu, (0, 0))
        renderText(window, 'Backgr. Music:', (50, 190), globals.WHITE, 30)
        renderText(window, 'Sound Volume:', (50, 220), globals.WHITE, 30)
        renderText(window, 'Skin:', (50, 250), globals.WHITE, 30)
        renderText(window, 'Nickname:', (50, 280), globals.WHITE, 30)
        renderText(window, 'WWOPW v0.8 by Rande', (50, 310), globals.GRAY, 30)
        renderText(window, str(settings['background_music']), (300, 190), globals.WHITE, 30)
        renderText(window, str(settings['volume']), (300, 220), globals.WHITE, 30)
        renderText(window, str(settings['skin']), (300, 250), globals.WHITE, 30)
        renderText(window, 'None', (300, 280), globals.WHITE, 30)
        for i in buttongroup:
            i.update()
            i.draw(window=window)
        pygame.display.update()

    update()
    playSound('click')
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()

        with open('data.json', 'r') as fr:
            settings = json.loads(fr.read())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.exittomenu = True
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    if saveandreturn_button.rect.collidepoint(mousepos):
                        run = False
                    elif 190 < posY < 220 and 300 < posX < 450:
                        settings['background_music'] = not settings['background_music']
                        save_to_json(settings, "data")
                    elif 220 < posY < 250 and 300 < posX < 450:
                        if settings['volume'] >= 10:
                            settings['volume'] = 0
                        settings['volume'] += 1
                        save_to_json(settings, "data")
                    elif 250 < posY < 280 and 300 < posX < 450:
                        if settings['skin'] == "3lia03":
                            settings['skin'] = "Rande"
                        elif settings['skin'] == "Rande":
                            settings['skin'] = "3lia03"
                        save_to_json(settings, "data")
                    elif 280 < posY < 310 and 300 < posX < 450:
                        print("test4")
                    playSound('click')
                    update()

            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False

    playSound('click')

def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False
