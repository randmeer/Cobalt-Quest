import pygame
from data import utils

ESCAPE = 27

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
        window.blit(pygame.image.load("data/textures/3lia03.png"), (0, 0))
        window.blit(pygame.image.load("data/textures/IchKeksi.png"), (10, 0))
        window.blit(pygame.image.load("data/textures/damage.png"), (20, 0))
        window.blit(pygame.image.load("data/textures/Outline.png"), (30, 0))
        window.blit(pygame.image.load("data/textures/Crosshair.png"), (40, 0))
        window.blit(pygame.image.load("data/textures/1.png"), (50, 0))
        window.blit(pygame.image.load("data/textures/2.png"), (60, 0))
        window.blit(pygame.image.load("data/textures/3.png"), (70, 0))
        window.blit(pygame.image.load("data/textures/background.png"), (0, 10))
        window.blit(pygame.image.load("data/textures/title_screen.png"), (100, 10))
        window.blit(pygame.image.load("data/textures/menu.png"), (200, 10))
        window.blit(pygame.image.load("data/textures/sword_1.png"), (0, 110))
        window.blit(pygame.image.load("data/textures/sword_2.png"), (30, 110))
        window.blit(pygame.image.load("data/textures/sword_3.png"), (60, 110))
        window.blit(pygame.image.load("data/textures/sword_4.png"), (90, 110))
        window.blit(pygame.image.load("data/textures/sword_5.png"), (120, 110))
        window.blit(pygame.image.load("data/textures/sword_6.png"), (150, 110))
        window.blit(pygame.image.load("data/textures/sword_7.png"), (180, 110))
        window.blit(pygame.image.load("data/textures/sword_8.png"), (210, 110))
        window.blit(pygame.image.load("data/textures/Web.png"), (0, 140))

        pygame.display.update()

# pygame.quit()
