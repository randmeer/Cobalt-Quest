import pygame, random
from data.sprites import player, victim
from data import utils, globals


def playLevel1():
    print("LEVEL1 START")
    utils.setGlobalDefaults()
    utils.setGameDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()

    background = utils.background()
    playersprite = player.Player()
    victimgroup = pygame.sprite.Group()
    utils.generateDirections()
    utils.generateVictims(victimgroup)
    victimSummonCooldown = 0
    victimcounter = 0
    victimvelocity = globals.difficulty

    heart = pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18))
    keksi = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20))
    tick = pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18))
    cross = pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18))
    damage_player = pygame.transform.scale(pygame.image.load("data/textures/damage_player.png"), (500, 500))

    run = True
    while run:
        clock.tick(60)
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    click = True
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
            if victimcounter <= globals.victimspawns:
                victimSummonCooldown = 100 / (globals.difficulty * (globals.difficulty / 2))
                globals.victims[victimcounter].summon(globals.direction[victimcounter], victimcounter)
                globals.on_screen[victimcounter] = True
                victimcounter += 1

        window.blit(background, (0, 0))
        playersprite.update(w, a, s, d, velocity)
        utils.updateVictims(victimvelocity, playersprite, click)

        victimgroup.draw(window)
        playersprite.draw(window)

        damage_player.set_alpha((globals.maxcooldown * 256 / 100) - (globals.damagecooldown * 256 / 100))

        window.blit(damage_player, (0, 0))

        window.blit(heart, (10, 10))
        window.blit(keksi, (100, 10))
        window.blit(tick, (190, 10))
        window.blit(cross, (280, 10))

        utils.renderIngameText(window)
        pygame.display.update()

        if globals.damagecooldown < globals.maxcooldown:
            globals.damagecooldown += 1

        if globals.exittomenu:
            run = False
            globals.menu = True

    print("LEVEL1 END")
