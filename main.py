import pygame, threading
from data import utils, globals

# def updateMusic():
#    pygame.mixer.init()
#
#    test = utils.getSetting('background_music')
#    while True:
#        if test != utils.getSetting('background_music'):
#            pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)
#        test = utils.getSetting('background_music')
#
#
# musicthread = threading.Thread(target=updateMusic, daemon=True)
#
# if utils.getSetting('background_music') == "true":
#    utils.playTheme()
#    pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)
#    musicthread.start()

if utils.getSetting('background_music'):
    utils.playTheme()
    pygame.mixer.music.set_volume(utils.getSetting('volume') / 10)

print(utils.getSetting('volume'))

utils.setGlobalDefaults()
globals.titlescreen = True
window = utils.setupWindow()
clock = pygame.time.Clock()

run = True
while run:
    print(" ")
    print("MAIN LOOP ROUND START")
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if globals.quitgame:
        run = False
        print("DETECTED ORDER TO QUIT GAME")

    else:
        utils.playCurrentState()

    print("MAIN LOOP ROUND END")
    print(" ")

print(" ")
print("MAIN LOOP FULLY EXECUTED, PROGRAM END")
