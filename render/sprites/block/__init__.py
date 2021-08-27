import pygame
from utils.images import block_tx
# from utils.images import web_texture, mud_texture, brick_texture, cobblestone_texture, sandstone_texture, wall_texture
# from utils.__init__ import rta_height, rta_dual

# blocks = ["web", "wall", "brick", "cobble", "sandstone", "mud"]
# textures = [web_texture, wall_texture, brick_texture, cobblestone_texture, sandstone_texture, mud_texture]

class Block(pygame.sprite.Sprite):
    def __init__(self, block, pos):
        pygame.sprite.Sprite.__init__(self)
        self.block = block
        self.pos = pos
        self.posx, self.posy = pos[0]*16, pos[1]*16
        self.image = block_tx[block]
        self.rect = self.image.get_rect()

        # this converts the positions of the blocks from my system to something pygame can use
        if self.posx < 0 and self.posy < 0:
            pass
        elif self.posx > 0 and self.posy < 0:
            self.posx -= self.image.get_width()
        elif self.posx > 0 and self.posy > 0:
            self.posx -= self.image.get_width()
            self.posy -= self.image.get_height()
        elif self.posx < 0 and self.posy > 0:
            self.posy -= self.image.get_height()

        self.rect.x, self.rect.y = (self.posx, self.posy)
        #print(self.rect)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x+surface.get_width()/2, self.rect.y+surface.get_height()/2))
        #print("drew block")

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
