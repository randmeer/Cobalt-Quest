import pygame, random, pygame.freetype, json
from data import globals, title_screen, menu, level_selection, level1
from data.sprites import victim, player, web


def background():
    background_original = pygame.image.load("data/textures/background.png")
    return pygame.transform.scale(background_original, (500, 500))


def setGlobalDefaults():
    globals.quitgame = False
    globals.exittomenu = False
    globals.titlescreen = False
    globals.menu = False
    globals.level_selection = False
    globals.rndebug = False
    globals.level1 = False


def setGameDefaults():
    globals.victimbreakcooldownmax = 500 - 100 * globals.difficulty

    globals.victimsmissed = 0
    globals.victimskilled = 0

    # globals.victimspawns = (15 * globals.difficulty + globals.difficulty - 1)
    globals.victimspawns = 1
    globals.playerhealthpoints = (32 / globals.difficulty + globals.difficulty - 1)
    globals.maxcooldown = (60 / globals.difficulty)

    globals.damagecooldown = globals.maxcooldown
    globals.damageoverlaycooldown = 0
    globals.damagesum = 0

    globals.webs_left = 3
    globals.webcounter = 0


def playCurrentState():
    if globals.titlescreen:
        title_screen.showTitleScreen()
    elif globals.menu:
        menu.showMenu()
    elif globals.level_selection:
        level_selection.showLevelSelection()
    elif globals.level1:
        level1.playLevel1()
    else:
        print("yeah so there is no current state u f**ked up")
    print("CYCLED TROUGH CURRENT STATES")


def generateWeb(webgroup):
    webprogram = 'web' + str(globals.webcounter) + ' = web.Web()\nwebgroup.add(web' + str(
        globals.webcounter) + ')\nweb' + str(globals.webcounter) + '.summon()'
    exec(webprogram)
    print(webprogram)
    print("EXECUTED")
    globals.webcounter += 1


def setupWindow():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("WWOPW version " + globals.VERSION + " by Rande")
    pygame.display.flip()
    return window


def renderText(window, text, position, color, size):
    font = pygame.freetype.Font("data/fonts/standart.otf", size)
    font.render_to(window, position, text, color)


def renderIngameText(window):
    renderText(window, str(int(globals.playerhealthpoints)), (35, 10), globals.WHITE, 24)
    #renderText(window, str((sum(i > 0 for i in globals.victimhealth))), (127, 10), globals.WHITE, 24)
    renderText(window, str(globals.victimspawns-globals.victimsmissed-globals.victimskilled + 1), (127, 10), globals.WHITE, 24)
    renderText(window, str(globals.victimskilled), (215, 10), globals.WHITE, 24)
    renderText(window, str(globals.victimsmissed), (305, 10), globals.WHITE, 24)
    renderText(window, str(globals.damagesum), (395, 10), globals.WHITE, 24)


def playClick():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/click.wav"))


def playHit():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/hit.wav"))


def playHurt():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/sounds/hurt.wav"))


def playBlockPlace():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/block_place.wav"))


def playSwing():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/sounds/swing.wav"))


def playVictory():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(3).play(pygame.mixer.Sound("data/sounds/victory.wav"))


def playDefeat():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(3).play(pygame.mixer.Sound("data/sounds/defeat.wav"))


def playTheme():
    pygame.mixer.init()
    pygame.mixer.music.load("data/sounds/theme.wav")
    pygame.mixer.music.play(-1)
    # pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/theme.wav"))


def showPauseScreen(window):
    setGlobalDefaults()

    overlay = pygame.transform.scale(pygame.image.load("data/textures/overlay.png"), (500, 500))
    pausemenu = pygame.transform.scale(pygame.image.load("data/textures/pause_menu.png"), (500, 500))

    window.blit(overlay, (0, 0))
    window.blit(pausemenu, (0, 0))
    pygame.display.update()

    playClick()

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.exittomenu = True
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    # print(posX, " ", posY)
                    if 207 < posY < 272 and 26 < posX < 475:
                        run = False
                    if 287 < posY < 352 and 26 < posX < 475:
                        run = False
                        globals.exittomenu = True
                    if 367 < posY < 432 and 26 < posX < 475:
                        run = False
                        showSettings(window)

            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
    playClick()


