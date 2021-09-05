import time
import pygame
import QuickJSON

import utils
from utils import globs, mp_scene, get_setting, render_text, rta_dual, angle_deg, conv_deg_rad, set_global_defaults, set_game_defaults
from utils.images import images
from render.sprites import gui, dagger
from render import camera
from logic.gui.overlay import pause_screen, show_inventory
from render.sprites import block, particle_cloud
from render.sprites.entity import player, apprentice
from render.sprites.projectile import shuriken, arrow

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
        self.projectiles = []
        self.melee = []
        self.player = None
        self.now, self.prev_time, self.delta_time = 0, 0, 0
        self.click = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.auto_render = True
        self.events = []
        self.scene = None
        self.cooldown = 0.5

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
        self.scene = camera.Scene(sidelength=self.sidelength)
        self.scene.camera.follow(target=self.player)

    def save(self):
        self.floorjson["entitys"] = []
        for i in self.entitys:
            self.floorjson["entitys"].append(["apprentice", [i.position[0], i.position[1]], i.health, i.weapon])
        self.floorjson["player"] = self.player.position
        self.floorjson.save()
        self.guisprite.save_hotbar()

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
        if self.cooldown > 0:
            self.cooldown -= self.delta_time

        # update objects
        self.click = False
        mp = mp_scene(scene=self.scene)
        self.player.update(blocks=self.blocks, webs=[], particles=self.particles, delta_time=self.delta_time)
        for i in self.entitys:
            i.update(webs=[], blocks=self.blocks, particles=self.particles, projectiles=self.projectiles, player=self.player, delta_time=self.delta_time)
            if i.dead:
                self.entitys.remove(i)
        for i in self.particles:
            i.update(delta_time=self.delta_time, entitys=self.entitys, player=self.player, particles=self.particles)
            x = 0
            for j in i.particles:
                if j.dead:
                    x += 1
                if x == len(i.particles):
                    self.particles.remove(i)
                    break
        for i in self.projectiles:
            i.update(delta_time=self.delta_time, blocks=self.blocks, entitys=self.entitys, particles=self.particles, player=self.player, projectiles=self.projectiles)
            if i.dead:
                self.projectiles.remove(i)
        for i in self.melee:
            i.update(delta_time=self.delta_time, blocks=self.blocks, entitys=self.entitys, particles=self.particles, player=self.player, projectiles=self.projectiles)
            if i.dead:
                self.melee.remove(i)
        self.scene.update(playerentity=self.player, blocks=self.blocks, entitys=self.entitys, particles=self.particles, projectiles=self.projectiles, melee=self.melee)
        self.guisprite.update()

        self.particles.append(particle_cloud.ParticleCloud(center=(self.scene.surface.get_width()/2, 0), radius=self.scene.surface.get_width(),
                                                           particlesize=(1, 1), color=(255, 0, 0), density=1, spawnregion=(2, self.scene.surface.get_height()/2),
                                                           velocity=100, priority=0, no_debug=True, distribution=0.5, colorvariation=100))

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
                if event.button == pygame.BUTTON_LEFT and self.cooldown <= 0:
                    if self.guisprite.hotbar[self.guisprite.slot][1] == "dagger":
                        utils.play_sound('swing')
                        self.melee.append(dagger.Dagger(playerpos=self.player.hitbox.center, mousepos=mp))
                        self.cooldown += 0.5
                    if self.guisprite.hotbar[self.guisprite.slot][2] > 0:
                        if self.guisprite.hotbar[self.guisprite.slot][1] == "shuriken":
                            utils.play_sound('swing')
                            self.projectiles.append(shuriken.Shuriken(exploding=True, pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 0.25
                        elif self.guisprite.hotbar[self.guisprite.slot][1] == "bow":
                            utils.play_sound('swing')
                            self.projectiles.append(arrow.Arrow(pos=self.player.hitbox.center, radians=conv_deg_rad(angle_deg(self.player.hitbox.center, mp))))
                            self.cooldown += 1
                        self.guisprite.hotbar[self.guisprite.slot][2] -= 1
                if event.button == pygame.BUTTON_RIGHT:
                    pass
                if event.button == pygame.BUTTON_WHEELUP:
                    self.guisprite.set_selectangle(self.guisprite.slot - 1)
                if event.button == pygame.BUTTON_WHEELDOWN:
                    self.guisprite.set_selectangle(self.guisprite.slot + 1)
            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(window=self.window, background=self.surface)
                    self.prev_time = time.time()
                elif event.key == pygame.K_e:
                    self.surface.blit(images["background"], (0, 0))
                    self.scene.draw(self.surface)
                    self.guisprite.save_hotbar()
                    show_inventory(window=self.window, background=self.surface)
                    self.guisprite.load_hotbar()
                    self.guisprite.update()
                    self.prev_time = time.time()
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
        self.prev_time = time.time()
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
            surface.blit(pygame.transform.scale(images["background"], self.window.get_size()), (0, 0))
            self.scene.draw(surface)
        else:
            self.surface.blit(images["background"], (0, 0))
            self.scene.draw(self.surface)
            self.guisprite.draw(self.surface)
            render_text(window=self.surface, text=str(round(self.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02),
                        color=globs.WHITE)
            surface = pygame.transform.scale(self.surface, globs.res_size)
        self.window.blit(surface, (0, 0))
        pygame.display.update()
