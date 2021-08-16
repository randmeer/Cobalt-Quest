import json
import pygame
import pygame.freetype
import pygame.freetype
from utils import globs


def write_json(data, name):
    with open(f'{name}.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_json(path):
    with open(path, 'r') as fr:
        data = json.loads(fr.read())
    return data

def getSetting(setting):
    settings = read_json('./data/settings.json')
    return settings[setting]


def set_resolution():
    aspect_ratio = getSetting('aspect_ratio')
    resolution = getSetting('resolution')
    fullscreen = getSetting('fullscreen')
    if aspect_ratio == "16to9":
        globs.res = globs.RES_16TO9[resolution]
    elif aspect_ratio == "16to10":
        globs.res = globs.RES_16TO10[resolution]
    elif aspect_ratio == "4to3":
        globs.res = globs.RES_4TO3[resolution]
    globs.fullscreen = fullscreen
    globs.res_size = globs.res[0]
    globs.res_name = globs.res[1]
    print("RESOLUTION: " + str(globs.res))

class DefaultError(Exception):
    def __init__(self, errmsg='unknown error has occured'):
        self.errmsg = errmsg
        Exception.__init__(self, errmsg)
    def __reduce__(self):
        return self.__class__, self.errmsg


w, h = 256, 144

def rta_width(input_value):
    output = w * input_value
    return round(output)

def atr_width(input_value):
    output = input_value / w
    return output

def rta_height(input_value):
    output = h * input_value
    return round(output)

def atr_height(input_value):
    output = input_value / h
    return output

def rta_dual(input_x, input_y):
    output_x, output_y = w * input_x, h * input_y
    return round(output_x), round(output_y)

def atr_dual(input_x, input_y):
    output_x, output_y = input_x / w, input_y / h
    return output_x, output_y

def rta_dual_height(input_x, input_y):
    output_x, output_y = h * input_x, h * input_y
    return round(output_x), round(output_y)

def atr_dual_height(input_x, input_y):
    output_x, output_y = input_x / h, input_y / h
    return output_x, output_y

def rta_dual_width(input_x, input_y):
    output_x, output_y = w * input_x, w * input_y
    return round(output_x), round(output_y)

def atr_dual_width(input_x, input_y):
    output_x, output_y = input_x / w, input_y / w
    return output_x, output_y


def setGlobalDefaults():
    globs.quitgame = globs.exittomenu = globs.titlescreen = globs.menu = globs.level_selection = globs.rndebug = globs.level1 = False


def setGameDefaults():
    pass
    # globs.victimbreakcooldownmax = 500 - 100 * globs.difficulty
    #
    # globs.victimsmissed = 0
    # globs.victimskilled = 0
    #
    # globs.victimbreakcooldownmax = 500 - 100 * globs.difficulty
    # globs.victimsmissed = globs.victimskilled = 0
    # # globs.victimspawns = (15 * globs.difficulty + globs.difficulty - 1)
    # globs.victimspawns = 0
    # globs.playerhealthpoints = (32 / globs.difficulty + globs.difficulty - 1)
    # globs.maxcooldown = (60 / globs.difficulty)
    #
    # globs.damagecooldown = globs.maxcooldown
    # globs.damageoverlaycooldown = 0
    # globs.damagesum = 0
    #
    # globs.webs_left = 3
    # globs.webcounter = 0
    # globs.victimspawns = 0
    # globs.playerhealthpoints = (32 / globs.difficulty + globs.difficulty - 1)
    # globs.maxcooldown = (60 / globs.difficulty)
    # globs.damagecooldown = globs.maxcooldown
    # globs.damageoverlaycooldown = 0
    # globs.damagesum = 0
    # globs.webs_left = 3
    # globs.webcounter = 0


def setupWindow():
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption(f"Cobalt Quest {globs.VERSION}")
    pygame.display.set_icon(pygame.image.load('./resources/textures/' + "icon.png"))
    if globs.fullscreen:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode(globs.res_size)
    return window


def renderText(window, text, position, color, size=5, antialiased=False, vertical=False, font="game"):
    if font == "game":
        f = pygame.freetype.Font("./resources/fonts/PortableVengeance.ttf", size)
    elif font == "debug":
        f = pygame.freetype.Font("./resources/fonts/standart.otf", size)
    # PortableVengeance by Pixel Kitchen on fontspace.com, Licensed as Public Domain
    # The dot (.) has been modified
    # px * .75 = pt (example: 8px is equivalent to 6pt)
    f.antialiased = antialiased
    f.vertical = vertical
    f.render_to(surf=window, dest=position, text=text, fgcolor=color)


def getTextRect(text, size=5, font="game"):
    if font == "game":
        f = pygame.freetype.Font("./resources/fonts/PortableVengeance.ttf", size)
    elif font == "debug":
        f = pygame.freetype.Font("./resources/fonts/standart.otf", size)
    return f.get_rect(text=text)


def gradientRect(width, height, left_colour, right_color):
    color_rect = pygame.Surface((2, 2))
    pygame.draw.line(color_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(color_rect, right_color, (1, 0), (1, 1))
    color_rect = pygame.transform.smoothscale(color_rect, (width, height))
    return color_rect


def playSound(sound):
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


def play_music(music):
    if music == "menu":
        pygame.mixer.music.load("./resources/sounds/theme1_calm_before_the_storm.wav")
    pygame.mixer.music.play(-1)


def check_collision(sprite1, sprite2):
    col = pygame.sprite.collide_rect(sprite1, sprite2)
    if col:
        return True
    else:
        return False


def mousepos():
    return (pygame.mouse.get_pos()[0] / (globs.res_size[0] / globs.SIZE[0]),
            pygame.mouse.get_pos()[1] / (globs.res_size[1] / globs.SIZE[1]))


def set_anchor_point(rect, pos, anchor):
    if anchor == "midtop":
        rect.midtop = pos
    elif anchor == "midbottom":
        rect.midbottom = pos
    elif anchor == "midleft":
        rect.midleft = pos
    elif anchor == "midright":
        rect.midright = pos
    elif anchor == "topleft":
        rect.topleft = pos
    elif anchor == "topright":
        rect.topright = pos
    elif anchor == "bottomleft":
        rect.bottomleft = pos
    elif anchor == "bottomright":
        rect.bottomright = pos
    elif anchor == "center":
        rect.center = pos
