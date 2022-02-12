import pygame
import octagon
import globs

if __name__ == '__main__':
    octagon.init()
    window = octagon.window()

    from game.gui import menu, title_screen, map, dungeon
    from game.floor import Floor

    # main game loop
    run = True
    while run:

        # event iteration
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # game state manager
        if globs.quitgame:
            run = False
        elif globs.titlescreen:
            title_screen.show_title_screen(window=window)
        elif globs.menu:
            menu.show_menu(window=window)
        elif globs.map:
            map.show_map(window=window)
        elif globs.dungeon:
            dungeon.show_dungeon(window=window, dungeon=globs.dungeon_str)
        elif globs.floor:
            globs.floor_str = "entrance"
            floor = Floor(window=window)
            floor.load()
            floor.start_loop()
        else:
            print("no current state")
            run = False

    octagon.quit()

