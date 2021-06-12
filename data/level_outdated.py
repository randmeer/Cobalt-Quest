import pygame
import random
from data import utils
from data import globals

# NOT USED INGAME
def playLevelOutdated(difficulty):
    pygame.init()

    window = pygame.display.set_mode((500, 500))

    pygame.display.set_caption("WWOPW version 0.5 by Rande")

    pygame.display.flip()

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    ESCAPE = 27

    playerX = 50
    playerY = 50
    playerWidth = 50
    playerHeight = 50
    playerVelocity = 2
    usedPlayerVelocity = 0
    playercenterX = 0
    playercenterY = 0

    victim1SpawnCounter = 400
    victimVelocity = 1
    victim1_X = -100
    victim1_Y = -100
    victim1_Width = 50
    victim1_Height = 50
    victim1_Direction = 0
    victim1_isOnScreen = False
    victim1_isTrapped = False
    victim1_VelocityLimiter = False
    victim1_alive_counter = 600
    victim1_health = 32
    victim1centerX = 0
    victim1centerY = 0

    outlineposX = 0
    outlineposY = 0

    hitX = 0
    hitY = 0

    elia_original = pygame.image.load("data/textures/3lia03.png")
    # elia_rect = elia_original.get_rect()

    keksi_original = pygame.image.load("data/textures/IchKeksi.png")
    # keksi_rect = keksi_original.get_rect()

    web_original = pygame.image.load("data/textures/web.png")

    elia = pygame.transform.scale(elia_original, (50, 50))
    keksi = pygame.transform.scale(keksi_original, (50, 50))

    web1 = pygame.transform.scale(web_original, (48, 48))
    web2 = pygame.transform.scale(web_original, (48, 48))
    web3 = pygame.transform.scale(web_original, (48, 48))

    web1_X = -400
    web1_Y = -400
    web1_onScreen = False

    web2_X = -400
    web2_Y = -400
    web2_onScreen = False

    web3_X = -400
    web3_Y = -400
    web3_onScreen = False

    selection = False

    crosshair_original = pygame.image.load("data/textures/Crosshair.png")
    crosshair = pygame.transform.scale(crosshair_original, (10, 10))

    number_1_original = pygame.image.load("data/textures/1.png")
    number_2_original = pygame.image.load("data/textures/2.png")
    number_3_original = pygame.image.load("data/textures/3.png")

    number_1 = pygame.transform.scale(number_1_original, (10, 10))
    number_2 = pygame.transform.scale(number_2_original, (10, 10))
    number_3 = pygame.transform.scale(number_1_original, (10, 10))

    outline_original = pygame.image.load("data/textures/Outline.png")
    outline = pygame.transform.scale(outline_original, (50, 50))

    sword1_original = pygame.image.load("data/textures/sword_1.png")
    sword1 = pygame.transform.scale(sword1_original, (150, 150))
    sword2_original = pygame.image.load("data/textures/sword_2.png")
    sword2 = pygame.transform.scale(sword2_original, (150, 150))
    sword3_original = pygame.image.load("data/textures/sword_3.png")
    sword3 = pygame.transform.scale(sword3_original, (150, 150))
    sword4_original = pygame.image.load("data/textures/sword_4.png")
    sword4 = pygame.transform.scale(sword4_original, (150, 150))
    sword5_original = pygame.image.load("data/textures/sword_5.png")
    sword5 = pygame.transform.scale(sword5_original, (150, 150))
    sword6_original = pygame.image.load("data/textures/sword_6.png")
    sword6 = pygame.transform.scale(sword6_original, (150, 150))
    sword7_original = pygame.image.load("data/textures/sword_7.png")
    sword7 = pygame.transform.scale(sword7_original, (150, 150))
    sword8_original = pygame.image.load("data/textures/sword_8.png")
    sword8 = pygame.transform.scale(sword8_original, (150, 150))

    currentHitFrame = 0
    hitAnimationOngoing = False
    mousepressCooldown = 0
    cobwebcooldown = 0

    damage_original = pygame.image.load("data/textures/damage.png")
    damage = pygame.transform.scale(damage_original, (50, 50))

    # pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    # pygame.mouse.set_visible(False)

    playerVictory = True

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == RIGHT:
                    utils.playBlockPlace()
                    web1_onScreen = True
                    web1_X = outlineposX
                    web1_Y = outlineposY
                if event.button == LEFT:
                    # if mousepressCooldown == 0:
                    # if not hitAnimationOngoing:
                    if victim1centerX - hitX in range(-25, 25) and victim1centerY - hitY in range(-25, 25):
                        if playercenterX - hitX in range(-75, 75) and playercenterY - hitY in range(-75, 75):
                            hitAnimationOngoing = True
                            # utils.playSwing()
                            utils.playHit()
                            currentHitFrame = 1
                            mousepressCooldown = 50
                            victim1_health = victim1_health - 1
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE:
                    utils.showPauseScreen(window)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            usedPlayerVelocity = playerVelocity / 2
        else:
            usedPlayerVelocity = playerVelocity

        if keys[pygame.K_w] and playerY > usedPlayerVelocity:
            playerY -= usedPlayerVelocity
        if keys[pygame.K_a] and playerX > usedPlayerVelocity:
            playerX -= usedPlayerVelocity
        if keys[pygame.K_s] and playerY < 500 - playerHeight:
            playerY += usedPlayerVelocity
        if keys[pygame.K_d] and playerX < 500 - playerWidth:
            playerX += usedPlayerVelocity

        # if keys[pygame.K_ESCAPE]:
        #    run = False
        #
        #    if pygame.mouse.get_pos() == (100, 100):
        #        selection = True

        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed(3)

        window.fill((0, 0, 0))

        numberposX = pygame.mouse.get_pos()[0] + 20
        numberposY = pygame.mouse.get_pos()[1] + 20

        # outlineposX = round(pygame.mouse.get_pos()[0], 1)
        # outlineposY = round(pygame.mouse.get_pos()[1], 1)
        outlineposX = round((pygame.mouse.get_pos()[0] - 25) / 50) * 50
        outlineposY = round((pygame.mouse.get_pos()[1] - 25) / 50) * 50

        window.blit(outline, (outlineposX, outlineposY))

        # if pressed3:
        #    if outlineposX != web1_X and outlineposY != web1_Y:
        #        utils.playBlockPlace()
        #        #cobwebcooldown = 100
        #    web1_onScreen = True
        #    web1_X = outlineposX
        #    web1_Y = outlineposY

        if victim1_isOnScreen:
            if not victim1_isTrapped:
                if victim1_Direction == 1:
                    victim1_Y = victim1_Y + victimVelocity
                    victim1_alive_counter = victim1_alive_counter + 1
                if victim1_Direction == 2:
                    victim1_X = victim1_X - victimVelocity
                    victim1_alive_counter = victim1_alive_counter + 1
                if victim1_Direction == 3:
                    victim1_Y = victim1_Y - victimVelocity
                    victim1_alive_counter = victim1_alive_counter + 1
                if victim1_Direction == 4:
                    victim1_X = victim1_X + victimVelocity
                    victim1_alive_counter = victim1_alive_counter + 1

        victim1centerX = victim1_X + 25
        victim1centerY = victim1_Y + 25

        playercenterX = playerX + 25
        playercenterY = playerY + 25

        web1centerX = web1_X + 25
        web1centerY = web1_Y + 25

        if (victim1centerX - web1centerX in range(-30, 30)) and (victim1centerY - web1centerY in range(-30, 30)):
            victim1_isTrapped = True
        else:
            victim1_isTrapped = False

        if victim1SpawnCounter > 600 and not victim1_isTrapped and victim1_alive_counter > 550 or victim1_health < 0:
            direction = random.randint(1, 4)
            position = random.randint(50, 450)
            victim1_Direction = direction

            if victim1_Direction == 1:
                victim1_X = position
                victim1_Y = -10
            victim1_isOnScreen = True
            victim1SpawnCounter = 0
            if victim1_Direction == 2:
                victim1_Y = position
                victim1_X = 550
            victim1_isOnScreen = True
            victim1SpawnCounter = 0
            if victim1_Direction == 3:
                victim1_X = position
                victim1_Y = 550
            victim1_isOnScreen = True
            victim1SpawnCounter = 0
            if victim1_Direction == 4:
                victim1_Y = position
                victim1_X = -10
            victim1_isOnScreen = True
            victim1SpawnCounter = 0
            victim1_alive_counter = 0
            victim1_health = 32

        hitX = pygame.mouse.get_pos()[0]
        hitY = pygame.mouse.get_pos()[1]

        hitPosX = playerX - 50
        hitPosY = playerY - 50

        # if pressed1:
        #    if mousepressCooldown == 0:
        #        if not hitAnimationOngoing:
        #            if victim1centerX - hitX in range(-25, 25) and victim1centerY - hitY in range(-25, 25):
        #                if playercenterX - hitX in range(-75, 75) and playercenterY - hitY in range(-75, 75):
        #                    hitAnimationOngoing = True
        #                    #utils.playSwing()
        #                    utils.playHit()
        #                    currentHitFrame = 1
        #                    mousepressCooldown = 50
        #                    victim1_health = victim1_health - 1

        if not pressed1:
            mousepressCooldown = 0

        if hitAnimationOngoing:
            if currentHitFrame == 1:
                window.blit(sword1, (hitPosX, hitPosY))
            if currentHitFrame == 2:
                window.blit(sword2, (hitPosX, hitPosY))
            if currentHitFrame == 3:
                window.blit(sword3, (hitPosX, hitPosY))
            if currentHitFrame == 4:
                window.blit(sword4, (hitPosX, hitPosY))
            if currentHitFrame == 5:
                window.blit(sword5, (hitPosX, hitPosY))
            if currentHitFrame == 6:
                window.blit(sword6, (hitPosX, hitPosY))
            if currentHitFrame == 7:
                window.blit(sword7, (hitPosX, hitPosY))
            if currentHitFrame == 8:
                window.blit(sword8, (hitPosX, hitPosY))
                hitAnimationOngoing = False
                currentHitFrame = 0
            currentHitFrame = currentHitFrame + 1

        window.blit(web1, (web1_X, web1_Y))
        window.blit(web2, (web2_X, web2_Y))
        window.blit(web3, (web3_X, web3_Y))

        window.blit(keksi, (victim1_X, victim1_Y))

        if hitAnimationOngoing:
            window.blit(damage, (victim1_X, victim1_Y))
        window.blit(elia, (playerX, playerY))

        window.blit(number_1, (numberposX, numberposY))

        pygame.display.update()

        victim1SpawnCounter = victim1SpawnCounter + 1

        if mousepressCooldown > 0:
            mousepressCooldown = mousepressCooldown - 1
        if cobwebcooldown > 0:
            cobwebcooldown = cobwebcooldown - 1

        if globals.exittomenu:
            run = False
