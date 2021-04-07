# settings that reset on startup
# (plz dont change these the game will crash)
quitgame = None
exittomenu = None

titlescreen = None
menu = None
level_selection = None
rndebug = None
level1 = None


difficulty = 1

# variables for the numbers pygame assigns to the keys. If you change these,
# the keybinds change (so, dont)

LEFT = 1
MIDDLE = 2
RIGHT = 3

ESCAPE = 27
KEY_R = 114
KEY_Q = 113
COMMAND = 1073742051
CONTROL = 1073742048
ALT = 1073742050
KEY_F4 = 1073741885

WIDTH = 500
HEIGHT = 500

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# variables used for the gameplay

direction = []
victims = []
victimhealth = []
on_screen = []

victimhealthpoints = 32
playerhealthpoints = int(48 / difficulty)
victimspawns = 0
victimskilled = 0
victimsmissed = 0

damagecooldown = 0
maxcooldown = 0

damageoverlayalpha = 64
tookdamage = False
damagesum = 0

webs_left = 3
webcounter = 0
