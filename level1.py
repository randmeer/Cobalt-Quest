import math
import time
import pygame
import utils
import globs
from sprites import sword, player, outline, victim, web, gui, new_player, particle_cloud, shuriken, block
from utils import relToAbs, relToAbsDual, absToRelDual

damage_player_texture = pygame.image.load("textures/damage_player.png")
heart_img = pygame.image.load("textures/heart.png")
ichkeksi_img = pygame.image.load("textures/ichkeksi.png")
tick_img = pygame.image.load("textures/tick.png")
cross_img = pygame.image.load("textures/cross.png")
broken_heart_img = pygame.image.load("textures/broken_heart.png")
background_original = pygame.image.load("textures/background.png")
gui_background_original = pygame.image.load("textures/gui_background.png")

def playLevel1():
    print("LEVEL1 START")
    # ------------------ SETUP ------------------
    utils.setGlobalDefaults()
    utils.setGameDefaults()
    window = utils.setupWindow()
    background = pygame.transform.scale(background_original, (globs.height, globs.height))
    gui_background = pygame.transform.scale(gui_background_original, (globs.height, globs.height))
    playersprite = new_player.Player()
    outlinesprite = outline.Outline()
    swordsprite = sword.Sword()
    guisprite = gui.GUI()
    victimgroup = pygame.sprite.Group()
    webgroup = pygame.sprite.Group()
    blocks, victims, particleclouds, shurikens = [], [], [], []
    victim_summon_cooldown = victimcounter = 0

    #gui_surface_original = pygame.Surface((relToAbsDual(1, 0.06)), pygame.SRCALPHA, 32)
    #gui_surface_original = gui_surface_original.convert_alpha()
    #gui_surface_original.blit(pygame.transform.scale(heart_img, relToAbsDual(0.036, 0.036)), relToAbsDual(0.02, 0.02))
    #gui_surface_original.blit(pygame.transform.scale(ichkeksi_img, relToAbsDual(0.04, 0.04)), relToAbsDual(0.2, 0.02))
    #gui_surface_original.blit(pygame.transform.scale(tick_img, relToAbsDual(0.036, 0.036)), relToAbsDual(0.38, 0.02))
    #gui_surface_original.blit(pygame.transform.scale(cross_img, relToAbsDual(0.036, 0.036)), relToAbsDual(0.56, 0.02))
    #gui_surface_original.blit(pygame.transform.scale(broken_heart_img, relToAbsDual(0.036, 0.036)), relToAbsDual(0.74, 0.02))
    #gui_surface = gui_surface_original
    main_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
    gui_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
    damage_player = pygame.transform.scale(damage_player_texture, (relToAbsDual(1, 1)))

    prev_time = time.time()
    resizeupdate = False
    # ------------------ SETUP ------------------

    # ------------------ GAME LOOP -------------------------------------------------------------------------------------
    clock = pygame.time.Clock()
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
        mousepos = pygame.mouse.get_pos()

        # ------------------ EVENTS -------------------
        for event in pygame.event.get():
            # quitevent
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            # mousebutton event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left button
                if event.button == globs.LEFT:
                    if guisprite.items[guisprite.weapon][0] == "dagger":
                        click = True
                        swordsprite.visibility = True
                        swordsprite.animation = 1
                        particleclouds.append(particle_cloud.ParticleCloud(relcenter=absToRelDual(mousepos[0], mousepos[1]), relradius=0.06, relparticlesize=0.02, color=(230, 0, 0), density=10, relvelocity=1.5, distribution=0.5))
                    if guisprite.items[guisprite.weapon][0] == "shuriken" and guisprite.items[guisprite.weapon][1] > 0:
                        angle = math.atan2(mousepos[1]-playersprite.rect.centery, mousepos[0]-playersprite.rect.centerx)
                        shurikens.append(shuriken.Shuriken(relpos=absToRelDual(playersprite.rect.centerx, playersprite.rect.centery), radians=angle))
                        guisprite.items[guisprite.weapon][1] -= 1
                if event.button == globs.WHEELUP:
                    guisprite.weapon -= 1
                if event.button == globs.WHEELDOWN:
                    guisprite.weapon += 1
                # right button and spawn webs
                if event.button == globs.RIGHT:
                    # ToDo: bind the block type to the selection
                    blocks.append(block.Block(blocktype="web"))
            # keyevents
            if event.type == pygame.KEYDOWN:
                # pausekey
                if event.key == pygame.K_ESCAPE:
                    utils.showPauseScreen(window=window, mainsurf=main_surface)
                    resizeupdate = True
                    playersprite.update_skin()
                if event.key == pygame.K_e:
                    guisprite.weapon += 1
                if event.key == pygame.K_q:
                    guisprite.block += 1
                if event.key == pygame.K_1:
                    guisprite.weapon = 0
                elif event.key == pygame.K_2:
                    guisprite.weapon = 1
                elif event.key == pygame.K_3:
                    guisprite.weapon = 2
                elif event.key == pygame.K_4:
                    guisprite.weapon = 3
                elif event.key == pygame.K_5:
                    guisprite.weapon = 4
                guisprite.update()

                # SHURIKENS SHOULD EXPLODE WHEN HITTING ENTITYS OR BLOCKS, SPACE KEY IS JUST TEMPORARELY
                if event.key == pygame.K_SPACE:
                    for i in shurikens:
                        i.explode()

            # update screen on screenresize
            if event.type == pygame.VIDEORESIZE or resizeupdate:
                resizeupdate = False
                w, h = pygame.display.get_surface().get_size()
                utils.resizeWindow(w, h)
                main_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
                gui_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
                damage_player = pygame.transform.scale(damage_player_texture, (relToAbsDual(1, 1)))
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                gui_background = pygame.transform.scale(gui_background_original, (relToAbsDual(1, 1)))
                #gui_surface = pygame.transform.scale(gui_surface_original, (relToAbsDual(1, 0.06)))
                for i in victimgroup:
                    i.resize()
                for i in blocks:
                    i.resize()
                playersprite.update_skin()
                outlinesprite.resize()
                guisprite.resize()
                swordsprite.resize()
        # ------------------ EVENTS -------------------

        # ------------------ GAME LOGIC ---------------
        # subtract victim cooldown if possible else summon new victim to fight
        if victim_summon_cooldown > 0:
            victim_summon_cooldown = victim_summon_cooldown - 1
        else:
            if victimcounter <= globs.victimspawns:
                victim_summon_cooldown = 100 / (globs.difficulty * (globs.difficulty / 2))
                victims.append(victim.Victim())
                victimgroup.add(victims[victimcounter])
                victims[victimcounter].summon()
                victimcounter += 1

        # manage damagecooldown
        if globs.damagecooldown < globs.maxcooldown:
            globs.damagecooldown += 50 * delta_time

        # determin victory or defeat
        if globs.victimskilled == globs.victimspawns + 1:
            utils.showEndScreen(window=window, end="victory", mainsurf=main_surface)
            run = False
        elif globs.victimsmissed >= globs.victimspawns and globs.victimspawns - globs.victimsmissed - globs.\
                victimskilled + 1 <= 0 or globs.playerhealthpoints < 1:
            utils.showEndScreen(window=window, end="defeat", mainsurf=main_surface)
            run = False
        # ------------------ GAME LOGIC ---------------

        # ------------------ UPDATES ------------------
        victimgroup.update(player=playersprite, click=click, webgroup=webgroup, delta_time=delta_time)
        playersprite.update(webgroup=webgroup, main_surface=main_surface)
        swordsprite.update(playersprite=playersprite, delta_time=delta_time)
        #webgroup.update()
        guisprite.update()
        damage_player.set_alpha(256 - (globs.damagecooldown * 256 / globs.maxcooldown))
        # ------------------ UPDATES ------------------

        # ------------------ DRAWING ------------------
        main_surface.blit(background, (0, 0))
        gui_surface.blit(gui_background, relToAbsDual(0, 0))
        outlinesprite.draw(main_surface)
        for i in blocks:
            i.update(window=main_surface)
        victimgroup.draw(main_surface)
        for i in particleclouds:
            i.update(window=main_surface, delta_time=delta_time)
        for i in shurikens:
            i.update(delta_time=delta_time, window=main_surface)

        swordsprite.draw(main_surface)
        playersprite.draw(main_surface)
        guisprite.draw(gui_surface)
        main_surface.blit(damage_player, (0, 0))
        #main_surface.blit(gui_surface, (0, 0))
        #utils.renderIngameText(main_surface)
        #utils.renderText(window=main_surface, text=str(round(clock.get_fps())) + "",
        #                 position=relToAbsDual(0.92, 0.02),
        #                 color=globs.WHITE, size=relToAbs(0.048))
        window.blit(main_surface, (0, 0))
        window.blit(gui_surface, relToAbsDual(1, 0))
        pygame.display.update()
        # ------------------ DRAWING ------------------

        # ------------------ EVENTUAL EXIT ------------
        if globs.exittomenu:
            run = False
            globs.menu = True
        # ------------------ EVENTUAL EXIT ------------
    # ------------------ GAME LOOP -------------------------------------------------------------------------------------

    print("LEVEL1 END")
