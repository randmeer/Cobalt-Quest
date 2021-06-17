import pygame
import utils
import globs
from sprites import button, label
from utils import relToAbsDual

background_original = pygame.image.load("textures/background.png")
menu_original = pygame.image.load("textures/menu.png")

def showMenu():
    print("MENU START")
    utils.setGlobalDefaults()
    window = utils.setupWindow()
    resizeupdate = False

    background = pygame.transform.scale(background_original, (globs.height, globs.height))
    menu = pygame.transform.scale(menu_original, (globs.height, globs.height))

    buttongroup = pygame.sprite.Group()
    levelselection_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Level Selection", relpos=(0.05, 0.44))
    difficulty_button = button.Button(relwidth=0.9, relheight=0.15, textcontent=f" Difficulty: {globs.difficulty}", relpos=(0.05, 0.62))
    settings_button = button.Button(relwidth=0.9, relheight=0.15, textcontent="Settings", relpos=(0.05, 0.80))
    buttongroup.add(levelselection_button, difficulty_button, settings_button)

    labelgroup = pygame.sprite.Group()
    line1_label = label.Label(text='"Invincibility lies in defence;', anchor="center", reltextsize=0.06, relanchorpointposition=(0.5, 0.32))
    line2_label = label.Label(text='Victory in the attack."', anchor="center", reltextsize=0.06, relanchorpointposition=(0.5, 0.38))
    labelgroup.add(line1_label, line2_label)
    # btw that quote is from sun tzu

    # draw window
    window.blit(background, (0, 0))
    window.blit(background, relToAbsDual(1, 0))
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
                    if levelselection_button.rect.collidepoint(mousepos):
                        run = False
                        globs.level_selection = True
                    if difficulty_button.rect.collidepoint(mousepos):
                        if globs.difficulty < 3:
                            globs.difficulty += 1
                        else:
                            globs.difficulty = 1
                        print(globs.difficulty)
                        difficulty_button.text = f" Difficulty: {globs.difficulty}"
                        print(globs.difficulty)
                        difficulty_button.text = f" difficulty: {globs.difficulty}"
                        difficulty_button.update()
                        difficulty_button.draw(window=window)
                        pygame.display.update()
                        utils.playSound('click')
                    if settings_button.rect.collidepoint(mousepos):
                        utils.showSettings(window=window)
                        resizeupdate = True
            # keypress event
            if event.type == pygame.KEYDOWN:
                if event.key == globs.ESCAPE:
                    run = False
                    globs.titlescreen = True
            # resize event
            if event.type == pygame.VIDEORESIZE or resizeupdate:
                resizeupdate = False
                w, h = pygame.display.get_surface().get_size()
                utils.resizeWindow(w, h)
                background = pygame.transform.scale(background_original, (relToAbsDual(1, 1)))
                menu = pygame.transform.scale(menu_original, relToAbsDual(1, 1))
                window.blit(background, (0, 0))
                window.blit(background, relToAbsDual(1, 0))
                window.blit(menu, (0, 0))
                for i in buttongroup:
                    i.update()
                    i.draw(window=window)
                for i in labelgroup:
                    i.update()
                    i.draw(window=window)
                pygame.display.update()

    utils.playSound('click')
    print("MENU END")
