import pygame
from utils import relToAbsDual

selection_texture = pygame.image.load("textures/selection.png")
sword_texture = pygame.image.load("textures/sword.png")
bow_texture = pygame.image.load("textures/bow.png")

class Selection(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(selection_texture, relToAbsDual(0.15, 0.15))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.bottomright = relToAbsDual(0.95, 0.95)
        self.items = [["sword", -1], ["bow", 3], ["katana", 3], ["knives", 15]]
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
        elif item[0] == "bow":
            self.item = pygame.transform.scale(bow_texture, relToAbsDual(0.1, 0.1))
        elif item[0] == "katana":
            self.item = pygame.transform.scale(selection_texture, relToAbsDual(0.1, 0.1))
        # 3rd item is just for test purposes don't worry
        print(self.selection)

    def draw(self, window):
        window.blit(self.image, self.rect)
        window.blit(self.item, self.itemrect)
