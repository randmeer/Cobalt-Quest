import pygame
import random
from data.sprites import player, victim
from data import utils
from data import globals


def playLevel1(difficulty):

    print("LEVEL1 START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()
    globals.victimspawns = (16 * difficulty)

    background = utils.background()
    playersprite = player.Player()
    victimgroup = pygame.sprite.Group()
    utils.generateDirections()
    utils.generateVictims(victimgroup)

    victimSummonCooldown = 0
    victimcounter = 0
    victimvelocity = difficulty

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    None
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    utils.showPauseScreen(window)

        w = False
        a = False
        s = False
        d = False
        velocity = 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            velocity = velocity / 2
        if keys[pygame.K_w]:
            w = True
        if keys[pygame.K_a]:
            a = True
        if keys[pygame.K_s]:
            s = True
        if keys[pygame.K_d]:
            d = True

        if victimSummonCooldown > 0:
            victimSummonCooldown = victimSummonCooldown - 1
        elif not victimcounter == globals.victimspawns:
            victimSummonCooldown = 100 / (globals.difficulty * (globals.difficulty / 2))
            print("VICTIM SUMMONED")
            globals.victims[victimcounter].summon(globals.direction[victimcounter])
            victimcounter += 1

        window.blit(background, (0, 0))
        playersprite.update(w, a, s, d, velocity)
        utils.updateVictims(victimvelocity)

        victimgroup.draw(window)
        playersprite.draw(window)
        pygame.display.update()

        if globals.exittomenu:
            run = False
            globals.menu = True

    globals.direction = []
    globals.victims = []
    print("LEVEL1 END")
