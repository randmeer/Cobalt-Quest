import pygame
import utils
import globals
from sprites import button, label
from utils import relToAbs
from utils import relToAbsDual
from utils import renderText
from utils import getTextRect

background_original = pygame.image.load("textures/background.png")
menu_original = pygame.image.load("textures/menu.png")

def showMenu():
    print("MENU START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()

    background = pygame.transform.scale(background_original, (globals.windowsize, globals.windowsize))
    menu = pygame.transform.scale(menu_original, (globals.windowsize, globals.windowsize))

    buttongroup = pygame.sprite.Group()
    levelselection_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="level selection", relpos=(0.05, 0.44))
    difficulty_button = button.Button(relwidth=0.9, relheight=0.15, textcontent=f" difficulty: {globals.difficulty}", relpos=(0.05, 0.62))
    settings_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="settings", relpos=(0.05, 0.80))
    buttongroup.add(levelselection_button, difficulty_button, settings_button)

    labelgroup = pygame.sprite.Group()
    line1_label = label.Label(text='"Invincibility lies in defence;', anchor="center", reltextsize=0.06, relanchorpointposition=(0.5, 0.32))
    line2_label = label.Label(text='Victory in the attack."', anchor="center", reltextsize=0.06, relanchorpointposition=(0.5, 0.38))
    labelgroup.add(line1_label, line2_label)
    # btw that quote is from sun tzu

    # draw window
    window.blit(background, (0, 0))
    window.blit(menu, (0, 0))
    for i in buttongroup:
        i.update()
        i.draw(window=window)
    for i in labelgroup:
        i.update()
        i.draw(window=window)

    pygame.display.update()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)

        if globals.quitgame:
            run = False
        mousepos = pygame.mouse.get_pos()

        # event iteration
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                run = False
                globals.quitgame = True
            # mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left button event
                if event.button == globals.LEFT:
                    if levelselection_button.rect.collidepoint(mousepos):
                        run = False
                        globals.level_selection = True
                    if difficulty_button.rect.collidepoint(mousepos):
                        if globals.difficulty < 3:
                            globals.difficulty += 1
                        else:
                            globals.difficulty = 1
                        print(globals.difficulty)
                        difficulty_button.text = f" difficulty: {globals.difficulty}"
                        difficulty_button.update()
                        difficulty_button.draw(window=window)
                        pygame.display.update()
                        utils.playSound('click')
                    if settings_button.rect.collidepoint(mousepos):
                        utils.showSettings(window=window)
                        window.blit(background, (0, 0))
                        window.blit(menu, (0, 0))
                        for i in buttongroup:
                            i.draw(window=window)
                        for i in labelgroup:
                            i.update()
                            i.draw(window=window)
                        pygame.display.update()
            # keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == globals.ESCAPE:
                    run = False
                    globals.titlescreen = True
            # resize event
            if event.type == pygame.VIDEORESIZE:
                w, h = pygame.display.get_surface().get_size()
                if w < 500 or h < 500:
                    pygame.display.set_mode((500, 500), pygame.RESIZABLE)
                else:
                    pygame.display.set_mode((h, h), pygame.RESIZABLE)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                menu = pygame.transform.scale(menu_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(menu, (0, 0))
                for i in buttongroup:
                    i.update()
                    i.draw(window=window)
                for i in labelgroup:
                    i.update()
                    i.draw(window=window)
                pygame.display.update()
                globals.windowsize = h

    utils.playSound('click')
    print("MENU END")
