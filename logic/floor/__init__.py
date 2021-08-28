import time
import pygame
import QuickJSON

import utils
from utils import globs, mp_scene, get_setting, render_text, rta_dual, angle_deg, conv_deg_rad
from utils.images import bg_tx
from render.sprites import gui, shuriken
from render import camera
from utils import set_global_defaults, set_game_defaults
from logic.gui.overlay import pause_screen
from render.sprites import block, particle_cloud
from render.sprites.entity import player, apprentice


class Floor:

    def __init__(self, window):
        """
        game logic for a single floor of a dungeon

        main functions:
        load() --> loads floor json
        save() --> saves floor json
        start_loop() --> starts game loop
        end_loop() --> ends game loop

        local functions:
        single_loop() --> runs update and render functions
        update() --> updates objects, handles input
        render() --> renders objects
        """
        set_global_defaults()
        self.window = window
        self.surface = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
        self.guisprite = gui.IngameGUI()

        self.floorjson = QuickJSON.QJSON(
            path=f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json")
        self.sidelength = 0
        self.blocks = []
        self.entitys = []
        self.particles = []
        self.othersprites = []
        self.player = None

        self.now, self.prev_time, self.delta_time = 0, 0, 0
        self.resizeupdate = False
        self.click = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.auto_render = True
        self.events = []
        self.scene = None

    def load(self):
        """
        loads the json of the respective floor and creates all the specified
        block & entity classes and the player class
        """

        # load floor json
        self.floorjson.load()
        self.sidelength = self.floorjson["size"] * 16 * 2
        self.player = player.Player(pos=(self.floorjson["player"][0], self.floorjson["player"][1]))

        # read and convert blocks to Block()'s in list
        blocks = list(self.floorjson["blocks"])
        for i in range(self.floorjson["size"] * 2):
            for j in range(self.floorjson["size"] * 2):
                if blocks[i][j] != 0:
                    x, y = j - self.floorjson["size"], i - self.floorjson["size"]
                    if x < 0 and y < 0:
                        pass
                    elif x > 0 and y < 0:
                        x += 1
                    elif x > 0 and y > 0:
                        x += 1
                        y += 1
                    elif x < 0 and y > 0:
                        y += 1
                    self.blocks.append(block.Block(block=blocks[i][j], pos=(x, y)))

        # read and convert entitys to Entity()'s in list
        for i in self.floorjson["entitys"]:
            if i[0] == "apprentice":
                self.entitys.append(apprentice.Apprentice(pos=(i[1][0], i[1][1]), health=i[2], weapon=i[3]))

        # create scene and set camera target
        self.scene = camera.Scene(path=f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json", sidelength=self.sidelength)
        self.scene.camera.follow(target=self.player)

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
        updates the game surface and handles user input
        """

        # calculate delta time
        self.clock.tick(60)
        self.now = time.time()
        self.delta_time = self.now - self.prev_time
        self.prev_time = self.now

        # update objects
        self.click = False
        mp = mp_scene(scene=self.scene)
        self.player.update(blocks=self.blocks, webs=[], particles=self.particles, delta_time=self.delta_time)
        for i in self.entitys:
            i.update(webs=[], blocks=self.blocks)
        for i in self.particles:
            i.update(delta_time=self.delta_time)
            for j in i.particles:
                if j.dead:
                    self.particles.remove(i)
                    break
        for i in self.othersprites:
            i.update(delta_time=self.delta_time, blocks=self.blocks, particles=self.particles)
        self.scene.update(playerentity=self.player, blocks=self.blocks, entitys=self.entitys, particles=self.particles, othersprites=self.othersprites)
        self.guisprite.update()

        # handle events
        key = pygame.key.get_pressed()
        self.events = list(pygame.event.get())
        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True
            # buttonevents
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.guisprite.weapons[self.guisprite.weapon][0] == "dagger":
                        self.player.start_swing(scene=self.scene)
                        utils.play_sound('swing')
                    if self.guisprite.weapons[self.guisprite.weapon][0] == "shuriken":
                        self.othersprites.append(shuriken.Shuriken(pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
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
                elif event.key == pygame.K_b:
                    if key[pygame.K_F3]:
                        globs.soft_debug = not globs.soft_debug
                elif event.key == pygame.K_e:
                    pass
                elif event.key == pygame.K_1:
                    self.guisprite.set_selectangle(0)
                elif event.key == pygame.K_2:
                    self.guisprite.set_selectangle(1)
                elif event.key == pygame.K_3:
                    self.guisprite.set_selectangle(2)
                elif event.key == pygame.K_4:
                    self.guisprite.set_selectangle(3)
                elif event.key == pygame.K_5:
                    self.guisprite.set_selectangle(4)
                elif event.key == pygame.K_6:
                    self.guisprite.set_selectangle(5)

        # end loop if exittomenu order is detected
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

        if globs.hard_debug:
            surface = pygame.Surface(self.window.get_size())
            surface.blit(pygame.transform.scale(bg_tx, self.window.get_size()), (0, 0))
            self.scene.draw(surface)
        else:
            self.surface.blit(bg_tx, (0, 0))
            self.scene.draw(self.surface)
            self.guisprite.draw(self.surface)
            render_text(window=self.surface, text=str(round(self.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02),
                        color=globs.WHITE)
            surface = pygame.transform.scale(self.surface, globs.res_size)
        self.window.blit(surface, (0, 0))
        pygame.display.update()
