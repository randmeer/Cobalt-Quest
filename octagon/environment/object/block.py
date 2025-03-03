import pygame

from octagon.utils import block_to_cord, img


class Block(pygame.sprite.Sprite):
    def __init__(self, blockgrid, blockpos, pos):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 3
        self.texture = img.BlockTexture(blockgrid, blockpos)
        self.image = self.texture.get()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.posx, self.posy = block_to_cord(pos, self.image)
        self.rect.x, self.rect.y = (self.posx, self.posy)

    def draw(self, surface, convert):
        surface.blit(self.texture.get(), convert(self.rect.topleft))