def showEndScreen(window, end):
    setGlobalDefaults()

    if end == "victory":
        playVictory()
    if end == "defeat":
        playDefeat()

    victory = pygame.transform.scale(pygame.image.load("data/textures/victory.png"), (500, 500))
    defeat = pygame.transform.scale(pygame.image.load("data/textures/defeat.png"), (500, 500))
    overlay = pygame.transform.scale(pygame.image.load("data/textures/overlay.png"), (500, 500))

    overlay.set_alpha(2)
    clock = pygame.time.Clock()

    i = 0
    animrun = True
    while animrun:
        clock.tick(60)
        window.blit(overlay, (0, 0))
        if end == "victory":
            victory.set_alpha(i)
            window.blit(victory, (0, 0))
        if end == "defeat":
            defeat.set_alpha(i)
            window.blit(defeat, (0, 0))
        pygame.display.update()
        i += 1
        if i > 64:
            animrun = False

    victory.set_alpha(256)
    defeat.set_alpha(256)

    if end == "victory":
        window.blit(victory, (0, 0))
    if end == "defeat":
        window.blit(defeat, (0, 0))
    pygame.display.update()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.exittomenu = True
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    if 207 < posY < 272 and 26 < posX < 475:
                        run = False
                        globals.exittomenu = True

            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.exittomenu = True

    playClick()


def showSettings(window):
    setGlobalDefaults()

    with open('data.json', "r") as f:
        settings = json.loads(f.read())

    # Reading from file

    # Iterating through the json
    for i in settings:
        print(i)

    print(settings['volume'])
    print(settings['background_music'])

    backgr = pygame.transform.scale(pygame.image.load("data/textures/background.png"), (500, 500))
    settingsmenu = pygame.transform.scale(pygame.image.load("data/textures/settings_menu.png"), (500, 500))

    window.blit(backgr, (0, 0))
    window.blit(settingsmenu, (0, 0))
    renderText(window, 'Backgr. Music:', (50, 190), globals.WHITE, 30)
    renderText(window, 'Sound Volume:', (50, 220), globals.WHITE, 30)
    renderText(window, 'Skin:', (50, 250), globals.WHITE, 30)
    renderText(window, 'Nickname:', (50, 280), globals.WHITE, 30)
    renderText(window, 'WWOPW ' + globals.VERSION + ' by Rande', (50, 310), globals.WHITE, 30)

    renderText(window, str(settings['background_music']), (300, 190), globals.WHITE, 30)
    renderText(window, '100%', (300, 220), globals.WHITE, 30)
    renderText(window, '3lia03', (300, 250), globals.WHITE, 30)
    renderText(window, '', (300, 280), globals.WHITE, 30)

    pygame.display.update()

    playClick()

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

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
                    # print(posX, " ", posY)
                    if 367 < posY < 432 and 26 < posX < 475:
                        run = False
                    elif 190 < posY < 220 and 300 < posX < 450:
                        settings['background_music'] = not settings['background_music']
                        with open('data.json', 'w') as json_file:
                            json.dump(settings, json_file)
                        playClick()
                    elif 220 < posY < 250 and 300 < posX < 450:
                        if settings['volume'] >= 10:
                            settings['volume'] = 0
                        settings['volume'] += 1
                        with open('data.json', 'w') as json_file:
                            json.dump(settings, json_file)
                            playClick()
                    elif 250 < posY < 280 and 300 < posX < 450:
                        if settings['skin'] == "3lia03":
                            settings['skin'] = "Rande"
                        elif settings['skin'] == "Rande":
                            settings['skin'] = "3lia03"
                        with open('data.json', 'w') as json_file:
                            json.dump(settings, json_file)
                        playClick()
                    elif 280 < posY < 310 and 300 < posX < 450:
                        print("test4")
                        playClick()
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False

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
        pygame.display.update()

    playClick()


def getSetting(setting):
    with open('data.json', 'r') as fr:
        settings = json.loads(fr.read())
    if setting == 'background_music':
        return settings['background_music']
    elif setting == 'volume':
        return settings['volume']
    elif setting == 'skin':
        return settings['skin']


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False
