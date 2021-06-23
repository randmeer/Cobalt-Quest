import pygame

from utils.images import selection_texture, cross_texture, bow_texture, shuriken_texture, dagger_texture, \
    broken_heart_texture, tick_texture, ichkeksi_texture, heart_texture
from sprites import label
from utils import relToAbsDual, relToAbs, renderText, globs

# GUI class is unfinished, working on it. ~Rande

class GUI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.weapons = [["dagger", -1], ["katana", -1], ["shuriken", 25], ["bow", 10], ["unknown", -1], ["unknown", -1]]
        self.blocks = [["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10], ["block", 10]]
        self.centers = [(0.075, 0.925), (0.200, 0.925), (0.325, 0.925), (0.450, 0.925), (0.575, 0.925), (0.700, 0.925)]
        self.centers_small = [(0.050, 0.825), (0.125, 0.825), (0.200, 0.825), (0.275, 0.825), (0.350, 0.825), (0.425, 0.825), (0.500, 0.825), (0.575, 0.825), (0.650, 0.825), (0.725, 0.825)]
        self.rects, self.rects_small, self.itemlabels = [], [], []
        for i in range(len(self.weapons)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        for i in range(len(self.blocks)):
            self.rects_small.append(pygame.Rect(0, 0, 0, 0))
        self.weapon = self.block = 0
        self.resize()
        self.update()

    def resize(self):
        self.titlangle = pygame.Surface(relToAbsDual(0.725, 0.11))
        self.titlangle.fill((0, 0, 0))
        self.titlangle.set_alpha(75)
        self.statlangle = pygame.Surface(relToAbsDual(0.725, 0.11))
        self.statlangle.fill((0, 0, 0))
        self.statlangle.set_alpha(75)
        self.floorlabel = label.Label(text="3rd Floor:", anchor="topleft", reltextsize=0.05, relanchorpointposition=(0.035, 0.035), textcolor=(255, 255, 255))
        self.titlelabel = label.Label(text="Menga's Hideout", anchor="topleft", reltextsize=0.05, relanchorpointposition=(0.035, 0.085), textcolor=(255, 255, 255))
        self.itemtextures = [pygame.transform.scale(dagger_texture, relToAbsDual(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDual(0.08, 0.08)),
                             pygame.transform.scale(shuriken_texture, relToAbsDual(0.08, 0.08)),
                             pygame.transform.scale(bow_texture, relToAbsDual(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDual(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDual(0.08, 0.08))]
        self.selectangle = pygame.transform.scale(selection_texture, relToAbsDual(0.12, 0.12))
        self.selectangle_small = pygame.transform.scale(selection_texture, relToAbsDual(0.06, 0.06))
        self.overlangle = pygame.Surface(relToAbsDual(0.1, 0.1))
        self.overlangle.fill((0, 0, 0))
        self.overlangle.set_alpha(75)
        self.overlangle_small = pygame.transform.scale(self.overlangle, relToAbsDual(0.05, 0.05))

        for i in range(len(self.rects)):
            self.rects[i].size = relToAbsDual(0.1, 0.1)
            self.rects[i].center = relToAbsDual(self.centers[i][0], self.centers[i][1])
        for i in range(len(self.rects_small)):
            self.rects_small[i].size = relToAbsDual(0.05, 0.05)
            self.rects_small[i].center = relToAbsDual(self.centers_small[i][0], self.centers_small[i][1])

    def update(self):
        self.itemlabels = []
        for i in range(len(self.weapons)):
            if self.weapons[i][1] != -1:
                self.itemlabels.append(label.Label(text=str(self.weapons[i][1]), anchor="bottomleft", reltextsize=0.04, relanchorpointposition=(self.centers[i][0] - 0.045, self.centers[i][1] + 0.045), textcolor=(255, 255, 255)))
        if self.weapon >= len(self.rects):
            self.weapon = 0
        elif self.weapon < 0:
            self.weapon = len(self.rects)-1
        if self.block >= len(self.rects_small):
            self.block = 0
        elif self.block < 0:
            self.block = len(self.rects_small)-1

    def draw(self, window):
        for i in range(len(self.rects)):
            window.blit(self.overlangle, self.rects[i])
            window.blit(self.itemtextures[i], (self.rects[i].x+relToAbs(0.01), self.rects[i].y+relToAbs(0.01)))
        for i in range(len(self.rects_small)):
            window.blit(self.overlangle_small, self.rects_small[i])
        window.blit(self.selectangle, (self.rects[self.weapon].x - relToAbs(0.01), self.rects[self.weapon].y - relToAbs(0.01)))
        window.blit(self.selectangle_small, (self.rects_small[self.block].x - relToAbs(0.005), self.rects_small[self.block].y - relToAbs(0.005)))
        for i in self.itemlabels:
            i.update()
            i.draw(window=window)
        window.blit(self.titlangle, relToAbsDual(0.025, 0.025))
        window.blit(self.statlangle, relToAbsDual(0.025, 0.150))
        self.floorlabel.draw(window=window)
        self.titlelabel.draw(window=window)
        renderText(window, str(int(globs.playerhealthpoints)), relToAbsDual(0.085, 0.160), globs.WHITE, relToAbs(0.048))
        renderText(window, str(globs.victimspawns - globs.victimsmissed - globs.victimskilled + 1), relToAbsDual(0.254, 0.160), globs.WHITE, relToAbs(0.048))
        renderText(window, str(globs.victimskilled), relToAbsDual(0.43, 0.160), globs.WHITE, relToAbs(0.048))
        renderText(window, str(globs.victimsmissed), relToAbsDual(0.61, 0.160), globs.WHITE, relToAbs(0.048))
        renderText(window, str(globs.damagesum), relToAbsDual(0.085, 0.215), globs.WHITE, relToAbs(0.048))
        window.blit(pygame.transform.scale(heart_texture, relToAbsDual(0.036, 0.036)), relToAbsDual(0.035, 0.160))
        window.blit(pygame.transform.scale(ichkeksi_texture, relToAbsDual(0.04, 0.04)), relToAbsDual(0.2, 0.160))
        window.blit(pygame.transform.scale(tick_texture, relToAbsDual(0.036, 0.036)), relToAbsDual(0.38, 0.160))
        window.blit(pygame.transform.scale(cross_texture, relToAbsDual(0.036, 0.036)), relToAbsDual(0.56, 0.160))
        window.blit(pygame.transform.scale(broken_heart_texture, relToAbsDual(0.036, 0.036)), relToAbsDual(0.035, 0.215))
