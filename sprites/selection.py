import pygame
from sprites import label
from utils import relToAbsDual

dagger_texture = pygame.image.load("textures/dagger.png")
shuriken_texture = pygame.image.load("textures/shuriken.png")
bow_texture = pygame.image.load("textures/bow.png")
item_texture = pygame.image.load("textures/cross.png")

# ToDo: This whole class needs to be reworked & moved to the gui area

class Selection(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.centers = [(0.075, 0.925), (0.200, 0.925), (0.325, 0.925), (0.450, 0.925), (0.575, 0.925), (0.700, 0.925)]
        self.centers_small = [(0.050, 0.825), (0.125, 0.825), (0.200, 0.825), (0.275, 0.825)]
        self.rects = [pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0),
                      pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)]
        self.rects_small = [pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0),
                            pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)]

        self.items = [["dagger", -1], ["katana", -1], ["shuriken", 25], ["bow", 10], ["unknown", -1], ["unknown", -1]]
        self.itemlabels = []
        self.weapon, self.block = 0, 0
        self.resize()
        self.update()

    def resize(self):

        self.itemtextures = [pygame.transform.scale(dagger_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(item_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(shuriken_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(bow_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(item_texture, relToAbsDual(0.1, 0.1)),
                             pygame.transform.scale(item_texture, relToAbsDual(0.1, 0.1))]
        self.selectangle = pygame.Surface(relToAbsDual(0.1, 0.1))
        self.selectangle.fill((255, 255, 255))
        self.selectangle.set_alpha(125)
        self.selectangle_small = pygame.transform.scale(self.selectangle, relToAbsDual(0.05, 0.05))

        for i in range(6):
            self.rects[i].size = relToAbsDual(0.1, 0.1)
            self.rects[i].center = relToAbsDual(self.centers[i][0], self.centers[i][1])
        for i in range(4):
            self.rects_small[i].size = relToAbsDual(0.05, 0.05)
            self.rects_small[i].center = relToAbsDual(self.centers_small[i][0], self.centers_small[i][1])

    def update(self):
        self.itemlabels = []
        for i in range(len(self.items)):
            if self.items[i][1] != -1:
                self.itemlabels.append(label.Label(text=str(self.items[i][1]), anchor="bottomleft", reltextsize=0.04, relanchorpointposition=(self.centers[i][0]-0.05, self.centers[i][1]+0.05), textcolor=(255, 255, 255)))

        if self.weapon >= 6:
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
        for i in range(6):
            window.blit(self.itemtextures[i], self.rects[i])
        for i in self.itemlabels:
            i.update()
            i.draw(window=window)
