import pygame
from utils import relToAbsDual

dagger_texture = pygame.image.load("textures/dagger.png")
shuriken_texture = pygame.image.load("textures/shuriken.png")
bow_texture = pygame.image.load("textures/bow.png")

# ToDo: This whole class needs to be reworked someday

class Selection(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.centers = [(0.425, 0.925), (0.550, 0.925), (0.675, 0.925), (0.800, 0.925), (0.925, 0.925)]
        self.centers_small = [(0.050, 0.950), (0.125, 0.950), (0.200, 0.950), (0.275, 0.950)]
        self.rects = [pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0),
                      pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)]
        self.rects_small = [pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0),
                            pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)]

        self.items = [["dagger", -1], ["katana", -1], ["shuriken", 50], ["bow", 10], ["unknown", -1]]
        self.weapon, self.block = 0, 0
        self.resize()

    def resize(self):
        self.itemtextures = [pygame.transform.scale(dagger_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(bow_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1))]
        self.selectangle = pygame.Surface(relToAbsDual(0.1, 0.1))
        self.selectangle.fill((255, 255, 255))
        self.selectangle.set_alpha(125)
        self.selectangle_small = pygame.transform.scale(self.selectangle, relToAbsDual(0.05, 0.05))

        for i in range(5):
            self.rects[i].size = relToAbsDual(0.1, 0.1)
            self.rects[i].center = relToAbsDual(self.centers[i][0], self.centers[i][1])
        for i in range(4):
            self.rects_small[i].size = relToAbsDual(0.05, 0.05)
            self.rects_small[i].center = relToAbsDual(self.centers_small[i][0], self.centers_small[i][1])

    def update(self):
        if self.weapon >= 5:
            self.weapon = 0
        elif self.weapon < 0:
            self.weapon = 4
        if self.block >= 4:
            self.block = 0
        elif self.block < 0:
            self.block = 3

    def draw(self, window):
        window.blit(self.selectangle, self.rects[self.weapon])
        window.blit(self.selectangle_small, self.rects_small[self.block])
        for i in range(5):
            window.blit(self.itemtextures[i], self.rects[i])
