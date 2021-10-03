import pygame

from utils.images import item_tx, overlays, images
from render.sprites import progress_bar
from render.elements import label
from utils import globs, rta_height, rta_dual_height, get_setting

damage_overlay = pygame.transform.scale(images["damage_overlay"], globs.SIZE)
mana_overlay = pygame.transform.scale(images["mana_overlay"], globs.SIZE)

class IngameGUI(pygame.sprite.Sprite):
    def __init__(self, invjson):
        pygame.sprite.Sprite.__init__(self)
        # [string item_name, int item_count (-1 for infinite), float item_cooldown (in seconds)]
        self.inventory = invjson
        self.hotbar = []
        self.load_hotbar()
        self.rects, self.itemlabels = [], []
        for i in range(len(self.hotbar)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        self.slot = 0
        self.last_health = self.inventory["health"]
        self.last_mana = self.inventory["mana"]
        self.overlay = None
        self.resize()

    def load_hotbar(self):
        self.inventory.load()
        self.hotbar = self.inventory["hotbar"]

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
        self.selectangle = images["selection"]
        self.overlangle = pygame.Surface(rta_dual_height(0.1, 0.1), pygame.SRCALPHA)
        self.overlangle.fill((255, 255, 255))
        self.overlangle.set_alpha(75)
        for i in range(len(self.rects)):
            self.rects[i].size = rta_dual_height(0.1, 0.1)
            self.rects[i].center = (i * rta_height(0.1) + rta_height(0.05) + i * rta_height(0.025), rta_height(0.05))
        self.bars = [progress_bar.ProgressBar(icon=images["heart"], maxvalue=100, colors=((255, 0, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.944), has_image=True, image_str="bar_health"),  # health
                     progress_bar.ProgressBar(icon=images["cross"], maxvalue=100, colors=((0, 0, 255), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.903), has_image=True, image_str="bar_mana"),  # mana
                     progress_bar.ProgressBar(icon=images["cross"], maxvalue=100, colors=((0, 255, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.861), has_image=True, image_str="bar_progress")]  # progress
        self.bars[0].set(self.inventory["health"])
        self.bars[1].set(self.inventory["mana"])

    def update(self, player):
        self.surf_selection = pygame.Surface(rta_dual_height(0.72, 0.1), pygame.SRCALPHA)
        self.surf_selection_2 = pygame.Surface(rta_dual_height(0.74, 0.12), pygame.SRCALPHA)
        self.itemlabels = []
        for i in self.hotbar:
            if i[2] == 0:
                i[0] = i[1] = "unset"
                i[2] = i[3] = -1
                self.resize()
        for i in range(len(self.hotbar)):
            if self.hotbar[i][2] != -1:
                self.itemlabels.append(label.Label(text=str(self.hotbar[i][2]), anchor="topleft", relpos=(i * 0.045 + i * 0.025 + 0.005, 0.055), color=(255, 255, 255)))

        if self.last_health != player.health:
            if self.overlay is not None:
                self.overlay.set_alpha(255)
                self.overlay = None
            self.bars[0].set(player.health, player.max_health)
            self.overlay = damage_overlay
            self.last_health = player.health
        if self.last_mana != player.mana:
            if self.overlay is not None:
                self.overlay.set_alpha(255)
                self.overlay = None
            self.bars[1].set(player.mana, player.max_mana)
            self.overlay = mana_overlay
            self.last_mana = player.mana

        if self.overlay is not None:
            self.overlay.set_alpha(self.overlay.get_alpha()-5)
            if self.overlay.get_alpha() <= 0:
                self.overlay.set_alpha(255)
                self.overlay = None
                print("overlay is none")

    def set_selectangle(self, pos: int):
        self.slot = pos
        if self.slot > len(self.hotbar)-1:
            self.slot = 0
        elif self.slot < 0:
            self.slot = len(self.hotbar) - 1

    def draw(self, surface):
        if self.overlay is not None:
            surface.blit(self.overlay, (0, 0))
        for i in range(len(self.rects)):
            self.surf_selection.blit(overlays[self.hotbar[i][0]][0], self.rects[i])
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

