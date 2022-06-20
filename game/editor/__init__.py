import time
import pygame

from octagon.utils import get_setting, img
from octagon.environment import Environment

from game.floor import Floor
from game.editor import hud
from game.editor.camera import Scene, Camera
from game.editor.entity import EditorEntity
from octagon.environment.camera import Scene as cameraScene
from game import globs
from game.sprite.projectile import shuriken, arrow
from game.sprite.attack import dagger, hands, katana
from game.overlay import pause, inventory, end_screen
from game.editor.entity import Player
from game.editor.entity import Apprentice
from game.sprite.particle import environment
from octagon.utils import mp_screen, img, play_sound
from octagon.utils.static import tuple_subtract, tuple_add, tuple_factor

import time
import pygame
import QuickJSON
import copy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from octagon.utils import render_text, var, img, cout, mp_scene
from octagon.sprites import block

# "id": ["category", "description", max durability/stack_size, leftclick, rightclick]

# blocks = {
    # ""
# }

items = {
    "unset":    ["weapon",      "your hands",                               None,   hands.Punch,        hands.Block],
    "dagger":   ["weapon",      "a very interesting dagger description",    None,   dagger.Stab,        dagger.Swing],
    "katana":   ["weapon",      "a very interesting katana description",    200,    katana.Slash,       katana.Vortex],
    "bow":      ["weapon",      "a very interesting bow description",       100,    arrow.Arrow,        None],
    "rande":    ["weapon",      "test item",                                None,   dagger.Stab,        None],
    "shuriken": ["projectile",  "a very interesting shuriken description",  99,     shuriken.Shuriken,  None],
    "arrow":    ["projectile",  "a very interesting arrow description",     99,     None,               None]
}

