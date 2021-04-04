import pygame, random, pygame.freetype
from data import globals, title_screen, menu, level_selection, level1
from data.sprites import victim, player

LEFT = 1
MIDDLE = 2
RIGHT = 3
ESCAPE = 27


def setGlobalDefaults():
    globals.quitgame = False
    globals.exittomenu = False
    globals.titlescreen = False
    globals.menu = False
    globals.level_selection = False
    globals.rndebug = False
    globals.level1 = False


def setGameDefaults():
    globals.direction = []
    globals.victims = []
    globals.victimhealth = []
    globals.on_screen = []

    globals.victimsmissed = 0
    globals.victimskilled = 0
    globals.playerhealthpoints = 0
    globals.victimspawns = 0
    globals.victimspawns = 0

    globals.victimspawns = (15 * globals.difficulty + globals.difficulty - 1)
    globals.playerhealthpoints = (32 / globals.difficulty + globals.difficulty - 1)
    globals.maxcooldown = (60 / globals.difficulty)

    globals.damagecooldown = globals.maxcooldown
    globals.damageoverlaycooldown = 0
    globals.damagesum = 0


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


def generateDirections():
    i = globals.victimspawns
    while i >= 0:
        globals.direction.append(random.randint(1, 4))
        globals.on_screen.append(False)
        i -= 1


def generateVictims(victimgroup):
    i = globals.victimspawns

    while i >= 0:
        victimprogram = 'victim' + str(i) + ' = victim.Victim()\nvictimgroup.add(victim' + str(
            i) + ')\nglobals.victims.append(victim' + str(i) + ')'
        globals.victimhealth.append(globals.victimhealthpoints)
        exec(victimprogram)
        print(victimprogram)
        print("EXECUTED")
        i -= 1
    print(globals.victims)


def updateVictims(velocity, playersprite, click):
    i = globals.victimspawns
    while i >= 0:
        globals.victims[i].update(globals.direction[i], velocity, playersprite, i, click, globals.damagecooldown)
        i -= 1


def setupWindow():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("WWOPW version 0.7 by Rande")
    pygame.display.flip()
    return window


def renderText(window, text, position, color, size):
    font = pygame.freetype.Font("data/fonts/standart.otf", size)
    font.render_to(window, position, text, color)


def renderIngameText(window):
    renderText(window, str(int(globals.playerhealthpoints)), (35, 10), globals.WHITE, 24)
    renderText(window, str((sum(i > 0 for i in globals.victimhealth))), (127, 10), globals.WHITE, 24)
    # renderText(window, str(sum(globals.on_screen)), (127, 10), globals.WHITE, 24)
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
    pygame.display.flip()

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
                if event.button == LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    # print(posX, " ", posY)
                    if 207 < posY < 272 and 26 < posX < 475:
                        run = False
                    if 287 < posY < 352 and 26 < posX < 475:
                        run = False
                        globals.exittomenu = True

            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE:
                    run = False
    playClick()


def showVictoryScreen(window):
    setGlobalDefaults()

    victory = pygame.transform.scale(pygame.image.load("data/textures/victory.png"), (500, 500))
    overlay = pygame.transform.scale(pygame.image.load("data/textures/overlay.png"), (500, 500))

    i = 0
    while i < 256:
        overlay.set_alpha(i)
        window.blit(overlay, (0, 0))
        pygame.display.flip()
        i -= 1

    window.blit(overlay, (0, 0))
    window.blit(victory, (0, 0))
    pygame.display.flip()

    playVictory()

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
                if event.button == LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                    if 207 < posY < 272 and 26 < posX < 475:
                        run = False
                        globals.exittomenu = True

            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE:
                    run = False
                    globals.exittomenu = True
    playClick()


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False


def background():
    background_original = pygame.image.load("data/textures/background.png")
    return pygame.transform.scale(background_original, (500, 500))
