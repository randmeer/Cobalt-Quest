import pygame, random
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


def playCurrentState():
    if globals.titlescreen:
        title_screen.showTitleScreen()
    elif globals.menu:
        menu.showMenu()
    elif globals.level_selection:
        level_selection.showLevelSelection()
    elif globals.level1:
        level1.playLevel1(globals.difficulty)
    else:
        print("yeah so there is no current state u f**ked up")
    print("CYCLED TROUGH CURRENT STATES")


def generateDirections():
    i = 15
    while i >= 0:
        globals.direction.append(random.randint(1, 4))
        i -= 1


def generateVictims(victimgroup):
    victimcounter = 0

    while victimcounter <= 15:
        victimprogram = 'victim' + str(victimcounter) + ' = victim.Victim()\nvictimgroup.add(victim' + str(victimcounter) + ')\nglobals.victims.append(victim' + str(victimcounter) + ')'
        exec(victimprogram)
        print(victimprogram)
        print("EXECUTED")
        victimcounter += 1
    print(globals.victims)


def updateVictims(velocity):
    i = 15
    while i >= 0:
        globals.victims[i].update(globals.direction[i], velocity)
        i -= 1


def setupWindow():
    pygame.init()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("WWOPW version 0.5 by Rande")
    pygame.display.flip()
    return window


def playClick():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/click.wav"))


def playHit():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/hit.wav"))


def playBlockPlace():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(1).play(pygame.mixer.Sound("data/sounds/block_place.wav"))


def playSwing():
    pygame.mixer.init()
    # pygame.mixer.music.load("sounds/click.wav")
    pygame.mixer.Channel(2).play(pygame.mixer.Sound("data/sounds/swing.wav"))


def playTheme():
    pygame.mixer.init()
    pygame.mixer.music.load("data/sounds/theme.wav")
    pygame.mixer.music.play(-1)
    # pygame.mixer.Channel(0).play(pygame.mixer.Sound("sounds/theme.wav"))


def showPauseScreen(window):
    setGlobalDefaults()

    overlay_original = pygame.image.load("data/textures/overlay.png")
    overlay = pygame.transform.scale(overlay_original, (500, 500))
    pausemenu_original = pygame.image.load("data/textures/pause_menu.png")
    pausemenu = pygame.transform.scale(pausemenu_original, (500, 500))

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
    # pygame.time.delay(1000)


def checkCollision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False


def background():
    background_original = pygame.image.load("data/textures/background.png")
    return pygame.transform.scale(background_original, (500, 500))