class Editor(Environment):
    def __init__(self, window):
        # globs.set_global_defaults()

        # Environment.__init__(self, window,
        #                      f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json",
        #                      f"./data/savegames/{get_setting('current_savegame')}/inventory.json",
        #                      Player,
        #                      [Apprentice],
        #                      items=items)
        envjsonpath = f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json"
        invjsonpath = f"./data/savegames/{get_setting('current_savegame')}/inventory.json"
        entity = [Apprentice]
        self.window = window
        self.items = items
        self.entities = []
        self.surface = pygame.Surface(var.SIZE, pygame.SRCALPHA)
        self.envjson = QuickJSON.QJSON(envjsonpath)
        self.invjson = QuickJSON.QJSON(invjsonpath)
        self.hud = hud.HUD(self)
        self.clock = pygame.time.Clock()

        # index entities and projectiles
        self.PlayerObj = Player
        self.EntityObj = {}
        for i in entity:
            self.EntityObj[str(i.__name__).lower()] = i

        # declare variables for later use
        self.blocks, self.entities, self.particles, self.projectiles, self.melee, self.events, self.pathfinder_grid, self.pathfinder_blocks = [], [], [], [], [], [], [], []
        self.now, self.prev_time, self.delta_time, self.cooldown, self.sidelength = 0, 0, 0, 0, 0
        self.player, self.scene, self.pathfinder = None, None, None
        self.run, self.click = True, False
        self.load()

    def load(self):
        # load environment/inventory json
        self.envjson.load()
        self.invjson.load()
        self.sidelength = self.envjson["size"] * 16 * 2
        self.player = self.PlayerObj(env=self, pos=(self.envjson["player"][0], self.envjson["player"][1]), health=self.invjson["health"], mana=self.invjson["mana"])

        # read and convert blocks to Block()'s in list
        blocks = list(self.envjson["blocks"])
        for i in range(self.envjson["size"] * 2):
            for j in range(self.envjson["size"] * 2):
                if blocks[i][j] != 0:
                    x, y = j - self.envjson["size"], i - self.envjson["size"]
                    if x < 0 and y < 0:
                        pass
                    elif x > 0 and y < 0:
                        x += 1
                    elif x > 0 and y > 0:
                        x += 1
                        y += 1
                    elif x < 0 and y > 0:
                        y += 1
                    self.blocks.append(block.Block(blocks, (i, j), (x, y)))

        # read and convert entitys/projectiles to instances of their classes
        for i in self.envjson["entities"]:
            args = list(i)
            args.pop(0)
            self.entities.append(self.EntityObj[i[0]](env=self, args=args))
        # create scene and set camera target

        self.hud = hud.HUD(self)
        self.particles = []
        self.drag = False
        self.cursor = mp_screen()
        self.target = pygame.Rect((0, 0), var.SIZE)
        self.scene = Scene(self)
        self.scene.camera.follow(self.target)
        self.startpoint = self.scene.camera.rect.topleft

    def _update(self):
        # calculate delta time
        self.now = time.time()
        self.delta_time = self.now - self.prev_time
        self.prev_time = self.now

        # count down cooldown
        if self.cooldown > 0:
            self.cooldown -= self.delta_time

        # update objects
        self.scene.update()
        self.hud.update()

        # handle events
        self.key = pygame.key.get_pressed()
        self.events = list(pygame.event.get())
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.key[pygame.K_F3]:
                        var.soft_debug = not var.soft_debug
                        cout("soft_debug = " + str(var.soft_debug))
                elif event.key == pygame.K_h:
                    if self.key[pygame.K_F3]:
                        var.hard_debug = not var.hard_debug
                        cout("hard_debug = " + str(var.hard_debug))
                elif event.key == pygame.K_g:
                    if self.key[pygame.K_F3]:
                        var.render_all = not var.render_all
                        cout("render_all = " + str(var.render_all))
                elif event.key == pygame.K_f:
                    if self.key[pygame.K_F3]:
                        var.fps_meter = not var.fps_meter
                        cout("fps_meter = " + str(var.fps_meter))

                # elif event.key == pygame.K_1:
                #     self.hud.set_selectangle(0)
                # elif event.key == pygame.K_2:
                #     self.hud.set_selectangle(1)
                # elif event.key == pygame.K_3:
                #     self.hud.set_selectangle(2)
                # elif event.key == pygame.K_4:
                #     self.hud.set_selectangle(3)
                # elif event.key == pygame.K_5:
                #     self.hud.set_selectangle(4)
                # elif event.key == pygame.K_6:
                #     self.hud.set_selectangle(5)
                # elif event.key == pygame.K_x:
                #     self.save()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if self.cooldown <= 0:
            #         if event.button == pygame.BUTTON_LEFT:
            #             # left mousebutton clicked
            #             item = self.items[self.hud.hotbar[self.hud.slot][0]]
            #             if item[3] is not None:
            #                 # this item object will append itself to the correct array and handle cooldown etc.
            #                 item[3](self)

            #         elif event.button == pygame.BUTTON_RIGHT:
            #             # right mousebutton clicked
            #             item = self.items[self.hud.hotbar[self.hud.slot][0]]
            #             if item[4] is not None:
            #                 # this item object will append itself to the correct array and handle cooldown etc.
            #                 item[4](self)

            #     if event.button == pygame.BUTTON_WHEELUP:
            #         self.hud.set_selectangle(self.hud.slot - 1)
            #     elif event.button == pygame.BUTTON_WHEELDOWN:
            #         self.hud.set_selectangle(self.hud.slot + 1)

    def save(self):
        self.envjson["entities"] = []
        for i in self.entities:
            args = i.save()
            if args:
                self.envjson["entities"].append([str(type(i).__name__).lower()] + args)
        self.envjson["player"] = self.player.position
        self.envjson.save()
        self.invjson["health"] = self.player.health
        self.invjson["mana"] = self.player.mana
        self.invjson.save()

    def update(self):
        """
        updates the game surface and handles user input
        """
        mp = pygame.mouse.get_pos()

        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.drag = True
                    self.cursor = mp_screen()
                    self.startpoint = self.scene.camera.rect.topleft
                # if event.button == 4: 
                #     self.scene.zoom *= 1.025
                    # self.target.centerx += (var.SIZE[0] / 2 + mp_screen()[0] - var.SIZE[0] / 2) / 2
                    # self.target.centery += (var.SIZE[1] / 2 + mp_screen()[1] - var.SIZE[1] / 2) / 2

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.drag = False
                # if event.button == 5: 
                #     self.scene.zoom *= 0.975
                    # self.target.centerx += (var.SIZE[0] / 2 + mp_screen()[0] - var.SIZE[0] / 2) / 2
                    # self.target.centery += (var.SIZE[1] / 2 + mp_screen()[1] - var.SIZE[1] / 2) / 2


            elif event.type == pygame.MOUSEMOTION:
                if self.drag:
                    cursorCursorOffset = tuple_subtract(mp_screen(), self.cursor)
                    self.target.topleft = tuple_subtract(self.startpoint, cursorCursorOffset)

            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause.pause_screen(window=self.window, background=self.surface)
                    self.prev_time = time.time()
                elif event.key == pygame.K_e:
                    self.surface.blit(img.misc["background"]["game"], (0, 0))
                    self.scene.draw(self.surface)
                    self.hud.save_hotbar()
                    inventory.show_inventory(window=self.window, background=self.surface, itemdict=self.items)
                    self.hud.load_hotbar()
                    self.hud.update()
                    self.prev_time = time.time()
                # elif event.key == pygame.K_SPACE and self.player.mana > 0:
                #     self.player.dash()

        # end loop if exittomenu order is detected
        if globs.exittomenu:
            self.end_loop()
            globs.menu = True

    def _render(self):
        """
        renders the gui and game surface
        """

        if var.hard_debug:
            surface = pygame.Surface(self.window.get_size())
            surface.blit(pygame.transform.scale(img.misc["background"]["game"], self.window.get_size()), (0, 0))
            self.scene.draw(surface)
            render_text(window=surface, text=str(round(self.clock.get_fps())) + "", pos=(surface.get_width() - 60 , 20), color=var.WHITE, size=20)
        else:

            # background
            x = self.scene.camera.rect.centerx % 255
            y = self.scene.camera.rect.centery % 144
            self.surface.blit(img.misc["background"]["game"], (255-x, 144-y))
            self.surface.blit(img.misc["background"]["game"], (255-x, 144-y-144))
            self.surface.blit(img.misc["background"]["game"], (255-x-255, 144-y))
            self.surface.blit(img.misc["background"]["game"], (255-x-255, 144-y-144))

            self.scene.draw(self.surface)
            self.hud.draw(self.surface)
            surface = pygame.transform.scale(self.surface, var.res_size)

        self.window.blit(surface, (0, 0))
        pygame.display.update()
