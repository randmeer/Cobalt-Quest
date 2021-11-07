import pygame

from utils.images import item_tx, overlays, images
from render.sprites import progress_bar
from render.elements import label
from utils import globs, rta_height, rta_dual_height, rta_dual, render_multiline_text

damage_overlay = pygame.transform.scale(images["damage_overlay"], globs.SIZE)
mana_overlay = pygame.transform.scale(images["mana_overlay"], globs.SIZE)

class IngameGUI(pygame.sprite.Sprite):
    def __init__(self, invjson):
        pygame.sprite.Sprite.__init__(self)
        # [string item_name, int item_count (-1 for infinite), float item_cooldown (in seconds)]
        self.inventory = invjson
        self.inventory.load()
        self.hotbar, self.rects, self.itemlabels, self.itemtextures = [], [], [], []
        self.load_hotbar()

        for i in range(len(self.hotbar)):
            text = ""
            if self.hotbar[i][2] != -1:
                text = str(self.hotbar[i][2])
            self.itemlabels.append(label.Label(text=text, anchor="topleft", relpos=(i * 0.045 + i * 0.025 + 0.005, 0.055), color=(255, 255, 255)))
        self.update_hotbar()

        self.last_hotbar = self.hotbar
        for i in range(len(self.hotbar)):
            self.rects.append(pygame.Rect(0, 0, 0, 0))
        self.slot = 0
        self.last_health = self.inventory["health"]
        self.last_mana = self.inventory["mana"]
        self.overlay = None

        self.surf_selection = pygame.Surface(rta_dual_height(0.72, 0.1), pygame.SRCALPHA)
        # this should theoretically be 0.725, but for some reason it's 0.72 and if it works don't change it
        self.surf_selection_rect = self.surf_selection.get_rect()
        self.surf_selection_rect.bottomright = (globs.SIZE[0] - rta_height(0.035), rta_height(0.965))

        self.objectangle = pygame.Surface(rta_dual_height(0.725, 0.11), pygame.SRCALPHA)
        self.objectangle.fill((255, 255, 255))
        self.objectangle.set_alpha(75)
        self.objectivelabel = label.Label(text="Objective:", anchor="topleft", relpos=(0.035, 0.035), color=(255, 255, 255))

        self.chatangle = pygame.Surface(rta_dual(0.367, 0.805), pygame.SRCALPHA)
        self.last_chat = globs.chat
        self.update_chat()

        self.selectangle = images["selection"]
        self.overlangle = pygame.Surface(rta_dual_height(0.1, 0.1), pygame.SRCALPHA)
        self.overlangle.fill((255, 255, 255))
        self.overlangle.set_alpha(75)
        for i in range(len(self.rects)):
            self.rects[i].size = rta_dual_height(0.1, 0.1)
            self.rects[i].center = (i * rta_height(0.1) + rta_height(0.05) + i * rta_height(0.025), rta_height(0.05))

        self.bars = [progress_bar.ProgressBar(icon=images["heart"], maxvalue=100, colors=((255, 0, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.944), has_image=True, image_str="bar_health"),
                     progress_bar.ProgressBar(icon=images["cross"], maxvalue=100, colors=((0, 0, 255), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.903), has_image=True, image_str="bar_mana"),
                     progress_bar.ProgressBar(icon=images["cross"], maxvalue=100, colors=((0, 255, 0), (75, 75, 75)), relsize=(0.3, 0.0347), relpos=(0.02, 0.861), has_image=True, image_str="bar_progress")]
        self.bars[0].set(self.inventory["health"])
        self.bars[1].set(self.inventory["mana"])

        self.last_fps = []
        for i in range(256):
            self.last_fps.append([i, 144])

    def load_hotbar(self):
        self.inventory.load()
        self.hotbar = self.inventory["hotbar"]

    def save_hotbar(self):
        self.inventory.save()

    def update_hotbar(self):
        for i in range(len(self.hotbar)):
            if self.hotbar[i][2] == 0:
                self.hotbar[i][0] = self.hotbar[i][1] = "unset"
                self.hotbar[i][2] = self.hotbar[i][3] = -1
                self.itemlabels[i].text = ""
                self.itemlabels[i].render()
            elif self.hotbar[i][2] != -1:
                self.itemlabels[i].text = str(self.hotbar[i][2])
                self.itemlabels[i].render()

        self.itemtextures = []
        for i in self.hotbar:
            self.itemtextures.append(item_tx[i[1]])

    def update_chat(self):
        if self.last_chat != globs.chat:
            self.chatangle.set_alpha(255)
            self.chatangle.fill((0, 0, 0, 0))
            lastlines = "\n".join(globs.chat.splitlines()[-5:])
            # set to 19 for full lenght chat, on 5 for now because it looks better ig...
            render_multiline_text(surface=self.chatangle, text=lastlines, pos=(0, 0), fadeout="up")
        else:
            self.chatangle.set_alpha(self.chatangle.get_alpha()-1)
        self.last_chat = globs.chat

    def update(self, player):
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
        for i in range(len(self.hotbar)):
            if self.hotbar[i][2] != self.last_hotbar[i]:
                self.update_hotbar()

        # i know it's shit, but nothing exept for this worked
        self.last_hotbar = []
        for i in range(len(self.hotbar)):
            self.last_hotbar.append(self.hotbar[i][2])

        self.update_chat()

    def set_selectangle(self, pos: int):
        self.slot = pos
        if self.slot > len(self.hotbar)-1:
            self.slot = 0
        elif self.slot < 0:
            self.slot = len(self.hotbar) - 1

    def draw(self, surface, clock):
        if self.overlay is not None:
            surface.blit(self.overlay, (0, 0))
        for i in range(len(self.rects)):
            self.surf_selection.blit(overlays[self.hotbar[i][0]][0], self.rects[i])
            if self.itemtextures[i] is not None:
                self.surf_selection.blit(self.itemtextures[i], (self.rects[i].x + 2, self.rects[i].y + 2))
        for i in self.itemlabels:
            i.update()
            i.draw(surface=self.surf_selection)
        surf_selection_2 = pygame.Surface(rta_dual_height(0.74, 0.12), pygame.SRCALPHA)
        surf_selection_2.blit(self.surf_selection, rta_dual_height(0.01, 0.01))
        surf_selection_2.blit(self.selectangle, (self.rects[self.slot].x, self.rects[self.slot].y))
        surface.blit(surf_selection_2, self.surf_selection_rect)
        # objective overlay and label - may needed in future - do not delete
        #surface.blit(self.objectangle, rta_dual_height(0.025, 0.025))
        #self.objectivelabel.draw(surface=surface)
        surface.blit(self.chatangle, rta_dual_height(0.025, 0.025))
        for i in self.bars:
            i.draw(surface=surface)
        if globs.fps_meter:
            for i in range(len(self.last_fps)-1):
                self.last_fps[i][1] = self.last_fps[i+1][1]
            self.last_fps[len(self.last_fps)-1][1] = (144 - round(clock.get_fps()))

            pygame.draw.lines(surface, (255, 255, 255), False, self.last_fps, 1)
