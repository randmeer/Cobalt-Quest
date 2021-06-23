import gui.level

class level(gui.level.LevelTemplate):

    def __init__(self, name='{name}'):
        gui.level.LevelTemplate.__init__(self, name)
        self.lvl_height, self.lvl_width = 20, 40