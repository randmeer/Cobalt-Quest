import time

import pygame

from data import utils, globals
from data.sprites import player, outline, sword
from data.utils import relToAbs
from data.utils import relToAbsDual

def playLevel1():
    print("LEVEL1 START")
    # pygame.mouse.set_visible(False)
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

    victim_summon_cooldown = 0
    victimcounter = 0

    damage_player = pygame.transform.scale(pygame.image.load("data/textures/damage_player.png"), (500, 500))

    gui_surface_original = pygame.Surface((relToAbsDual(1, 0.06)), pygame.SRCALPHA, 32)
    gui_surface_original = gui_surface_original.convert_alpha()

    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18)), (10, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20)),
                              (100, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18)), (190, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18)), (280, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/broken_heart.png"), (18, 18)),
                              (370, 10))

    prev_time = time.time()

    resizeupdate = False
    # ------------------ SETUP ------------------

    # ------------------ GAME LOOP -------------------------------------------------------------------------------------
    run = True
    while run:
        # ------------------ TIME ---------------------
        clock.tick(60)
        now = time.time()
        delta_time = now - prev_time
        prev_time = now
        # ------------------ TIME ---------------------

        click = False
        main_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
        gui_surface = pygame.transform.scale(gui_surface_original, (relToAbsDual(1, 0.06)))
        background = pygame.transform.scale(background, (relToAbsDual(1, 1)))
        damage_player = pygame.transform.scale(damage_player, (relToAbsDual(1, 1)))

        # ------------------ EVENTS -------------------
        for event in pygame.event.get():
            # quitevent
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            # mousebutton event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left button
                if event.button == globals.LEFT:
                    click = True
                    swordsprite.visibility = True
                # right button and spawn webs
                if event.button == globals.RIGHT:
                    if globals.webs_left > 0:
                        utils.generateWeb(webgroup)
                        globals.webs_left -= 1
                    for i in webgroup:
                        i.image = pygame.transform.scale(i.original_image, (relToAbsDual(0.1, 0.1)))
                        i.rect = i.image.get_rect()
            # keyevents
            if event.type == pygame.KEYDOWN:
                # pausekey
                if event.key == globals.ESCAPE:
                    utils.showPauseScreen(window)
                    resizeupdate = True
            # update screen on screenresize
            if event.type == pygame.VIDEORESIZE or resizeupdate:
                resizeupdate = False
                w, h = pygame.display.get_surface().get_size()
                if w < 500 or h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((h, h), pygame.RESIZABLE)
                for i in victimgroup:
                    i.image = pygame.transform.scale(i.original_image, (relToAbsDual(0.1, 0.1)))
                    i.rect = i.image.get_rect()
                playersprite.original_image = pygame.transform.scale(playersprite.original_original_image,
                                                                     (relToAbsDual(0.1, 0.1)))
                for i in webgroup:
                    i.image = pygame.transform.scale(i.original_image, (relToAbsDual(0.1, 0.1)))
                    i.rect = i.image.get_rect()
                outlinesprite.image = pygame.transform.scale(outlinesprite.original_image, (relToAbsDual(0.1, 0.1)))
        # ------------------ EVENTS -------------------

        # ------------------ GAME LOGIC ---------------
        # subtract victim cooldown if possible else summon new victim to fight
        if victim_summon_cooldown > 0:
            victim_summon_cooldown = victim_summon_cooldown - 1
        else:
            if victimcounter <= globals.victimspawns:
                victim_summon_cooldown = 100 / (globals.difficulty * (globals.difficulty / 2))
                # WHY THE FUCK ARE YOU USING A EXEC COMMAND
                # JUST CONSTRUCT A FUCKLING VICTIM OBJECT WITH A METHOD INSIDE THE VICTIM CLASS
                summonprogram = 'victim' + str(victimcounter) + ' = victim.Victim()\nvictimgroup.add(victim' + str(
                    victimcounter) + ')\nvictim' + str(victimcounter) + '.summon()'
                print(summonprogram)
                exec(summonprogram)
                victimcounter += 50 * delta_time

        # manage damagecooldown
        if globals.damagecooldown < globals.maxcooldown:
            globals.damagecooldown += 50 * delta_time

        # determin victory or defeat
        if globals.victimskilled == globals.victimspawns + 1:
            utils.showEndScreen(window, "victory")
        elif globals.victimsmissed >= globals.victimspawns and globals.victimspawns - globals.victimsmissed - globals.\
                victimskilled + 1 <= 0 or globals.playerhealthpoints < 1:
            utils.showEndScreen(window, "defeat")
        # ------------------ GAME LOGIC ---------------

        # ------------------ UPDATES ------------------
        victimgroup.update(player=playersprite, click=click, webgroup=webgroup, delta_time=delta_time)
        playersprite.update(webgroup=webgroup, delta_time=delta_time)
        swordgroup.update(posX=playersprite.rect.centerx, posY=playersprite.rect.centery)
        webgroup.update()
        damage_player.set_alpha(256 - (globals.damagecooldown * 256 / globals.maxcooldown))
        # ------------------ UPDATES ------------------

        # ------------------ DRAWING ------------------
        main_surface.blit(background, (0, 0))
        outlinesprite.draw(main_surface)
        webgroup.draw(main_surface)
        victimgroup.draw(main_surface)
        if swordsprite.visibility:
            swordgroup.draw(main_surface)
        playersprite.draw(main_surface)
        main_surface.blit(damage_player, (0, 0))
        main_surface.blit(gui_surface, (0, 0))

        utils.renderIngameText(main_surface)
        utils.renderText(window=main_surface, text=str(round(clock.get_fps())) + " FPS",
                         position=relToAbsDual(0.04, 0.92),
                         color=globals.WHITE, size=relToAbs(0.048))
        # new_main_surface = pygame.transform.scale(main_surface, pygame.display.get_surface().get_size())
        window.blit(main_surface, (0, 0))
        pygame.display.update()
        # ------------------ DRAWING ------------------

        # ------------------ EVENTUAL EXIT ------------
        if globals.exittomenu:
            run = False
            globals.menu = True
        # ------------------ EVENTUAL EXIT ------------

    # ------------------ GAME LOOP -------------------------------------------------------------------------------------

    print("LEVEL1 END")
