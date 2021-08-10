import json
import pygame
import pygame.freetype
import pygame.freetype
from utils import globs

class DefaultError(Exception):
    def __init__(self, errmsg='unknown error has occured'):
        self.errmsg = errmsg
        Exception.__init__(self, errmsg)

    def __reduce__(self):
        return self.__class__, self.errmsg

from utils.images import icon_texture

def resizeWindow(eventw, eventh):
    # if eventw == globs.width and eventh != globs.height:
    #     if eventh < 500:
    #         globs.height = 500
    #         globs.width = int(500 * 16 / 9)
    #     else:
    #         globs.height = eventh
    #         globs.width = int(eventh * 16 / 9)
    # elif eventw != globs.width and eventh == globs.height:
    #     if eventw < int(500 * 16 / 9):
    #         globs.height = 500
    #         globs.width = int(500 * 16 / 9)
    #     else:
    #         globs.width = eventw
    #         globs.height = int(eventw * 9 / 16)
    # elif eventw != globs.width and eventh != globs.height:
    #     if eventh < 500:
    #         globs.height = 500
    #         globs.width = int(500 * 16 / 9)
    #     else:
    #         globs.height = eventh
    #         globs.width = int(eventh * 16 / 9)
    # pygame.display.set_mode((globs.width, globs.height), pygame.RESIZABLE)
    if eventw == globs.width and eventh != globs.height:
        if eventh < 250:
            globs.height = 250
        else:
            globs.height = eventh
    elif eventw != globs.width and eventh == globs.height:
        if eventw < int(250 * 16 / 9):
            globs.width = int(250 * 16 / 9)
        else:
            globs.width = eventw
    elif eventw != globs.width and eventh != globs.height:
        if eventh < 250:
            globs.height = 250
        if eventw < int(250 * 16 / 9):
            globs.width = int(250 * 16 / 9)
        else:
            globs.height = eventh
            globs.width = eventw

    pygame.display.set_mode((globs.width, globs.height), pygame.RESIZABLE)

