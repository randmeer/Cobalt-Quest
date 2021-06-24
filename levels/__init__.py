import gui.level

class level(gui.level.LevelTemplate):

    def __init__(self, spawnpos, dungeon_type, entities, blocks, lvl_width,
                 lvl_height, name='{name}'):
        gui.level.LevelTemplate.__init__(self, name)
        self.lvl_height = lvl_height
        self.lvl_width = lvl_width
        self.blocks = blocks
        self.entities = entities
        self.dungeon_type = dungeon_type
        self.spawnpos = spawnpos