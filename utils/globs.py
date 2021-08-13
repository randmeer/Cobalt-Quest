VERSION = "0.8.5"
DEFAULT_HEIGHT = 500
height = 500
width = 0

# VIDEO SETTINGS:
SIZE = (256, 144)
RES_16to9 = [((256, 144), "144p"),
             ((640, 360), "360p"),
             ((1280, 720), "720p HD"),
             ((1920, 1080), "1080p FullHD"),
             ((2560, 1440), "1440p WQHD"),
             ((3840, 2160), "2160p 4K UHD"),
             ((5120, 2880), "2880p Retina 5K"),
             ((7680, 4320), "4320p 8K UHD")]
RES_16to10 = [((320, 200), "-"),
              ((640, 400), "-"),
              ((800, 500), "-"),
              ((960, 600), "-"),
              ((1120, 700), "-"),
              ((1280, 800), "WXGA"),
              ((1440, 900), "WXGA+"),
              ((1680, 1050), "WSXGA+"),
              ((1920, 1200), "WUXGA"),
              ((2560, 1600), "WQXGA"),
              ((3840, 2400), "WQUXGA")]
RES_4to3 = [((160, 120), "QQVGA"),
            ((320, 240), "QVGA"),
            ((640, 480), "VGA"),
            ((800, 600), "SVGA"),
            ((1024, 768), "XGA"),
            ((1152, 864), "XGA+"),
            ((2048, 1536), "QXGA"),
            ((3200, 2400), "QUXGA"),
            ((4096, 3072), "HXGA"),
            ((6400, 4800), "HUXGA")]
res = RES_16to9[2]
res_size = res[0]
res_name = res[1]
fullscreen = False

# settings that reset on startup
# (plz dont change these the game will crash)
quitgame = exittomenu = titlescreen = menu = level_selection = rndebug = level1 = None
difficulty = 1

# variables for the numbers pygame assigns to the keys. If you change these,
# the keybinds change (so, dont)
LEFT, MIDDLE, RIGHT, WHEELUP, WHEELDOWN = 1, 2, 3, 4, 5
COMMAND = 1073742051
CONTROL = 1073742048
ALT = 1073742050
KEY_F4 = 1073741885
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# variables used for the gameplay
victimbreakcooldownmax = 0
victimhealthpointsmax = 32
playerhealthpoints = int(48 / difficulty)
victimspawns = victimskilled = victimsmissed = 0
damagecooldown = maxcooldown = 0

damageoverlayalpha = 64
tookdamage = False
damagesum = 0

skin = ''