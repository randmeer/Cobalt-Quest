import pygame

from utils.images import web_texture, mud_texture, brick_texture, cobblestone_texture, sandstone_texture, wall_texture
from utils.__init__ import relToAbs, relToAbsDual, absToRel

blocks = ["web", "wall", "brick", "cobble", "sandstone", "mud"]
textures = [web_texture, wall_texture, brick_texture, cobblestone_texture, sandstone_texture, mud_texture]

class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype):
        pygame.sprite.Sprite.__init__(self)
        self.type = blocktype
        for i in range(len(blocks)):
            if self.type == blocks[i]:
                self.original_image = textures[i]
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.relposx = round(number=(round((absToRel(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.relposy = round(number=(round((absToRel(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)
        self.resize()

    def update(self, window):
        self.rect.x, self.rect.y = relToAbs(self.relposx), relToAbs(self.relposy)
        self.draw(window=window)

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (relToAbsDual(0.1, 0.1)))
        self.rect = self.image.get_rect()

    def draw(self, window):
        window.blit(self.image, self.rect)