def absToRelDual(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = input_x / h
    output_y = input_y / h
    return output_x, output_y

def relToAbsDual(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = h * input_x
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

# these rel functions should replace the rel functions someday
# they work with the whole window, while rel functions only apply to a square with a = windowheight

def relToAbsDual2(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = w * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)

def relToAbsDualHeight(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = h * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)

def relToAbsDualWidth(input_x, input_y):
    w, h = pygame.display.get_surface().get_size()
    output_x = w * input_x
    output_y = w * input_y
    return int(output_x), int(output_y)

def relToAbsWidth(input_value):
    w, h = pygame.display.get_surface().get_size()
    output = w * input_value
    return int(output)

def relToAbsHeight(input_value):
    w, h = pygame.display.get_surface().get_size()
    output = h * input_value
    return int(output)


def getSetting(setting):
    with open('./data/data.json', 'r') as fr:
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
    globs.quitgame = False
    globs.exittomenu = False
    globs.titlescreen = False
    globs.menu = False
    globs.level_selection = False
    globs.rndebug = False
    globs.level1 = False
    globs.quitgame = globs.exittomenu = globs.titlescreen = globs.menu = globs.level_selection = globs.rndebug = globs.level1 = False

def setGameDefaults():
    globs.victimbreakcooldownmax = 500 - 100 * globs.difficulty

    globs.victimsmissed = 0
    globs.victimskilled = 0

    globs.victimbreakcooldownmax = 500 - 100 * globs.difficulty
    globs.victimsmissed = globs.victimskilled = 0
    # globs.victimspawns = (15 * globs.difficulty + globs.difficulty - 1)
    globs.victimspawns = 0
    globs.playerhealthpoints = (32 / globs.difficulty + globs.difficulty - 1)
    globs.maxcooldown = (60 / globs.difficulty)

    globs.damagecooldown = globs.maxcooldown
    globs.damageoverlaycooldown = 0
    globs.damagesum = 0

    globs.webs_left = 3
    globs.webcounter = 0
    globs.victimspawns = 0
    globs.playerhealthpoints = (32 / globs.difficulty + globs.difficulty - 1)
    globs.maxcooldown = (60 / globs.difficulty)
    globs.damagecooldown = globs.maxcooldown
    globs.damageoverlaycooldown = 0
    globs.damagesum = 0
    globs.webs_left = 3
    globs.webcounter = 0

def setupWindow():
    pygame.init()
    pygame.display.set_caption("Cobalt Quest version " + globs.VERSION + " by Rande")
    window = pygame.display.set_mode((globs.width, globs.height), pygame.RESIZABLE)
    pygame.display.set_icon(icon_texture)
    pygame.display.flip()
    return window

def renderText(window, text, position, color, size):
    font = pygame.freetype.Font("./Resources/fonts/standart.otf", size)
    font.render_to(surf=window, dest=position, text=text, fgcolor=color)

def getTextRect(text, size):
    font = pygame.freetype.Font("./Resources/fonts/standart.otf", size)
    return font.get_rect(text=text)

def gradientRect(width, height, left_colour, right_color):
    color_rect = pygame.Surface((2, 2))
    pygame.draw.line(color_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(color_rect, right_color, (1, 0), (1, 1))
    color_rect = pygame.transform.smoothscale(color_rect, (width, height))
    return color_rect

def playSound(sound):
    pygame.mixer.init()
    if sound == 'click':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./Resources/sounds/click.wav"))
    elif sound == 'hit':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./Resources/sounds/hit.wav"))
    elif sound == 'hurt':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./Resources/sounds/hurt.wav"))
    elif sound == 'blockplace':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./Resources/sounds/block_place.wav"))
    elif sound == 'swing':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./Resources/sounds/swing.wav"))
    elif sound == 'victory':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("./Resources/sounds/victory.wav"))
    elif sound == 'defeat':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("./Resources/sounds/defeat.wav"))
    pygame.mixer.Channel(1).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(2).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(3).set_volume(getSetting('volume') / 10)

def play_theme():
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/theme.wav")
    pygame.mixer.music.play(-1)

from Render.sprites import button
from utils.images import background_texture, overlay_texture, pause_menu_texture, victory_texture, defeat_texture,\
    settings_menu_texture

def pause_screen(window, mainsurf):
    playSound('click')
    setGlobalDefaults()
    buttongroup = pygame.sprite.Group()
    resumeplaying_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Resume", relpos=(0.05, 0.44))
    backtomenu_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Back to Menu", relpos=(0.05, 0.62))
    settings_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    buttongroup.add(resumeplaying_button, backtomenu_button, settings_button)
    def draw(resize=False):
        if resize:
            overlay = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA, 32)
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            gamesurf = pygame.transform.scale(mainsurf, relToAbsDual2(1, 1))
            # TODO: remake the pause gui with buttons and labels, including the "PAUSED" title
            #pausemenu = pygame.transform.scale(pause_menu_texture, relToAbsDual(1, 1))
        window.blit(gamesurf, (0, 0))
        window.blit(overlay, (0, 0))
        #window.blit(pausemenu, (0, 0))
        pygame.display.update()
    draw(resize=True)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    posX = (pygame.mouse.get_pos()[0])
                    posY = (pygame.mouse.get_pos()[1])
                if event.button == globs.LEFT:
                    if resumeplaying_button.rect.collidepoint(mousepos):
                        run = False
                    if backtomenu_button.rect.collidepoint(mousepos):
                        run = False
                        globs.exittomenu = True
                    if 367 < posY < 432 and 26 < posX < 475:
                        globs.exittomenu = True
                    if settings_button.rect.collidepoint(mousepos):
                        settings(window=window, backgr=pygame.transform.scale(mainsurf, relToAbsDual2(1, 1)))
                        draw(resize=True)
            if event.type == pygame.KEYDOWN:
                if event.key == globs.ESCAPE:
                    run = False
            if event.type == pygame.VIDEORESIZE:
                resizeWindow(event.w, event.h)
                draw(resize=True)
        for i in buttongroup:
            i.update()
            i.draw(window=window)
        pygame.display.update()
        if globs.exittomenu:
            run = False
    playSound('click')

def end_screen(window, mainsurf, end):
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
                if event.key == globs.ESCAPE:
                    run = False
                    globs.exittomenu = True
            if event.type == pygame.VIDEORESIZE:
                resizeWindow(event.w, event.h)
                window.blit(pygame.transform.scale(mainsurf, relToAbsDual(1, 1)), (0, 0))
                window.blit(pygame.transform.scale(main_surface, relToAbsDual(1, 1)), (0, 0))
        for x in buttongroup:
            x.update()
            x.draw(window=window)
        pygame.display.update()
    playSound('click')

def save_to_json(data, name):
    with open(f'{name}.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

def settings(window, backgr):
    setGlobalDefaults()
    buttongroup = pygame.sprite.Group()
    saveandreturn_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="save and return", relpos=(0.05, 0.80))
    buttongroup.add(saveandreturn_button)

    def resize():
        overlay = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA, 32)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        # background, overlay and settingsmenu only get blitted on resize to save performance
        #settingsmenu = pygame.transform.scale(settings_menu_texture, (relToAbs(1), relToAbs(1)))
        settingsbackgr = pygame.transform.scale(backgr, relToAbsDual2(1, 1))
        window.blit(settingsbackgr, (0, 0))
        window.blit(overlay, (0, 0))
        #window.blit(settingsmenu, (0, 0))
    resize()

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
        mousepos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.exittomenu = True
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if saveandreturn_button.rect.collidepoint(mousepos):
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
                if event.key == globs.ESCAPE:
                    run = False
            if event.type == pygame.VIDEORESIZE:
                resizeWindow(event.w, event.h)
                resize()
        for x in buttongroup:
            x.update()
            x.draw(window=window)
        pygame.display.update()
    playSound('click')

def check_collision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False
