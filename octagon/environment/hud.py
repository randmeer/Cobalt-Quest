import pygame
from copy import deepcopy

from octagon.gui import label, progress_bar
from octagon.utils import rta_dual, render_multiline_text, img, var, render_text

damage_overlay = pygame.transform.scale(img.misc["overlay"]["damage"], var.SIZE)
mana_overlay = pygame.transform.scale(img.misc["overlay"]["mana"], var.SIZE)


# TODO: fix chat / console


class HUD(pygame.sprite.Sprite):
    def __init__(self, env):
        pygame.sprite.Sprite.__init__(self)
        self.env = env
        self.itemdict = self.env.items
        self.inventory = self.env.invjson
        self.inventory.load()
        self.hotbar, self.rects, self.itemlabels, self.itemtextures = [], [], [], []
        self.load_hotbar()
        self.last_health = self.inventory["health"]
        self.last_mana = self.inventory["mana"]

        # hotbar overlay
        for i in range(len(self.hotbar)):
            self.itemlabels.append(label.Label(text="", anchor="topleft", relpos=(0.578+ i * 0.045 + i * 0.025 + 0.005, 0.93), color=(255, 255, 255)))
        self.update_hotbar()
        self.last_hotbar = self.hotbar
        self.slot = 0
        self.selectangle = img.misc["inventory"]["selection"][0]
        for i in range(len(self.hotbar)):
            rect = pygame.Rect(0, 0, 0, 0)
            rect.size = (14, 14)
            rect.center = (155 + i * 14 + i * 4, 133)  # 14 x 14 textures with 4 pixels space inbetween
            self.rects.append(rect)

        # overlay
        self.overlay = None
        self.overlay_max_alpha = 180

        # chat
        # self.chatangle = pygame.Surface(rta_dual(0.367, 0.805), pygame.SRCALPHA)
        # self.last_chat = var.chat
        # self.update_chat()

        # bars
        self.bars = [progress_bar.ProgressBar(maxvalue=100, relsize=(0.3, 0.0347), relpos=(0.02, 0.940), image=img.misc["bar"]["health"]),
                     progress_bar.ProgressBar(maxvalue=100, relsize=(0.3, 0.0347), relpos=(0.02, 0.895), image=img.misc["bar"]["mana"]),
                     progress_bar.ProgressBar(maxvalue=100, relsize=(0.3, 0.0347), relpos=(0.02, 0.852), image=img.misc["bar"]["progress"])]
        self.bars[0].set(self.inventory["health"])
        self.bars[1].set(self.inventory["mana"])

        # dialogue
        self.show_dialogue_box = False
        self.dialogue = []
        self.dialogue_index = 0
        self.dialogue_sentenceprogress = 0
        self.dialogue_box = pygame.Surface((248, 20))
        self.dialogue_rect = self.dialogue_box.get_rect()
        self.dialogue_rect.midtop = (128, 4)
        self.dialogue_box.fill((0, 0, 0))
        self.dialogue_box.set_alpha(200)
        self.dialogue = ["My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone.", "TEST test TEes MMM sus AMOgS is one too", "good morinigng"]

        # fps-meter
        self.last_fps = []
        for i in range(256):
            self.last_fps.append([i, 144])

        # frametime-meter
        self.frametimes = [0, 0]


    def load_hotbar(self):
        self.inventory.load()
        self.hotbar = self.inventory["hotbar"]

    def save_hotbar(self):
        self.inventory.save()

    def use_slot(self):
        self.hotbar[self.slot][1] -= 1

    def update_hotbar(self):
        for i in range(len(self.hotbar)):
            if self.hotbar[i][1] == 0:
                self.hotbar[i][0] = "unset"
                # self.hotbar[i][1] = self.hotbar[i][3] = -1
                self.itemlabels[i].text = ""
                self.itemlabels[i].render()
            elif self.hotbar[i][1] is not None:
                text = ""
                if self.itemdict[self.hotbar[i][0]][0] == "weapon":
                    # TODO: durability bar
                    text = "__"
                else:
                    text = str(self.hotbar[i][1])
                self.itemlabels[i].text = text
                self.itemlabels[i].render()

        self.itemtextures = []
        for i in self.hotbar:
            if i[0] != "unset":
                self.itemtextures.append(img.item[i[0]])
            else:
                self.itemtextures.append(None)

    # def update_chat(self):
    #     if self.last_chat != var.chat:
    #         self.chatangle.set_alpha(255)
    #         self.chatangle.fill((0, 0, 0, 0))
    #         lastlines = "\n".join(var.chat.splitlines()[-5:])
    #         # set to 19 for full lenght chat, on 5 for now because it looks better ig...
    #         render_multiline_text(surface=self.chatangle, text=lastlines, pos=(0, 0), fadeout="up")
    #     else:
    #         self.chatangle.set_alpha(self.chatangle.get_alpha()-1)
    #     self.last_chat = var.chat

    def start_dialogue(self, dialogue):
        # ["hello", "this is a sentence", "this is another sentence"]
        self.show_dialogue_box = True
        self.dialogue_index = 0
        self.dialogue_sentenceprogress = 0
        self.dialogue = dialogue

    def continue_dialogue(self):
        self.dialogue_sentenceprogress = 0
        self.dialogue_index += 1

    def end_dialogue(self):
        self.show_dialogue_box = False

    def update(self):
        # overlays
        if self.last_health != self.env.player.health:
            if self.overlay is not None:
                self.overlay.set_alpha(self.overlay_max_alpha)
                self.overlay = None
            self.bars[0].set(self.env.player.health, self.env.player.max_health)
            self.overlay = damage_overlay
            self.last_health = self.env.player.health
        if self.last_mana != self.env.player.mana:
            if self.overlay is not None:
                self.overlay.set_alpha(self.overlay_max_alpha)
                self.overlay = None
            self.bars[1].set(self.env.player.mana, self.env.player.max_mana)
            self.overlay = mana_overlay
            self.last_mana = self.env.player.mana
        if self.overlay is not None:
            self.overlay.set_alpha(self.overlay.get_alpha()-5)
            if self.overlay.get_alpha() <= 0:
                self.overlay.set_alpha(self.overlay_max_alpha)
                self.overlay = None

        # hotbar
        if self.hotbar != self.last_hotbar:
            self.update_hotbar()
        self.last_hotbar = deepcopy(self.hotbar)

        # chat
        # self.update_chat()

        # dialogue
        if self.show_dialogue_box:
            for event in self.env.events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if round(self.dialogue_sentenceprogress) >= len(self.dialogue[self.dialogue_index]):
                            self.continue_dialogue()
                        else:
                            self.dialogue_sentenceprogress = len(self.dialogue[self.dialogue_index])
            if self.dialogue_index >= len(self.dialogue):
                self.end_dialogue()
            else:
                self.dialogue_sentenceprogress += self.env.delta_time * 20  # letters per second

    def set_selectangle(self, pos: int):
        self.slot = pos
        if self.slot > len(self.hotbar)-1:
            self.slot = 0
        elif self.slot < 0:
            self.slot = len(self.hotbar) - 1

    def draw(self, surface):

        # overlay
        if self.overlay is not None:
            surface.blit(self.overlay, (0, 0))

        # hotbar
        for i in range(len(self.rects)):
            if self.hotbar[i][0] == "unset":
                surface.blit(img.misc["inventory"]["unset"][1], self.rects[i])
            else:
                surface.blit(img.misc["inventory"][self.itemdict[self.hotbar[i][0]][0]][1], self.rects[i])
            if self.itemtextures[i] is not None:
                surface.blit(self.itemtextures[i], (self.rects[i].x + 2, self.rects[i].y + 2))
        for i in self.itemlabels:
            i.update()
            i.draw(surface=surface)
        surface.blit(self.selectangle, (self.rects[self.slot].x-1, self.rects[self.slot].y-1))

        # chat
        # surface.blit(self.chatangle, rta_dual_height(0.025, 0.025))

        # bars
        for i in self.bars:
            i.draw(surface=surface)

        # dialogue
        if self.show_dialogue_box:
            surface.blit(self.dialogue_box, self.dialogue_rect)
            render_multiline_text(surface, self.dialogue[self.dialogue_index][:round(self.dialogue_sentenceprogress)], (8, 8), True)

        # performance overlay
        if var.debug_performance:
            # fps-meter
            for i in range(len(self.last_fps)-1):
                self.last_fps[i][1] = self.last_fps[i+1][1]
            self.last_fps[len(self.last_fps)-1][1] = (144 - round(self.env.clock.get_fps()))
            pygame.draw.lines(surface, (0, 255, 0), False, self.last_fps, 1)

            # frametime-meter
            if len(self.frametimes) > 1000:
                self.frametimes = self.frametimes[::2]
            self.frametimes.append(self.env.clock.get_rawtime())
            scaled_frametimes = []
            for i in range(256):
                scaled_frametimes.append([i, self.frametimes[int((len(self.frametimes)/256)*i)]])
            pygame.draw.lines(surface, (255, 0, 0), False, scaled_frametimes, 1)
            pygame.draw.line(surface, (255, 0, 0), (240, 8), (256, 8))
            pygame.draw.line(surface, (255, 0, 0), (240, 16), (256, 16))
            render_text(window=surface, text="60", pos=(240, 18), color=(255, 0, 0))
            pygame.draw.line(surface, (255, 0, 0), (240, 33), (256, 33))
            render_text(window=surface, text="30", pos=(240, 35), color=(255, 0, 0))
            pygame.draw.line(surface, (255, 0, 0), (240, 66), (256, 66))
            render_text(window=surface, text="15", pos=(240, 68), color=(255, 0, 0))
            pygame.draw.line(surface, (255, 0, 0), (240, 133), (256, 133))
            render_text(window=surface, text="7", pos=(240, 135), color=(255, 0, 0))

            # performance
            render_text(window=surface, text="ENTITIES: " + str(len(self.env.entities)), pos=(0, 0))
            render_text(window=surface, text="PROJECTILES: " + str(len(self.env.projectiles)), pos=(0, 8))
            render_text(window=surface, text="MELEE: " + str(len(self.env.melee)), pos=(0, 16))
            render_text(window=surface, text="PARTICLES: " + str(len(self.env.particles)), pos=(0, 24))
            render_text(window=surface, text="BLOCKS: " + str(len(self.env.blocks)), pos=(0, 32))
            render_text(window=surface, text="FRAME TIME: " + str(self.env.clock.get_rawtime()), pos=(0, 40), color=(255, 0, 0))
            render_text(window=surface, text="FRAMES PER SECOND: " + str(round(self.env.clock.get_fps())), pos=(0, 48), color=(0, 255, 0))
            render_text(window=surface, text="FPS LIMIT: " + str(var.FPS), pos=(0, 56), color=(0, 255, 0))

        # environment overlay
        if var.debug_environment:
            render_text(window=surface, text="ENV SIZE: " + str(self.env.sidelength), pos=(0, 90))
            render_text(window=surface, text="PLAYER HITBOX CENTER: " + str(self.env.player.hitbox.center), pos=(0, 98))
            render_text(window=surface,
                        text="PLAYER VELOCITY: " + str(round(self.env.player.move_vector.length())) + " PPS",
                        pos=(0, 106))

        # fps overlay
        if var.fps_overlay:
            render_text(window=surface, text=str(round(self.env.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02))
