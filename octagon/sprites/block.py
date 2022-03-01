import pygame

from octagon.utils import block_to_cord, img


class Block(pygame.sprite.Sprite):
    def __init__(self, block, pos):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 3
        self.block = block
        self.image = img.block[img.blockcode[block]]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.posx, self.posy = block_to_cord(pos, self.image)
        self.rect.x, self.rect.y = (self.posx, self.posy)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+surface.get_width()/2, self.rect.y+surface.get_height()/2))
