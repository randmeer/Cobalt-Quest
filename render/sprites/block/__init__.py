import pygame
from utils.images import block_tx
from utils import block_to_cord

class Block(pygame.sprite.Sprite):
    def __init__(self, block, pos):
        pygame.sprite.Sprite.__init__(self)
        self.priority = 3
        self.block = block
        self.image = block_tx[block]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.posx, self.posy = block_to_cord(pos, self.image)
        self.rect.x, self.rect.y = (self.posx, self.posy)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+surface.get_width()/2, self.rect.y+surface.get_height()/2))

        # for i in range(len(blocks)):
        #     if self.type == blocks[i]:
        #         self.original_image = textures[i]

        # self.image = self.original_image
        # self.rect = self.image.get_rect()
        # self.relposx = round(number=(round((atr_height(pygame.mouse.get_pos()[0]) - 0.05) / 0.1) * 0.1), ndigits=1)
        # self.relposy = round(number=(round((atr_height(pygame.mouse.get_pos()[1]) - 0.05) / 0.1) * 0.1), ndigits=1)
        # self.resize()

    # def update(self, window):
    #     self.rect.x, self.rect.y = rta_height(self.relposx), rta_height(self.relposy)
    #     self.draw(window=window)

    # def resize(self):
    #     self.image = pygame.transform.scale(self.original_image, (rta_dual(0.1, 0.1)))
    #     self.rect = self.image.get_rect()

    # def draw(self, window):
    #     window.blit(self.image, self.rect)
