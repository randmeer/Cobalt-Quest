import pygame, random
from data.sprites import player, victim
from data import utils, globals


def playLevel1(difficulty):
    print("LEVEL1 START")
    utils.setGlobalDefaults()
    utils.setGameDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()
    globals.victimspawns = (15 * difficulty + difficulty - 1)

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

                print("")
                print("VICTIM SUMMONED")
                print(victimcounter)
                print("on screen: " + str(globals.on_screen[victimcounter]))
                print("direction: " + str(globals.direction[victimcounter]))
                print("victimspawns: " + str(globals.victimspawns))
                victimcounter += 1

        #print(victimSummonCooldown)
        window.blit(background, (0, 0))
        playersprite.update(w, a, s, d, velocity)
        utils.updateVictims(victimvelocity, playersprite, click)

        victimgroup.draw(window)
        playersprite.draw(window)

        heart = pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18))
        window.blit(heart, (10, 10))
        keksi = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20))
        window.blit(keksi, (100, 10))
        tick = pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18))
        window.blit(tick, (190, 10))
        cross = pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18))
        window.blit(cross, (280, 10))
        utils.renderText(window, str(globals.playerhealthpoints), (35, 10), globals.WHITE, 24)
        utils.renderText(window, str((sum(i > 0 for i in globals.victimhealth))), (127, 10), globals.WHITE, 24)
        #utils.renderText(window, str(sum(globals.on_screen)), (127, 10), globals.WHITE, 24)

        utils.renderText(window, str(globals.victimskilled), (215, 10), globals.WHITE, 24)
        utils.renderText(window, str(globals.victimsmissed), (305, 10), globals.WHITE, 24)

        pygame.display.update()

        if globals.exittomenu:
            run = False
            globals.menu = True


    print("LEVEL1 END")
