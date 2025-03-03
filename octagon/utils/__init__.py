import pygame
import pygame.freetype
import QuickJSON
import math
import random

from octagon.utils import var, static


settings = QuickJSON.QJSON("./data/settings.json")


def save_settings():
    settings.save()


def load_settings():
    settings.load()


def set_setting(setting, value):
    settings[setting] = value


def get_setting(setting):
    return settings[setting]


def set_resolution():
    # TODO: rework resolution handling
    aspect_ratio = get_setting('aspect_ratio')
    resolution = get_setting('resolution')
    fullscreen = get_setting('fullscreen')

    var.fullscreen = fullscreen
    if var.fullscreen:
        infos = pygame.display.Info()
        screen_size = (infos.current_w, infos.current_h)
        ar = static.simplify_fraction(screen_size[0], screen_size[1])
        ar_string = f"{ar[0]}to{ar[1]}"
        var.SIZE = var.DISPLAY[ar_string][0]
        var.res = (screen_size, 'Fullscreen')
        var.res_size = screen_size
        var.res_name = "Fullscreen"
    else:
        var.SIZE = var.DISPLAY[aspect_ratio][0]
        var.res = var.DISPLAY[aspect_ratio][1][resolution]
        var.res_size = var.res[0]
        var.res_name = var.res[1]


class DefaultError(Exception):
    def __init__(self, errmsg='unknown error has occured'):
        self.errmsg = errmsg
        Exception.__init__(self, errmsg)

    def __reduce__(self):
        return self.__class__, self.errmsg


def rta_width(input_value):
    output = var.SIZE[0] * input_value
    return round(output)


def atr_width(input_value):
    output = input_value / var.SIZE[0]
    return output


def rta_height(input_value):
    output = var.SIZE[1] * input_value
    return round(output)


def atr_height(input_value):
    output = input_value / var.SIZE[1]
    return output


def rta_dual(input_x, input_y):
    output_x, output_y = var.SIZE[0] * input_x, var.SIZE[1] * input_y
    return round(output_x), round(output_y)


def atr_dual(input_x, input_y):
    output_x, output_y = input_x / var.SIZE[0], input_y / var.SIZE[1]
    return output_x, output_y


def rta_dual_height(input_x, input_y):
    output_x, output_y = var.SIZE[1] * input_x, var.SIZE[1] * input_y
    return round(output_x), round(output_y)


def atr_dual_height(input_x, input_y):
    output_x, output_y = input_x / var.SIZE[1], input_y / var.SIZE[1]
    return output_x, output_y


def rta_dual_width(input_x, input_y):
    output_x, output_y = var.SIZE[0] * input_x, var.SIZE[0] * input_y
    return round(output_x), round(output_y)


def atr_dual_width(input_x, input_y):
    output_x, output_y = input_x / var.SIZE[0], input_y / var.SIZE[0]
    return output_x, output_y


def render_text(window, text, pos, color=var.WHITE, size=5, antialiased=False, vertical=False):
    f = pygame.freetype.Font("./resources/fonts/PixelQuest.ttf", size)
    f.antialiased = antialiased
    f.vertical = vertical
    f.render_to(surf=window, dest=pos, text=text, fgcolor=color)


def get_text_rect(text, size=5):
    f = pygame.freetype.Font("./resources/fonts/PixelQuest.ttf", size)
    return f.get_rect(text=text)


