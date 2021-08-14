VERSION = "0.8.5"

# VIDEO SETTINGS:
SIZE = (256, 144)
SIZE_16TO9 = (256, 144)
SIZE_16TO10 = (230, 144)
SIZE_4TO3 = (192, 144)
RES_16TO9 = [((256, 144), "144p"),
             ((640, 360),    "360p  nHD"),
             ((854, 480),    "480p  ~"),  # not true 16:9, fuck 480p, but it's a YT stantart so i gotta include it
             ((960, 540),    "540p  qHD"),
             ((1280, 720),   "720p  HD"),
             ((1360, 765),   "765p  WXGA"),
             ((1600, 900),   "1600p HD+"),
             ((1920, 1080),  "1080p Full HD"),
             ((2048, 1152),  "1152p 2K"),
             ((2560, 1440),  "1440p QHD"),
             ((3072, 1728),  "1728p 3K"),
             ((3200, 1800),  "3200p QHD+"),
             ((3840, 2160),  "2160p 4K UHD"),
             ((4096, 2304),  "2304p DCI 4K"),
             ((5120, 2880),  "2880p 5K"),
             ((7680, 4320),  "4320p 8K UHD"),
             ((8192, 4608),  "4608p True 8K"),
             ((15360, 8640), "8640p 16K")]
RES_16TO10 = [((320, 200), "-"),
              ((640, 400),   "-"),
              ((800, 500),   "-"),
              ((960, 600),   "-"),
              ((1120, 700),  "-"),
              ((1280, 800),  "WXGA"),
              ((1440, 900),  "WXGA+"),
              ((1680, 1050), "WSXGA+"),
              ((1920, 1200), "WUXGA"),
              ((2560, 1600), "WQXGA"),
              ((3840, 2400), "WQUXGA"),
              ((8192, 5120), "8K ?")]
RES_4TO3 = [((160, 120), "QQVGA"),
            ((320, 240),   "QVGA"),
            ((640, 480),   "VGA"),
            ((800, 600),   "SVGA"),
            ((1024, 768),  "XGA"),
            ((1152, 864),  "XGA+"),
            ((2048, 1536), "QXGA"),
            ((3200, 2400), "QUXGA"),
            ((4096, 3072), "HXGA"),
            ((6400, 4800), "HUXGA")]
# following variables get set by the set_resolution function in utils
res = (0, 0)
res_size = 0
res_name = ""
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
