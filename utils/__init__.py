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
    # w, h = pygame.display.get_surface().get_size()
    w, h = 256, 144
    output_x = w * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)


def relToAbsDualHeight(input_x, input_y):
    # w, h = pygame.display.get_surface().get_size()
    w, h = 256, 144
    output_x = h * input_x
    output_y = h * input_y
    return int(output_x), int(output_y)


def relToAbsDualWidth(input_x, input_y):
    # w, h = pygame.display.get_surface().get_size()
    w, h = 256, 144
    output_x = w * input_x
    output_y = w * input_y
    return int(output_x), int(output_y)


def relToAbsWidth(input_value):
    # w, h = pygame.display.get_surface().get_size()
    w, h = 256, 144
    output = w * input_value
    return int(output)


def relToAbsHeight(input_value):
    # w, h = pygame.display.get_surface().get_size()
    w, h = 256, 144
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
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption("Cobalt Quest version " + globs.VERSION + " by Rande")
    pygame.display.set_icon(icon_texture)
    if globs.fullscreen:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode(globs.res_size)
    print(window.get_size())
    return window


def renderText(window, text, position, color, size):
    pygame.freetype.init()
    font = pygame.freetype.Font("./resources/fonts/standart.otf", size)
    font.render_to(surf=window, dest=position, text=text, fgcolor=color)


def getTextRect(text, size):
    pygame.freetype.init()
    font = pygame.freetype.Font("./resources/fonts/standart.otf", size)
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
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./resources/sounds/click.wav"))
    elif sound == 'hit':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./resources/sounds/hit.wav"))
    elif sound == 'hurt':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./resources/sounds/hurt.wav"))
    elif sound == 'blockplace':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./resources/sounds/block_place.wav"))
    elif sound == 'swing':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./resources/sounds/swing.wav"))
    elif sound == 'victory':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("./resources/sounds/victory.wav"))
    elif sound == 'defeat':
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("./resources/sounds/defeat.wav"))
    pygame.mixer.Channel(1).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(2).set_volume(getSetting('volume') / 10)
    pygame.mixer.Channel(3).set_volume(getSetting('volume') / 10)


def play_theme():
    pygame.mixer.init()
    pygame.mixer.music.load("sounds/theme.wav")
    pygame.mixer.music.play(-1)


def save_to_json(data, name):
    with open(f'{name}.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)


def check_collision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False


def mousepos():
    return (pygame.mouse.get_pos()[0] / (globs.res_size[0] / globs.SIZE[0]),
            pygame.mouse.get_pos()[1] / (globs.res_size[1] / globs.SIZE[1]))
