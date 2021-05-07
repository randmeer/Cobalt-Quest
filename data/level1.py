import pygame
from data import utils, globals
from data.sprites import player, outline, sword, victim


def playLevel1():
    print("LEVEL1 START")

    # ------------------ SETUP ------------------
    utils.setGlobalDefaults()
    utils.setGameDefaults()
    window = utils.setupWindow()
    clock = pygame.time.Clock()
    background = utils.background()
    playersprite = player.Player()
    outlinesprite = outline.Outline()
    swordsprite = sword.Sword()
    victimgroup = pygame.sprite.Group()
    webgroup = pygame.sprite.Group()
    swordgroup = pygame.sprite.Group()
    swordgroup.add(swordsprite)

    victimSummonCooldown = 0
    victimcounter = 0

    damage_player = pygame.transform.scale(pygame.image.load("data/textures/damage_player.png"), (500, 500))

    gui_surface = pygame.Surface((500, 30), pygame.SRCALPHA, 32)
    gui_surface = gui_surface.convert_alpha()
    gui_surface.blit(pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18)), (10, 10))
    gui_surface.blit(pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20)), (100, 10))
    gui_surface.blit(pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18)), (190, 10))
    gui_surface.blit(pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18)), (280, 10))
    gui_surface.blit(pygame.transform.scale(pygame.image.load("data/textures/broken_heart.png"), (18, 18)), (370, 10))
    # ------------------ SETUP ------------------

    # ------------------ GAME LOOP --------------
    run = True
    while run:
        clock.tick(60)
        click = False

        # ------------------ EVENTS -------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    click = True
                    swordsprite.visibility = True
                if event.button == globals.RIGHT:
                    if globals.webs_left > 0:
                        utils.generateWeb(webgroup)
                        globals.webs_left -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    utils.showPauseScreen(window)
        # ------------------ EVENTS -------------------

        # ------------------ GAME LOGIC ---------------
        if victimSummonCooldown > 0:
            victimSummonCooldown = victimSummonCooldown - 1
        else:
            if victimcounter <= globals.victimspawns:
                victimSummonCooldown = 100 / (globals.difficulty * (globals.difficulty / 2))
                summonprogram = 'victim' + str(victimcounter) + ' = victim.Victim()\nvictimgroup.add(victim' + str(
                    victimcounter) + ')\nvictim' + str(victimcounter) + '.summon()'
                print(summonprogram)
                exec(summonprogram)
                victimcounter += 1

        if globals.damagecooldown < globals.maxcooldown:
            globals.damagecooldown += 1

        if globals.victimskilled == globals.victimspawns + 1:
            utils.showEndScreen(window, "victory")
        if globals.victimsmissed >= globals.victimspawns and globals.victimspawns - globals.victimsmissed - globals.victimskilled + 1 <= 0 or globals.playerhealthpoints < 1:
            utils.showEndScreen(window, "defeat")
        # ------------------ GAME LOGIC ---------------

        # ------------------ UPDATES ------------------
        victimgroup.update(player=playersprite, click=click, webgroup=webgroup)
        playersprite.update(webgroup=webgroup)
        swordgroup.update(posX=playersprite.rect.centerx, posY=playersprite.rect.centery)
        damage_player.set_alpha(256 - (globals.damagecooldown * 256 / globals.maxcooldown))
        # ------------------ UPDATES ------------------

        # ------------------ DRAWING ------------------
        window.blit(background, (0, 0))
        outlinesprite.draw(window)
        webgroup.draw(window)
        victimgroup.draw(window)
        playersprite.draw(window)
        if swordsprite.visibility:
            swordgroup.draw(window)
        window.blit(damage_player, (0, 0))
        window.blit(gui_surface, (0, 0))

        utils.renderIngameText(window)
        utils.renderText(window=window, text=str(round(clock.get_fps())) + " FPS", position=(20, 460),
                         color=globals.WHITE, size=24)
        pygame.display.update()
        # ------------------ DRAWING ------------------

        # ------------------ EVENTUAL EXIT ------------
        if globals.exittomenu:
            run = False
            globals.menu = True
        # ------------------ EVENTUAL EXIT ------------

    # ------------------ GAME LOOP --------------

    print("LEVEL1 END")
