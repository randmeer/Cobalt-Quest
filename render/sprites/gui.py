import pygame

from utils.images import selection_tx, cross_tx, bow_tx, shuriken_tx, dagger_tx, heart_tx
from render.sprites import progress_bar
from render.elements import label
from utils import globs, rta_height, rta_dual_height

class IngameGUI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # [string item_name, int item_count (-1 for infinite), float item_cooldown (in seconds)]
        self.weapons = [["dagger", -1, 0.25], ["katana", -1, 1.00], ["shuriken", 25, 0.10], ["bow", 10, 0.50], ["unknown", -1, 0.00], ["unknown", -1, 0.00]]
        self.rects, self.itemlabels = [], []
        for i in range(len(self.weapons)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        self.weapon = self.block = 0
        self.resize()
        self.update()

    def resize(self):
        self.surf_selection = pygame.Surface(rta_dual_height(0.72, 0.1), pygame.SRCALPHA)
        # this should theoretically be 0.725, but for some reason it's 0.72 and if it works don't change it
        self.surf_selection_2 = pygame.Surface(rta_dual_height(0.74, 0.12), pygame.SRCALPHA)
        self.surf_selection_rect = self.surf_selection.get_rect()
        self.surf_selection_rect.bottomright = (globs.SIZE[0] - rta_height(0.035), rta_height(0.965))
        self.objectangle = pygame.Surface(rta_dual_height(0.725, 0.11), pygame.SRCALPHA)
        self.objectangle.fill((255, 255, 255))
        self.objectangle.set_alpha(75)
        self.objectivelabel = label.Label(text="Objective:", anchor="topleft", relpos=(0.035, 0.035), color=(255, 255, 255))
        self.itemtextures = [dagger_tx,
                             cross_tx,
                             shuriken_tx,
                             bow_tx,
                             cross_tx,
                             cross_tx]
        self.selectangle = selection_tx
        self.overlangle = pygame.Surface(rta_dual_height(0.1, 0.1), pygame.SRCALPHA)
        self.overlangle.fill((255, 255, 255))
        self.overlangle.set_alpha(75)
        for i in range(len(self.rects)):
            self.rects[i].size = rta_dual_height(0.1, 0.1)
            self.rects[i].center = (i * rta_height(0.1) + rta_height(0.05) + i * rta_height(0.025), rta_height(0.05))
        self.bars = [progress_bar.ProgressBar(icon=heart_tx, maxvalue=100, colors=((255, 0, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.944)),  # health
                     progress_bar.ProgressBar(icon=cross_tx, maxvalue=100, colors=((0, 0, 255), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.903)),  # mana
                     progress_bar.ProgressBar(icon=cross_tx, maxvalue=100, colors=((0, 255, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.861))]  # progress

    def update(self):
        self.surf_selection = pygame.Surface(rta_dual_height(0.72, 0.1), pygame.SRCALPHA)
        self.surf_selection_2 = pygame.Surface(rta_dual_height(0.74, 0.12), pygame.SRCALPHA)
        self.itemlabels = []
        for i in range(len(self.weapons)):
            if self.weapons[i][1] != -1:
                self.itemlabels.append(label.Label(text=str(self.weapons[i][1]), anchor="topleft", relpos=(i * 0.045 + i * 0.025 + 0.005, 0.055), color=(255, 255, 255)))

    def set_selectangle(self, pos: int):
        self.weapon = pos
        if self.weapon > len(self.weapons)-1:
            self.weapon = 0
        elif self.weapon < 0:
            self.weapon = len(self.weapons)-1

    def draw(self, surface):
        for i in range(len(self.rects)):
            self.surf_selection.blit(self.overlangle, self.rects[i])
            self.surf_selection.blit(self.itemtextures[i], (self.rects[i].x + 2, self.rects[i].y + 2))
        for i in self.itemlabels:
            i.update()
            i.draw(surface=self.surf_selection)
        self.surf_selection_2.blit(self.surf_selection, rta_dual_height(0.01, 0.01))
        self.surf_selection_2.blit(self.selectangle, (self.rects[self.weapon].x, self.rects[self.weapon].y))
        surface.blit(self.surf_selection_2, self.surf_selection_rect)
        surface.blit(self.objectangle, rta_dual_height(0.025, 0.025))
        self.objectivelabel.draw(surface=surface)
        for i in self.bars:
            i.draw(surface=surface)
