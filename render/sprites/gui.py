import pygame
import QuickJSON

from utils.images import selection_tx, item_tx, heart_tx, cross_tx
from render.sprites import progress_bar
from render.elements import label
from utils import globs, rta_height, rta_dual_height, get_setting

class IngameGUI(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # [string item_name, int item_count (-1 for infinite), float item_cooldown (in seconds)]
        self.inventory = QuickJSON.QJSON(f"./data/savegames/{get_setting('current_savegame')}/inventory.json")
        self.hotbar = []
        self.load_hotbar()
        self.rects, self.itemlabels = [], []
        for i in range(len(self.hotbar)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        self.slot = 0
        self.resize()
        self.update()

    def load_hotbar(self):
        self.inventory.load()
        self.hotbar = self.inventory["hotbar"]
        print(self.hotbar)
    def save_hotbar(self):
        self.inventory.save()

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
        self.itemtextures = []
        for i in self.hotbar:
            self.itemtextures.append(item_tx[i[1]])
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
        for i in self.hotbar:
            if i[2] == 0:
                #print("ITEM ZERO AAA")
                i[0] = i[1] = "unset"
                i[2] = i[3] = -1
                self.resize()

        for i in range(len(self.hotbar)):
            if self.hotbar[i][2] != -1:
                self.itemlabels.append(label.Label(text=str(self.hotbar[i][2]), anchor="topleft", relpos=(i * 0.045 + i * 0.025 + 0.005, 0.055), color=(255, 255, 255)))

    def set_selectangle(self, pos: int):
        self.slot = pos
        if self.slot > len(self.hotbar)-1:
            self.slot = 0
        elif self.slot < 0:
            self.slot = len(self.hotbar) - 1

    def draw(self, surface):
        for i in range(len(self.rects)):
            self.surf_selection.blit(self.overlangle, self.rects[i])
            if self.itemtextures[i] is not None:
                self.surf_selection.blit(self.itemtextures[i], (self.rects[i].x + 2, self.rects[i].y + 2))
        for i in self.itemlabels:
            i.update()
            i.draw(surface=self.surf_selection)
        self.surf_selection_2.blit(self.surf_selection, rta_dual_height(0.01, 0.01))
        self.surf_selection_2.blit(self.selectangle, (self.rects[self.slot].x, self.rects[self.slot].y))
        surface.blit(self.surf_selection_2, self.surf_selection_rect)
        surface.blit(self.objectangle, rta_dual_height(0.025, 0.025))
        self.objectivelabel.draw(surface=surface)
        for i in self.bars:
            i.draw(surface=surface)
