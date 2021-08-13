import pygame
from utils.images import selection_texture, cross_texture, bow_texture, shuriken_texture, dagger_texture, \
    broken_heart_texture, tick_texture, ichkeksi_texture, heart_texture
from render.sprites import label, progress_bar
from utils import renderText, globs, relToAbsDual2, relToAbsWidth, relToAbsHeight, relToAbsDualWidth, relToAbsDualHeight

# ToDo: Add a GUI-size setting which affects IngameGUI, Button Class ect.

class IngameGUI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.weapons = [["dagger", -1], ["katana", -1], ["shuriken", 25], ["bow", 10], ["unknown", -1], ["unknown", -1]]
        self.rects, self.itemlabels = [], []
        for i in range(len(self.weapons)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        self.weapon = self.block = 0
        self.resize()
        self.update()

    def resize(self):
        self.surf_selection = pygame.Surface(relToAbsDualHeight(0.72, 0.1), pygame.SRCALPHA)
        # this should theoretically be 0.725, but for some reason it's 0.72 and if it works don't change it
        self.surf_selection_2 = pygame.Surface(relToAbsDualHeight(0.74, 0.12), pygame.SRCALPHA)
        self.surf_selection_rect = self.surf_selection.get_rect()
        self.surf_selection_rect.bottomright = (globs.SIZE[0] - relToAbsHeight(0.035), relToAbsHeight(0.965))
        self.objectangle = pygame.Surface(relToAbsDualHeight(0.725, 0.11), pygame.SRCALPHA)
        self.objectangle.fill((0, 255, 0))
        self.objectangle.set_alpha(75)
        self.objectivelabel = label.Label(text="Objective: Complete GUI Class", anchor="topleft", reltextsize=0.04,
                                          relanchorpointposition=(0.035, 0.035), textcolor=(255, 255, 255))
        self.itemtextures = [pygame.transform.scale(dagger_texture, relToAbsDualHeight(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDualHeight(0.08, 0.08)),
                             pygame.transform.scale(shuriken_texture, relToAbsDualHeight(0.08, 0.08)),
                             pygame.transform.scale(bow_texture, relToAbsDualHeight(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDualHeight(0.08, 0.08)),
                             pygame.transform.scale(cross_texture, relToAbsDualHeight(0.08, 0.08))]
        self.selectangle = pygame.transform.scale(selection_texture, relToAbsDualHeight(0.12, 0.12))
        self.overlangle = pygame.Surface(relToAbsDualHeight(0.1, 0.1), pygame.SRCALPHA)
        self.overlangle.fill((0, 255, 0))
        self.overlangle.set_alpha(75)
        for i in range(len(self.rects)):
            self.rects[i].size = relToAbsDualHeight(0.1, 0.1)
            self.rects[i].center = (
            i * relToAbsHeight(0.1) + relToAbsHeight(0.05) + i * relToAbsHeight(0.025), relToAbsHeight(0.05))
        self.bar_health = progress_bar.ProgressBar(icon=heart_texture, maxvalue=100, colors=((255, 0, 0), (75, 75, 75)), relsize=(0.6, 0.025))
        self.bar_mana = progress_bar.ProgressBar(icon=cross_texture, maxvalue=100, colors=((0, 0, 255), (75, 75, 75)), relsize=(0.6, 0.025))
        self.bar_progress = progress_bar.ProgressBar(icon=cross_texture, maxvalue=100, colors=((0, 255, 0), (75, 75, 75)), relsize=(0.6, 0.025))

    def update(self):
        self.surf_selection = pygame.Surface(relToAbsDualHeight(0.72, 0.1), pygame.SRCALPHA)
        self.surf_selection_2 = pygame.Surface(relToAbsDualHeight(0.74, 0.12), pygame.SRCALPHA)
        self.itemlabels = []
        for i in range(len(self.weapons)):
            if self.weapons[i][1] != -1:
                self.itemlabels.append(label.Label(text=str(self.weapons[i][1]), anchor="topleft", reltextsize=0.04,
                                                   relanchorpointposition=(i * 0.1 + i * 0.025, 0.07),
                                                   textcolor=(255, 255, 255)))
        if self.weapon >= len(self.rects):
            self.weapon = 0
        elif self.weapon < 0:
            self.weapon = len(self.rects) - 1

    def set_selectangle(self, pos: int):
        self.weapon = pos

    def draw(self, window):
        for i in range(len(self.rects)):
            self.surf_selection.blit(self.overlangle, self.rects[i])
            self.surf_selection.blit(self.itemtextures[i], (self.rects[i].x + relToAbsHeight(0.01), self.rects[i].y + relToAbsHeight(0.01)))
        for i in self.itemlabels:
            i.update()
            i.draw(window=self.surf_selection)
        self.surf_selection_2.blit(self.surf_selection, relToAbsDualHeight(0.01, 0.01))
        self.surf_selection_2.blit(self.selectangle, (self.rects[self.weapon].x, self.rects[self.weapon].y))
        window.blit(self.surf_selection_2, self.surf_selection_rect)
        window.blit(self.objectangle, relToAbsDualHeight(0.025, 0.025))
        self.objectivelabel.draw(window=window)
        window.blit(self.bar_health.get(), relToAbsDualHeight(0.025, 0.950))
        window.blit(self.bar_mana.get(), relToAbsDualHeight(0.025, 0.9125))
        window.blit(self.bar_progress.get(), relToAbsDualHeight(0.025, 0.875))
