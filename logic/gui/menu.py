import pygame

from utils import globs, mousepos, setGlobalDefaults, playSound
from render.elements import button, image, label
from render import gui
from utils.images import background_menu_texture, logo_texture
from logic.gui.overlay import settings


def showMenu(window):
    print("MENU START")
    setGlobalDefaults()

    menu = gui.GUI(
        background=background_menu_texture, overlay=128,
        buttons=[
            button.Button(anchor="topleft", relwidth=0.264, relheight=0.1, textcontent="MAP", relpos=(0.225, 0.40)),
            button.Button(anchor="topright", relwidth=0.264, relheight=0.1, textcontent="SHOP", relpos=(0.775, 0.40)),
            button.Button(anchor="topleft", relwidth=0.413, relheight=0.1, textcontent="INVENTORY", relpos=(0.225, 0.525)),
            button.Button(anchor="topright", relwidth=0.116, relheight=0.1, textcontent="?", relpos=(0.775, 0.525)),
            button.Button(anchor="topleft", relwidth=0.413, relheight=0.1, textcontent="SETTINGS", relpos=(0.225, 0.65)),
            button.Button(anchor="topright", relwidth=0.116, relheight=0.1, textcontent=f"{globs.savegame}", relpos=(0.775, 0.65))],
        images=[
            image.Image(relpos=(0.5, 0.2), anchor="center", image=logo_texture)],
        labels=[
            label.Label(text=f"VERSION {globs.VERSION}", relpos=(0.01, 0.98), anchor="bottomleft", textcolor=(12, 18, 26)),
            label.Label(text="RANDE STUDIOS", relpos=(0.01, 0.94), anchor="bottomleft", textcolor=(12, 18, 26))])

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        if globs.quitgame:
            run = False
        mp = mousepos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                globs.quitgame = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == globs.LEFT:
                    if menu.buttongroup[0].rect.collidepoint(mp):
                        run = False
                        globs.level_selection = True
                    if menu.buttongroup[5].rect.collidepoint(mp):
                        if globs.savegame < 3:
                            globs.savegame += 1
                        else:
                            globs.savegame = 1
                        menu.buttongroup[5].text = f"{globs.savegame}"
                        playSound('click')
                    if menu.buttongroup[4].rect.collidepoint(mp):
                        settings(window=window, background=background_menu_texture)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    globs.titlescreen = True
        menu.draw(window=window)
    playSound('click')
    print("MENU END")
