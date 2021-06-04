import pygame, random, pygame.freetype, json
from data import globals


def absToRel(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = input_x / w
    output_y = input_y / h
    return output_x, output_y


def relToAbs(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = w * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)


def relToAbsHeight(input_value):
    # because i'm to dumb to use args
    w, h = pygame.display.get_surface().get_size()
    output = h * input_value
    return int(output)


def absToRelHeight(input_value):
    # because i'm to dumb to use args
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
    globals.victimspawns = 0
    globals.playerhealthpoints = (32 / globals.difficulty + globals.difficulty - 1)
    globals.maxcooldown = (60 / globals.difficulty)

    globals.damagecooldown = globals.maxcooldown
    globals.damageoverlaycooldown = 0
    globals.damagesum = 0

    globals.webs_left = 3
    globals.webcounter = 0

from data.sprites import web

def generateWeb(webgroup):
    webprogram = 'web' + str(globals.webcounter) + ' = web.Web()\nwebgroup.add(web' + str(
        globals.webcounter) + ')\nweb' + str(globals.webcounter) + '.summon()'
    exec(webprogram)
    print("EXECUTED")
    globals.webcounter += 1


def setupWindow():
    pygame.init()
    window = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    pygame.display.set_caption("WWOPW version " + globals.VERSION + " by Rande")
    pygame.display.flip()
    return window


def renderText(window, text, position, color, size):
    font = pygame.freetype.Font("data/fonts/standart.otf", size)
    font.render_to(window, position, text, color)


def renderIngameText(window):
    renderText(window, str(int(globals.playerhealthpoints)), relToAbs(0.07, 0.02), globals.WHITE, relToAbsHeight(0.048))
    # renderText(window, str((sum(i > 0 for i in globals.victimhealth))), (127, 10), globals.WHITE, 24)
    renderText(window, str(globals.victimspawns - globals.victimsmissed - globals.victimskilled + 1),
               relToAbs(0.254, 0.02), globals.WHITE, relToAbsHeight(0.048))
    renderText(window, str(globals.victimskilled), relToAbs(0.43, 0.02), globals.WHITE, relToAbsHeight(0.048))
    renderText(window, str(globals.victimsmissed), relToAbs(0.61, 0.02), globals.WHITE, relToAbsHeight(0.048))
    renderText(window, str(globals.damagesum), relToAbs(0.79, 0.02), globals.WHITE, relToAbsHeight(0.048))


def playSound(sound):
    pygame.mixer.init()
    if sound == 'click':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/click.wav"))
    elif sound == 'hit':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/hit.wav"))
    elif sound == 'hurt':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/sounds/hurt.wav"))
    elif sound == 'blockplace':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/block_place.wav"))
    elif sound == 'swing':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/sounds/swing.wav"))
    elif sound == 'victory':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("data/sounds/victory.wav"))
    elif sound == 'defeat':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("data/sounds/defeat.wav"))
    # volume = getSetting(setting='volume') / 10
    # pygame.mixer.Sound.set_volume(value=volume)


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

    playSound('click')

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
    playSound('click')


def showEndScreen(window, end):
    setGlobalDefaults()

    if end == "victory":
        playSound('victory')
    if end == "defeat":
        playSound('defeat')

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
        elif end == "defeat":
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
    elif end == "defeat":
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
                print("click")
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

    playSound('click')


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

    playSound('click')

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
                        playSound('click')
                    elif 220 < posY < 250 and 300 < posX < 450:
                        if settings['volume'] >= 10:
                            settings['volume'] = 0
                        settings['volume'] += 1
                        with open('data.json', 'w') as json_file:
                            json.dump(settings, json_file)
                            playSound('click')
                    elif 250 < posY < 280 and 300 < posX < 450:
                        if settings['skin'] == "3lia03":
                            settings['skin'] = "Rande"
                        elif settings['skin'] == "Rande":
                            settings['skin'] = "3lia03"
                        with open('data.json', 'w') as json_file:
                            json.dump(settings, json_file)
                        playSound('click')
                    elif 280 < posY < 310 and 300 < posX < 450:
                        print("test4")
                        playSound('click')
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

    playSound('click')


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False
