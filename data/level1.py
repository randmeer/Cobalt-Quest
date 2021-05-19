import pygame
from data import utils, globals
from data.sprites import player, outline, sword, victim
from data.utils import relToAbsHeight
from data.utils import relToAbs
from data.utils import absToRel

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

    victimSummonCooldown = 0
    victimcounter = 0

    damage_player = pygame.transform.scale(pygame.image.load("data/textures/damage_player.png"), (500, 500))

    gui_surface_original = pygame.Surface((relToAbs(1, 0.06)), pygame.SRCALPHA, 32)
    gui_surface_original = gui_surface_original.convert_alpha()

    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/heart.png"), (18, 18)), (10, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/IchKeksi.png"), (20, 20)), (100, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/tick.png"), (18, 18)), (190, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/cross.png"), (18, 18)), (280, 10))
    gui_surface_original.blit(pygame.transform.scale(pygame.image.load("data/textures/broken_heart.png"), (18, 18)), (370, 10))

    gui_surface = gui_surface_original

    # ------------------ SETUP ------------------

    # ------------------ GAME LOOP --------------
    run = True
    while run:
        clock.tick(60)
        click = False

        main_surface = pygame.Surface(relToAbs(1, 1), pygame.SRCALPHA, 32)
        gui_surface = pygame.transform.scale(gui_surface_original, (relToAbs(1, 0.06)))
        background = pygame.transform.scale(background, (relToAbs(1, 1)))
        damage_player = pygame.transform.scale(damage_player, (relToAbs(1, 1)))

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
            if event.type == pygame.VIDEORESIZE:
                if event.w < 500 or event.h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((event.h, event.h), pygame.RESIZABLE)
                for i in victimgroup:
                    i.image = pygame.transform.scale(i.original_image, (relToAbs(0.1, 0.1)))
                playersprite.original_image = pygame.transform.scale(playersprite.original_original_image, (relToAbs(0.1, 0.1)))


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
                         position=relToAbs(0.04, 0.92),
                         color=globals.WHITE, size=relToAbsHeight(0.048))
        # new_main_surface = pygame.transform.scale(main_surface, pygame.display.get_surface().get_size())
        window.blit(main_surface, (0, 0))
        pygame.display.update()
        # ------------------ DRAWING ------------------

        # ------------------ EVENTUAL EXIT ------------
        if globals.exittomenu:
            run = False
            globals.menu = True
        # ------------------ EVENTUAL EXIT ------------

    # ------------------ GAME LOOP --------------

    print("LEVEL1 END")
