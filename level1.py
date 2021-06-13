import time

import pygame

import utils
import globals
from sprites import sword, player, outline, victim, web
from utils import relToAbs
from utils import relToAbsDual

damage_player_texture = pygame.image.load("textures/damage_player.png")

heart_img = pygame.image.load("textures/heart.png")
ichkeksi_img = pygame.image.load("textures/ichkeksi.png")
tick_img = pygame.image.load("textures/tick.png")
cross_img = pygame.image.load("textures/cross.png")
broken_heart_img = pygame.image.load("textures/broken_heart.png")

def playLevel1():
    webs = []
    victims = []
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

    gui_surface_original = pygame.Surface((relToAbsDual(1, 0.06)), pygame.SRCALPHA, 32)
    gui_surface_original = gui_surface_original.convert_alpha()

    gui_surface_original.blit(pygame.transform.scale(heart_img, (18, 18)), (10, 10))
    gui_surface_original.blit(pygame.transform.scale(ichkeksi_img, (20, 20)), (100, 10))
    gui_surface_original.blit(pygame.transform.scale(tick_img, (18, 18)), (190, 10))
    gui_surface_original.blit(pygame.transform.scale(cross_img, (18, 18)), (280, 10))
    gui_surface_original.blit(pygame.transform.scale(broken_heart_img, (18, 18)),(370, 10))

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
        if delta_time > 1:
            delta_time = 0.01
        prev_time = now
        # ------------------ TIME ---------------------

        click = False
        main_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
        gui_surface = pygame.transform.scale(gui_surface_original, (relToAbsDual(1, 0.06)))
        background = pygame.transform.scale(background, (relToAbsDual(1, 1)))
        damage_player = pygame.transform.scale(damage_player_texture, (relToAbsDual(1, 1)))

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
                        webs.append(utils.generateWeb(webgroup))
                        globals.webs_left -= 1
                    for i in webgroup:
                        i.image = pygame.transform.scale(web.web_texture, (relToAbsDual(0.1, 0.1)))
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

                victims.append(victim.Victim())
                victimgroup.add(victims[victimcounter])
                victims[victimcounter].summon()

                victimcounter += 1

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
