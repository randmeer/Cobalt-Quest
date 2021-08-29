import random
import pygame
import pygame.freetype
import QuickJSON
import math
from utils import globs

# math utils

def hypo(a, b):
    """
    right-angled triangle:
    kathete a, kathete b --> hypothenuse c
    """
    c = math.sqrt(a ** 2 + b ** 2)
    return c

def angle_deg(p1, p2):
    """
    point p1, point p2 --> angle in degrees
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0:
        if dy == 0:
            deg = 0
        else:
            deg = 0 if p1[1] > p2[1] else 180
    elif dy == 0:
        deg = 90 if p1[0] < p2[0] else 270
    else:
        deg = math.atan(dy / dx) / math.pi * 180
        lowering = p1[1] < p2[1]
        if (lowering and deg < 0) or (not lowering and deg > 0):
            deg += 270
        else:
            deg += 90
    return deg

def conv_deg_rad(deg):
    """
    degrees --> radiants
    """
    rad = deg * math.pi / 180
    return rad

def sign(num):
    """
    positive value --> 1
    negative value --> -1
    zero --> 0
    """
    try:
        return num / abs(num)
    except ZeroDivisionError:
        return 0

def flip(num):
    """
    flips a values sign (+/-)
    """
    return 1 ^ num

def sin(num):
    return math.sin(num)

def cos(num):
    return math.cos(num)

settings = QuickJSON.QJSON("./data/settings.json")

def set_setting(setting, value):
    settings[setting] = value
    settings.save()

def get_setting(setting):
    settings.load()
    return settings[setting]

def set_resolution():
    aspect_ratio = get_setting('aspect_ratio')
    resolution = get_setting('resolution')
    fullscreen = get_setting('fullscreen')
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


def set_global_defaults():
    globs.quitgame = globs.exittomenu = globs.titlescreen = globs.menu = globs.map = globs.rndebug = globs.dungeon = False


def set_game_defaults():
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


def setup_window():
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption(f"Cobalt Quest {globs.VERSION}")
    pygame.display.set_icon(pygame.image.load('./resources/textures/' + "icon.png"))
    if globs.fullscreen:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode(globs.res_size)
    return window


def render_text(window, text, pos, color, size=5, antialiased=False, vertical=False, font="game"):
    if font == "game":
        f = pygame.freetype.Font("./resources/fonts/PortableVengeance.ttf", size)
    elif font == "debug":
        f = pygame.freetype.Font("./resources/fonts/standart.otf", size)
    # PortableVengeance by Pixel Kitchen on fontspace.com, Licensed as Public Domain
    # The dot (.) has been modified
    # px * .75 = pt (example: 8px is equivalent to 6pt)
    f.antialiased = antialiased
    f.vertical = vertical
    f.render_to(surf=window, dest=pos, text=text, fgcolor=color)


def get_text_rect(text, size=5, font="game"):
    if font == "game":
        f = pygame.freetype.Font("./resources/fonts/PortableVengeance.ttf", size)
    elif font == "debug":
        f = pygame.freetype.Font("./resources/fonts/standart.otf", size)
    return f.get_rect(text=text)


def gradient_rect(width, height, colors):
    color_rect = pygame.Surface((2, 2))
    pygame.draw.line(color_rect, colors[0], (0, 0), (0, 1))
    pygame.draw.line(color_rect, colors[1], (1, 0), (1, 1))
    color_rect = pygame.transform.smoothscale(color_rect, (width, height))
    return color_rect


def play_sound(sound):
    threshold = 10
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
    elif sound == 'alert':
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("./resources/sounds/hurt.wav"))
    elif sound == 'step':
        if pygame.mixer.Channel(3).get_busy() == False:
            num = random.randint(1, 5)
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("./resources/sounds/step" + str(num) + ".wav"))
            threshold = 20
    elif sound == 'explosion':
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("./resources/sounds/explosion.wav"))
    pygame.mixer.Channel(1).set_volume(get_setting('volume') / threshold)
    pygame.mixer.Channel(2).set_volume(get_setting('volume') / threshold)
    pygame.mixer.Channel(3).set_volume(get_setting('volume') / threshold)


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


def mp_screen():
    """
    returns mouse position relative to the screen
    (use for gui)
    """
    return (pygame.mouse.get_pos()[0] / (globs.res_size[0] / globs.SIZE[0]),
            pygame.mouse.get_pos()[1] / (globs.res_size[1] / globs.SIZE[1]))

def mp_scene(scene):
    """
    returns mouse position relative to the scene
    (use for game mechanics)
    """
    mp = mp_screen()
    return scene.camera.rect.centerx - globs.SIZE[0]/2 + mp[0], scene.camera.rect.centery - globs.SIZE[1]/2 + mp[1]

def set_anchor_point(rect, pos, anchor):
    if anchor == "midtop" or anchor == "mt":
        rect.midtop = pos
    elif anchor == "midbottom" or anchor == "mb":
        rect.midbottom = pos
    elif anchor == "midleft" or anchor == "ml":
        rect.midleft = pos
    elif anchor == "midright" or anchor == "mr":
        rect.midright = pos
    elif anchor == "topleft" or anchor == "tl":
        rect.topleft = pos
    elif anchor == "topright" or anchor == "tr":
        rect.topright = pos
    elif anchor == "bottomleft" or anchor == "bl":
        rect.bottomleft = pos
    elif anchor == "bottomright" or anchor == "br":
        rect.bottomright = pos
    elif anchor == "center" or anchor == "c":
        rect.center = pos

def dual_rect_anchor(rect1, rect2, anchor):
    if anchor == "midtop" or anchor == "mt":
        rect1.midtop = rect2.midtop
    elif anchor == "midbottom" or anchor == "mb":
        rect1.midbottom = rect2.midbottom
    elif anchor == "midleft" or anchor == "ml":
        rect1.midleft = rect2.midleft
    elif anchor == "midright" or anchor == "mr":
        rect1.midright = rect2.midright
    elif anchor == "topleft" or anchor == "tl":
        rect1.topleft = rect2.topleft
    elif anchor == "topright" or anchor == "tr":
        rect1.topright = rect2.topright
    elif anchor == "bottomleft" or anchor == "bl":
        rect1.bottomleft = rect2.bottomleft
    elif anchor == "bottomright" or anchor == "br":
        rect1.bottomright = rect2.bottomright
    elif anchor == "center" or anchor == "c":
        rect1.center = rect2.center

def draw_outline_mask(surface, img, loc, thickness=1, color=(255, 255, 255)):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n += 1
    pygame.draw.polygon(surface, color, mask_outline, thickness)

def get_outline_mask(img, thickness=1, color=(255, 255, 255)):
    surface = pygame.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA)
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0
    for point in mask_outline:
        mask_outline[n] = (point[0], point[1])
        n += 1
    pygame.draw.polygon(surface, color, mask_outline, thickness)
    return surface

def perfect_outline(surface, img, loc):
    mask = pygame.mask.from_surface(img)
    mask_surf = mask.to_surface()
    mask_surf.set_colorkey((0, 0, 0))
    surface.blit(mask_surf, (loc[0] - 1, loc[1]))
    surface.blit(mask_surf, (loc[0] + 1, loc[1]))
    surface.blit(mask_surf, (loc[0], loc[1] - 1))
    surface.blit(mask_surf, (loc[0], loc[1] + 1))

def perfect_outline_2(surface, img, loc):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    mask_surf = pygame.Surface(img.get_size())
    for pixel in mask_outline:
        mask_surf.set_at(pixel, (255, 255, 255))
    mask_surf.set_colorkey((0, 0, 0))
    surface.blit(mask_surf, (loc[0] - 1, loc[1]))
    surface.blit(mask_surf, (loc[0] + 1, loc[1]))
    surface.blit(mask_surf, (loc[0], loc[1] - 1))
    surface.blit(mask_surf, (loc[0], loc[1] + 1))