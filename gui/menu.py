import pygame

from utils import globs, __init__
from Render.sprites import button
from utils.images import background_texture, logo_texture
from utils.__init__ import relToAbsDualHeight, relToAbsDualWidth

def showMenu():
    print("MENU START")
    __init__.setGlobalDefaults()
    window = __init__.setupWindow()

    buttongroup = pygame.sprite.Group()
    map_button = button.Button(relwidth=0.4375, relheight=0.15, textcontent="Map", relpos=(0.05, 0.44))
    shop_button = button.Button(relwidth=0.4375, relheight=0.15, textcontent="Shop", relpos=(0.5125, 0.44))
    inventory_button = button.Button(relwidth=0.6875, relheight=0.15, textcontent="Inventory", relpos=(0.05, 0.62))
    menga_button = button.Button(relwidth=0.1875, relheight=0.15, textcontent="?", relpos=(0.7625, 0.62))
    settings_button = button.Button(relwidth=0.6875, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    difficulty_button = button.Button(relwidth=0.1875, relheight=0.15, textcontent=f"{globs.difficulty}", relpos=(0.7625, 0.80))
    buttongroup.add(map_button, shop_button, inventory_button, menga_button, settings_button, difficulty_button)

    def resize():
        w, h = pygame.display.get_surface().get_size()
        __init__.resizeWindow(w, h)
        bg = pygame.transform.scale(background_texture, (globs.height, globs.height))
        # and the logo comes in the widespread and commonly used 45:17 aspect ratio (thank me later)
        logo = pygame.transform.scale(logo_texture, ((int((globs.height / 3.5) * 45 / 17)), int(globs.height / 3.5)))
        window.blit(bg, (0, 0))
        window.blit(bg, relToAbsDualHeight(1, 0))
        window.blit(logo, relToAbsDualWidth(0.05, 0.05))
    def draw():
        for i in buttongroup:
            i.update()
            i.draw(window=window)
        pygame.display.update()
    resize()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        if globs.quitgame:
            run = False
        mousepos = pygame.mouse.get_pos()
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
                    if map_button.rect.collidepoint(mousepos):
                        run = False
                        globs.level_selection = True
                    if difficulty_button.rect.collidepoint(mousepos):
                        if globs.difficulty < 3:
                            globs.difficulty += 1
                        else:
                            globs.difficulty = 1
                        difficulty_button.text = f"{globs.difficulty}"
                        __init__.playSound('click')
                    if settings_button.rect.collidepoint(mousepos):
                        __init__.settings(window=window, backgr=background_texture)
                        resize()
            # keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == globs.ESCAPE:
                    run = False
                    globs.titlescreen = True
            # resize event
            if event.type == pygame.VIDEORESIZE:
                resize()
            draw()
    __init__.playSound('click')
    print("MENU END")
