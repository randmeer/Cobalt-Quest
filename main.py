import octagon
from game import globs


if __name__ == '__main__':
    octagon.init()

    window = octagon.window(f"Cobalt Quest {globs.VERSION}")

    from game.gui import menu, title_screen, map, dungeon, singleplayer, multiplayer
    from game.environment import floor

    GAMESTATES = {
        "titlescreen": title_screen.TitleScreen,
        "menu": menu.Menu,
        "singleplayer": singleplayer.Singleplayer,
        "multiplayer": multiplayer.Multiplayer,
        "map": map.Map,
        "dungeon": dungeon.Dungeon,
        "floor": floor.Floor
    }
    octagon.run(window, GAMESTATES, "titlescreen")

    octagon.quit()
