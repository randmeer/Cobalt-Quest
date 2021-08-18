import render.gui.level
from render import floor

class BasicLevel(render.gui.level.FloorTemplate):

    def __init__(self, spawnpos, dungeon_type, entities, blocks, lvl_width, lvl_height, name='{name}'):
        render.gui.level.FloorTemplate.__init__(self, name)
        self.lvl_height = lvl_height
        self.lvl_width = lvl_width
        self.blocks = blocks  # this is going to be transformed in a spritegroup with a bit of backprocessing
        self.entities = entities  # this is going to be transformed in a spritegroup with a bit of backprocessing
        self.dungeon_type = dungeon_type
        self.spawnpos = spawnpos

        self.camera = self.game_surface.get_rect()
        self.size = (self.lvl_width * 32, self.lvl_height * 32)
        self.block_mask = floor.CameraScene(size=self.size, camera=self.camera)
        self.entity_mask = floor.CameraScene(size=self.size, camera=self.camera)

        self.render_blocks()
        self.render_entities()

    def render_blocks(self):
        """
        is supposed to render the respective block textures on the block_mask but since there is no block texture,
        here is a quick  Todo: create a block class and a loop that blits every of its texture on here
        """
        pass

    def render_entities(self):
        """
        is supposed to render the respective entity textures on the entity_mask but since there is no entity texture,
        here is a quick  Todo: create a entity class and a loop that blits every of its texture on here
        """
        pass

    def get_voids(self):
        """
        will eventually return a list with all coordiantes inside the map that are void
        """
        pass