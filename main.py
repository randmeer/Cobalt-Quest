import pygame

from data import utils, globals

utils.playTheme()
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
