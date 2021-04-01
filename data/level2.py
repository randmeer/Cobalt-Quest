import pygame
import random
from data import player
from data import victim
from data import utils
from data import globals


def playLevel2(difficulty):
    print("LEVEL2 START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()

    background = utils.background()

    victim1 = pygame.sprite.Group()
    victim2 = pygame.sprite.Group()
    victim3 = pygame.sprite.Group()
    victim4 = pygame.sprite.Group()

    victim_all = pygame.sprite.Group()

    players = pygame.sprite.Group()
    playersprite = player.Player()
    players.add(playersprite)

    victimsprite1 = victim.Victim()
    victim1.add(victimsprite1)
    victimsprite2 = victim.Victim()
    victim2.add(victimsprite2)
    victimsprite3 = victim.Victim()
    victim3.add(victimsprite3)
    victimsprite4 = victim.Victim()
    victim4.add(victimsprite4)

    victim_all.add(victimsprite1)
    victim_all.add(victimsprite2)
    victim_all.add(victimsprite3)
    victim_all.add(victimsprite4)

    victimvelocity = difficulty

    victimSummonCooldown = 10
    victimCycler = 1

    run = True
    while run:

        # posX = pygame.mouse.get_pos()[0]
        # posY = pygame.mouse.get_pos()[1]

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
        else:
            victimSummonCooldown = 600 / (globals.difficulty * 2)
            position = random.randint(50, 450)
            if victimCycler == 1:
                victimCycler = 2
                globals.victimdirection1 = random.randint(1, 4)
                victimsprite1.summon(globals.victimdirection1, position)
            elif victimCycler == 2:
                victimCycler = 3
                globals.victimdirection2 = random.randint(1, 4)
                victimsprite2.summon(globals.victimdirection2, position)
            elif victimCycler == 3:
                victimCycler = 4
                globals.victimdirection3 = random.randint(1, 4)
                victimsprite3.summon(globals.victimdirection3, position)
            elif victimCycler == 4:
                victimCycler = 1
                globals.victimdirection4 = random.randint(1, 4)
                victimsprite4.summon(globals.victimdirection4, position)

        players.update(w, a, s, d, velocity)
        victim1.update(globals.victimdirection1, victimvelocity)
        victim2.update(globals.victimdirection2, victimvelocity)
        victim3.update(globals.victimdirection3, victimvelocity)
        victim4.update(globals.victimdirection4, victimvelocity)

        window.blit(background, (0, 0))
        victim_all.draw(window)
        players.draw(window)
        pygame.display.update()

        if globals.exittomenu:
            run = False
            globals.menu = True

    print("LEVEL2 END")
