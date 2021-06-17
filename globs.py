VERSION = "0.8.3"
windowsize = 500

# settings that reset on startup
# (plz dont change these the game will crash)
quitgame = exittomenu = titlescreen = menu = level_selection = rndebug = level1 = None
difficulty = 1

# variables for the numbers pygame assigns to the keys. If you change these,
# the keybinds change (so, dont)
LEFT, MIDDLE, RIGHT = 1, 2, 3
ESCAPE = 27
KEY_R = 114
KEY_Q = 113
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

webs_left = 3
webcounter = 0

skin = ''
