import pygame
import utils

ESCAPE = 27

Elia03_texture = pygame.image.load("textures/3lia03.png")
IchKeksi_texture = pygame.image.load("textures/IchKeksi.png")
damage_texture = pygame.image.load("textures/damage.png")
Outline_texture = pygame.image.load("textures/Outline.png")
Crosshair_texture = pygame.image.load("textures/Crosshair.png")
text_1 = pygame.image.load("textures/1.png")
text_2 = pygame.image.load("textures/2.png")
text_3 = pygame.image.load("textures/3.png")
background_texture = pygame.image.load("textures/background.png")
title_screen_texture = pygame.image.load("textures/title_screen.png")
menu_texture = pygame.image.load("textures/menu.png")
sword_1_texture = pygame.image.load("textures/sword_1.png")
sword_2_texture = pygame.image.load("textures/sword_2.png")
sword_3_texture = pygame.image.load("textures/sword_3.png")
sword_4_texture = pygame.image.load("textures/sword_4.png")
sword_5_texture = pygame.image.load("textures/sword_5.png")
sword_6_texture = pygame.image.load("textures/sword_6.png")
sword_7_texture = pygame.image.load("textures/sword_7.png")
sword_8_texture = pygame.image.load("textures/sword_8.png")
Web_texture = pygame.image.load("textures/Web.png")

# debugschreen?
def showRNDebug():
    window = utils.setupWindow()
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == ESCAPE:
                    run = False
        window.fill((0, 0, 0))
        window.blit(Elia03_texture, (0, 0))
        window.blit(IchKeksi_texture, (10, 0))
        window.blit(damage_texture, (20, 0))
        window.blit(Outline_texture, (30, 0))
        window.blit(Crosshair_texture, (40, 0))
        window.blit(text_1, (50, 0))
        window.blit(text_2, (60, 0))
        window.blit(text_3, (70, 0))
        window.blit(background_texture, (0, 10))
        window.blit(title_screen_texture, (100, 10))
        window.blit(menu_texture, (200, 10))
        window.blit(sword_1_texture, (0, 110))
        window.blit(sword_2_texture, (30, 110))
        window.blit(sword_3_texture, (60, 110))
        window.blit(sword_4_texture, (90, 110))
        window.blit(sword_5_texture, (120, 110))
        window.blit(sword_6_texture, (150, 110))
        window.blit(sword_7_texture, (180, 110))
        window.blit(sword_8_texture, (210, 110))
        window.blit(Web_texture, (0, 140))

        pygame.display.update()

# pygame.quit()
