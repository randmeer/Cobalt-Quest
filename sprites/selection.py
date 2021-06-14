import pygame
from utils import absToRel
from utils import relToAbsDual
from utils import relToAbs

selection_texture = pygame.image.load("textures/selection.png")
sword_texture = pygame.image.load("textures/sword.png")
web_texture = pygame.image.load("textures/web.png")

class Selection(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(selection_texture, relToAbsDual(0.15, 0.15))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.bottomright = relToAbsDual(0.95, 0.95)
        self.items = [["sword", -1], ["web", 3], ["test", 3]]
        self.selection = 0
        self.item = pygame.transform.scale(sword_texture, relToAbsDual(0.1, 0.1))
        self.itemrect = self.item.get_rect()
        self.itemrect.center = self.rect.center

    def resize(self):
        self.image = pygame.transform.scale(self.original_image, (relToAbsDual(0.15, 0.15)))
        self.rect = self.image.get_rect()
        self.rect.bottomright = relToAbsDual(0.95, 0.95)
        self.update()
        self.itemrect = self.item.get_rect()
        self.itemrect.center = self.rect.center

    def update(self):
        if self.selection >= len(self.items):
            self.selection = 0
        item = self.items[self.selection]
        if item[0] == "sword":
            self.item = pygame.transform.scale(sword_texture, relToAbsDual(0.1, 0.1))
        elif item[0] == "web":
            self.item = pygame.transform.scale(web_texture, relToAbsDual(0.1, 0.1))
        elif item[0] == "test":
            self.item = pygame.transform.scale(selection_texture, relToAbsDual(0.1, 0.1))
        # 3rd item is just for test purposes don't worry

    def draw(self, window):
        window.blit(self.image, self.rect)
        window.blit(self.item, self.itemrect)