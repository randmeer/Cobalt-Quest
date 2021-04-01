import pygame

from data import utils
from data import globals

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

    utils.playCurrentState()

    if globals.quitgame:
        run = False

    print("MAIN LOOP ROUND END")
    print(" ")

print(" ")
print("MAIN LOOP FULLY EXECUTED, PROGRAM END")