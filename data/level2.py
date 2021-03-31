import pygame
from data import player
from data import victim
from data import utils
from data import globals


def playLevel2(difficulty):
    print("LEVEL2 START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    playersprite = player.Player()
    all_sprites.add(playersprite)

    direction = 0
    velocity = 2

    w = False
    a = False
    s = False
    d = False

    run = True
    while run:

        posX = pygame.mouse.get_pos()[0]
        posY = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globals.LEFT:
                    # print("MENGA")
                    None
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

        all_sprites.update(w, a, s, d, velocity)
        window.fill(globals.BLACK)
        all_sprites.draw(window)
        pygame.display.update()

        if globals.exittomenu:
            run = False
            globals.menu = True