# https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
def render_multiline_text(surface, text, pos, linebreak=False, fadeout=None, color=(255, 255, 255)):
    if linebreak:
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    else:
        words = text.splitlines()
    # space = font.size(' ')[0]  # The width of a space.
    space = 5
    word_width, word_height = 5, 5
    max_width, max_height = surface.get_size()
    x, y = pos[0], pos[1]+5
    alpha = 255
    if fadeout == "up":
        alpha = 0
        # if it's down, it stays 255
    rendercolor = [color[0], color[1], color[2], alpha]
    for line in words:
        if fadeout == "up":
            rendercolor[3] += 255 / len(words)
        elif fadeout == "down":
            rendercolor[3] -= 255 / len(words)
        if linebreak:
            for word in line:
                bingorect = get_text_rect(word)
                word_width, word_height = bingorect.width, bingorect.height
                bingosurf = pygame.Surface((word_width, word_height), pygame.SRCALPHA)
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height + 2  # Start on new row.
                render_text(window=bingosurf, text=word, pos=(0, 0), color=rendercolor)
                bingorect.bottomleft = (x, y)
                surface.blit(bingosurf, bingorect)
                x += word_width + space
        else:
            render_text(window=surface, text=line, pos=(x, y), color=rendercolor)
        x = pos[0]  # Reset the x.
        y += word_height + 1  # Start on new row.


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
        if not pygame.mixer.Channel(3).get_busy():
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
    return (pygame.mouse.get_pos()[0] / (var.res_size[0] / var.SIZE[0]),
            pygame.mouse.get_pos()[1] / (var.res_size[1] / var.SIZE[1]))


def mp_scene(scene):
    """
    returns mouse position relative to the scene
    (use for game mechanics)
    """
    mp = mp_screen()
    return scene.camera.rect.centerx - var.SIZE[0] / 2 + mp[0], scene.camera.rect.centery - var.SIZE[1] / 2 + mp[1]


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


def debug_outlines(image, hitbox, rect, anchor="center"):
    rectcopy = pygame.Rect((0, 0), rect.size)
    hitboxcopy = pygame.Rect((0, 0), hitbox.size)
    dual_rect_anchor(hitboxcopy, rectcopy, anchor)
    img = image.copy()
    surf = pygame.Surface((hitbox.width, hitbox.height))
    surf.fill((0, 0, 0))
    hitoutlinesurf = get_outline_mask(surf, color=(255, 0, 0))
    surf = pygame.Surface((img.get_width(), img.get_height()))
    surf.fill((0, 0, 0))
    outlinesurf = get_outline_mask(surf, color=(255, 255, 255))
    img.blit(outlinesurf, (0, 0))
    # img.blit(hitoutlinesurf, (rect.width / 2 - hitbox.width / 2, rect.height / 2 - hitbox.height / 2))
    img.blit(hitoutlinesurf, hitboxcopy)
    return img


def mask_overlay(image, color=(255, 0, 0), opacity=64):
    image = image.copy()
    mask = pygame.mask.from_surface(image)
    surf = mask.to_surface(setcolor=color, unsetcolor=None)
    surf.set_alpha(opacity)
    image.blit(surf, (0, 0))
    return image


def block_to_cord(pos, image=None, center=False):
    if image is None:
        width, height = 16, 16
    else:
        width, height = image.get_width(), image.get_height()
    posx, posy = pos[0] * width, pos[1] * height
    # this converts the positions of the blocks.json from my system to something pygame can use
    if posx < 0 and posy < 0:
        pass
    elif posx > 0 and posy < 0:
        posx -= width
    elif posx > 0 and posy > 0:
        posx -= width
        posy -= height
    elif posx < 0 and posy > 0:
        posy -= height
    if center:
        return [posx + width / 2, posy + height / 2]
    else:
        return [posx, posy]


def cord_to_block(posx, posy, image=None):
    if image is None:
        width, height = 16, 16
    else:
        width, height = image.get_width(), image.get_height()
    pos = [math.floor(posx / width), math.floor(posy / height)]
    return pos


def cout(message):
    var.chat += message + "\n"


def load_console():
    f = open('./data/chat.txt', 'r')
    var.chat = f.read()
    f.close()


def save_console():
    f = open('./data/chat.txt', 'w')
    f.write(var.chat)
    f.close()


def scale(surface, factor):
    return pygame.transform.scale(surface, (surface.get_width()*factor, surface.get_height()*factor))
