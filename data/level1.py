import pygame
from data import utils, globals
from data.sprites import player, outline, victim


def playLevel1():
    print("LEVEL1 START")
    utils.setGlobalDefaults()
    utils.setGameDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()

    background = utils.background()
    playersprite = player.Player()
    outlinesprite = outline.Outline()

    victimgroup = pygame.sprite.Group()
    webgroup = pygame.sprite.Group()

    victimSummonCooldown = 0
    victimcounter = 0

    heart = pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18))
    keksi = pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20))
    tick = pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18))
    cross = pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18))
    broken_heart = pygame.transform.scale(pygame.image.load("data/textures/broken_heart.png"), (18, 18))
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
                if event.button == globals.RIGHT:
                    if globals.webs_left > 0:
                        utils.generateWeb(webgroup)
                        globals.webs_left -= 1
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
                # globals.victims[victimcounter].summon()
                # globals.on_screen[victimcounter] = True
                #victimgroup[victimcounter].summon()
                summonprogram = 'victim' + str(victimcounter) + ' = victim.Victim()\nvictimgroup.add(victim' + str(
                    victimcounter) + ')\nvictim' + str(victimcounter) + '.summon()'
                exec(summonprogram)
                victimcounter += 1

        window.blit(background, (0, 0))
        playersprite.update(w, a, s, d, velocity, webgroup)

        #utils.updateVictims(playersprite=playersprite, click=click, victimgroup=victimgroup)
        victimgroup.update(player=playersprite, click=click, damagecooldown=globals.damagecooldown, webgroup=webgroup)

        outlinesprite.draw(window)
        webgroup.draw(window)
        victimgroup.draw(window)
        playersprite.draw(window)

        damage_player.set_alpha(256 - (globals.damagecooldown * 256 / globals.maxcooldown))

        window.blit(damage_player, (0, 0))
        window.blit(heart, (10, 10))
        window.blit(keksi, (100, 10))
        window.blit(tick, (190, 10))
        window.blit(cross, (280, 10))
        window.blit(broken_heart, (370, 10))

        utils.renderIngameText(window)
        pygame.display.update()

        if globals.damagecooldown < globals.maxcooldown:
            globals.damagecooldown += 1

        if globals.victimskilled == globals.victimspawns + 1:
            utils.showEndScreen(window, "victory")
        if globals.victimsmissed >= globals.victimspawns and globals.victimspawns-globals.victimsmissed-globals.victimskilled + 1 <= 0  or globals.playerhealthpoints < 1:
            utils.showEndScreen(window, "defeat")

        if globals.exittomenu:
            run = False
            globals.menu = True

    print("LEVEL1 END")
