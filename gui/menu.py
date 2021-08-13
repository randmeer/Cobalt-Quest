import pygame

import utils
from utils import globs, mousepos, setGlobalDefaults, setupWindow, playSound
from render.sprites import button
from utils.images import background_texture, logo_texture
from gui.overlay import settings

def showMenu():
    print("MENU START")
    setGlobalDefaults()
    window = setupWindow()

    buttongroup = pygame.sprite.Group()
    map_button = button.Button(relwidth=0.4375, relheight=0.15, textcontent="Map", relpos=(0.05, 0.44))
    shop_button = button.Button(relwidth=0.4375, relheight=0.15, textcontent="Shop", relpos=(0.5125, 0.44))
    inventory_button = button.Button(relwidth=0.6875, relheight=0.15, textcontent="Inventory", relpos=(0.05, 0.62))
    menga_button = button.Button(relwidth=0.1875, relheight=0.15, textcontent="?", relpos=(0.7625, 0.62))
    settings_button = button.Button(relwidth=0.6875, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    difficulty_button = button.Button(relwidth=0.1875, relheight=0.15, textcontent=f"{globs.difficulty}", relpos=(0.7625, 0.80))
    buttongroup.add(map_button, shop_button, inventory_button, menga_button, settings_button, difficulty_button)

    def draw():
        og_surface = pygame.Surface(globs.SIZE)
        og_surface.blit(background_texture, (0, 0))
        og_surface.blit(logo_texture, (og_surface.get_width()/4-logo_texture.get_width()/2, og_surface.get_height()/4-logo_texture.get_height()/2))
        for i in buttongroup:
            i.update()
            i.draw(window=og_surface)
        surface = pygame.transform.scale(og_surface, globs.res_size)
        window.blit(surface, (0, 0))
        pygame.display.update()
    draw()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        if globs.quitgame:
            run = False
        mp = mousepos()
        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left button event
                if event.button == globs.LEFT:
                    if map_button.rect.collidepoint(mp):
                        run = False
                        globs.level_selection = True
                    if difficulty_button.rect.collidepoint(mp):
                        if globs.difficulty < 3:
                            globs.difficulty += 1
                        else:
                            globs.difficulty = 1
                        difficulty_button.text = f"{globs.difficulty}"
                        playSound('click')
                    if settings_button.rect.collidepoint(mp):
                        settings(window=window, background=background_texture)
                        #resize()
            # keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.titlescreen = True
            # resize event
            #if event.type == pygame.VIDEORESIZE:
            #    resize()
        draw()
    playSound('click')
    print("MENU END")
