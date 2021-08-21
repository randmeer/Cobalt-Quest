import time
import pygame
import QuickJSON

import utils
from utils import globs, mousepos, get_setting, render_text, rta_dual
from utils.images import bg_tx
from render.sprites import gui
from render import camera
from utils import set_global_defaults, set_game_defaults
from logic.gui.overlay import pause_screen
from render.sprites import block
from render.sprites.entity import player


# Template for handling game logic in a single floor of a dungeon
class Floor:

    def __init__(self, window):
        """
        level class. inherit in local levelsubclass and draw game on game_surface
        :param name: level name or number
        """
        # self.name = name

        set_global_defaults()
        #set_game_defaults()
        self.window = window
        self.surface = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
        self.guisprite = gui.IngameGUI()

        self.floorjson = QuickJSON.QJSON(path=f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json")
        self.sidelength = 0
        self.blocks = []
        self.entitys = []
        self.player = None

        self.now, self.prev_time, self.delta_time = 0, 0, 0
        self.resizeupdate = False
        self.click = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.auto_render = True
        self.events = []
        self.scene = None
        print("[Floor] initialized Floor")

    def load(self):
        """
        loads the json of the respective floor and creates all the specified
        block & entity classes and the player class
        """
        self.floorjson.load()
        self.sidelength = self.floorjson["size"] * 16 * 2
        self.player = player.Player(pos=(self.floorjson["player"][0], self.floorjson["player"][1]))
        test = list(self.floorjson["blocks"])
        for i in range(self.floorjson["size"]*2):
            for j in range(self.floorjson["size"]*2):
                if test[i][j] != 0:
                    x, y = j-self.floorjson["size"], i-self.floorjson["size"]
                    if x < 0 and y < 0:
                        pass
                    elif x > 0 and y < 0:
                        x += 1
                    elif x > 0 and y > 0:
                        x += 1
                        y += 1
                    elif x < 0 and y > 0:
                        y += 1
                    self.blocks.append(block.Block(block=test[i][j], pos=(x, y)))

        for i in self.floorjson["entitys"]:
            pass
        self.scene = camera.Scene(path=f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json", sidelength=self.sidelength)
        self.scene.camera.follow(target=self.player)
        print("[Floor] loaded floor json")

    def save(self):
        self.floorjson.save()

    def single_loop(self):
        """
        method performs a single iteration of the game loop. This can be overridden to add extra functionality before and
        after the game loop and render. call update() to perform a raw iteration and and render() to render stuff out
        """
        self.update()
        self.render()

    def update(self):
        """
        updates the game surface
        """
        self.clock.tick(60)
        self.now = time.time()
        delta_time = self.now - self.prev_time
        if delta_time > 1:
            self.delta_time = 0.01
        self.prev_time = self.now

        self.click = False
        mp = mousepos()

        self.player.update(blocks=self.blocks, webgroup=[], scene=self.scene.surface)

        self.scene.update(playerentity=self.player, blocks=self.blocks, entitys=self.entitys)

        self.events = list(pygame.event.get())
        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True
            # buttonevents
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    pass
                if event.button == pygame.BUTTON_RIGHT:
                    pass
                if event.button == pygame.BUTTON_WHEELUP:
                    self.guisprite.set_selectangle(self.guisprite.weapon - 1)
                if event.button == pygame.BUTTON_WHEELDOWN:
                    self.guisprite.set_selectangle(self.guisprite.weapon + 1)
            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(window=self.window, background=self.surface)
                    self.resizeupdate = True
                if event.key == pygame.K_e:
                    pass
                if event.key == pygame.K_1:
                    self.guisprite.set_selectangle(0)
                if event.key == pygame.K_2:
                    self.guisprite.set_selectangle(1)
                if event.key == pygame.K_3:
                    self.guisprite.set_selectangle(2)
                if event.key == pygame.K_4:
                    self.guisprite.set_selectangle(3)
                if event.key == pygame.K_5:
                    self.guisprite.set_selectangle(4)
                if event.key == pygame.K_6:
                    self.guisprite.set_selectangle(5)
            # if event.type == pygame.VIDEORESIZE or self.resizeupdate:
            #     self.resizeupdate = False
            #     w, h = pygame.display.get_surface().get_size()
            #     resizeWindow(w, h)
            #     self.game_surface = pygame.Surface(pygame.display.get_window_size(), pygame.SRCALPHA, 32)
            #     self.background = pygame.transform.scale(background_texture, (relToAbsDual(1, 1)))
            #     self.guisprite.resize()
        self.guisprite.update()

        if globs.exittomenu:
            self.end_loop()
            globs.menu = True

    def start_loop(self):
        self.run = True
        while self.run:
            self.single_loop()

    def end_loop(self):
        self.run = False

    def render(self):
        """
        renders the gui and game surface
        """
        if globs.debug:
            surface = pygame.Surface(self.window.get_size())
            surface.blit(pygame.transform.scale(bg_tx, self.window.get_size()), (0, 0))
            self.scene.draw(surface)
        else:
            self.surface.blit(bg_tx, (0, 0))
            self.scene.draw(self.surface)
            self.guisprite.draw(self.surface)
            render_text(window=self.surface, text=str(round(self.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02), color=globs.WHITE)
            surface = pygame.transform.scale(self.surface, globs.res_size)
        self.window.blit(surface, (0, 0))
        pygame.display.update()
