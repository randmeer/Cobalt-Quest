import time
import pygame
import QuickJSON

from octagon.utils import render_text, rta_dual, var
from octagon.utils import img
from octagon.environment import hud, camera
from octagon.sprites import block
from octagon.sprites.entity import apprentice, player
from octagon.sprites.particle import environment


class Environment:

    def __init__(self, window, envjsonpath, invjsonpath):
        """
        handles logic for player, blocks, entities, particles and more
        automatically calculates delta-time

        main functions:
        load() --> loads floor json
        save() --> saves floor json
        start_loop() --> starts game loop
        end_loop() --> ends game loop

        local functions:
        single_loop() --> runs _update, update and render functions
        _update() --> updates objects, handles input
        render() --> renders objects
        """

        self.window = window
        self.surface = pygame.Surface(var.SIZE, pygame.SRCALPHA)
        self.envjson = QuickJSON.QJSON(envjsonpath)
        self.invjson = QuickJSON.QJSON(invjsonpath)
        self.hud = hud.HUD(invjson=self.invjson)
        self.clock = pygame.time.Clock()

    def load(self):
        """
        loads the json of the respective floor and creates all the specified
        block & entity classes and the player class
        """
        self.blocks, self.entitys, self.particles, self.projectiles, self.melee, self.events = [], [], [], [], [], []
        self.now, self.prev_time, self.delta_time = 0, 0, 0
        self.cooldown, self.sidelength = 0.5, 0
        self.player, self.scene = None, None
        self.run = True
        self.click = False

        # load env json
        self.envjson.load()
        self.invjson.load()
        self.sidelength = self.envjson["size"] * 16 * 2
        self.player = player.Player(particles=self.particles,
                                    pos=(self.envjson["player"][0], self.envjson["player"][1]),
                                    health=self.invjson["health"], mana=self.invjson["mana"])
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
                    self.blocks.append(block.Block(block=blocks[i][j], pos=(x, y)))

        # read and convert entitys to Entity()'s in list
        for i in self.envjson["entitys"]:
            if i[0] == "apprentice":
                self.entitys.append(
                    apprentice.Apprentice(particles=self.particles, pos=(i[1][0], i[1][1]), health=i[2], weapon=i[3],
                                          floorjson=self.envjson))

        # create scene and set camera target
        self.scene = camera.Scene(sidelength=self.sidelength)
        self.scene.camera.follow(target=self.player)

        self.particles.append(environment.Cinder(sidelength=self.sidelength))

    def save(self):
        self.envjson["entitys"] = []
        for i in self.entitys:
            self.envjson["entitys"].append(["apprentice", [i.position[0], i.position[1]], i.health, i.weapon])
        self.envjson["player"] = self.player.position
        self.envjson.save()
        self.hud.save_hotbar()
        self.invjson["health"] = self.player.health
        self.invjson["mana"] = self.player.mana
        self.invjson.save()

    def end_loop(self):
        self.run = False

    def _update(self):
        # calculate delta time
        self.now = time.time()
        self.delta_time = self.now - self.prev_time
        self.prev_time = self.now
        if self.cooldown > 0:
            self.cooldown -= self.delta_time

    def update(self):
        pass

    def render(self):
        """
        renders the gui and game surface
        """

        if var.hard_debug:
            surface = pygame.Surface(self.window.get_size())
            surface.blit(pygame.transform.scale(img.misc["background"]["game"], self.window.get_size()), (0, 0))
            self.scene.draw(surface)
            render_text(window=surface, text=str(round(self.clock.get_fps())) + "", pos=(surface.get_width() - 60 , 20), color=var.WHITE, size=20)
        else:
            self.surface.blit(img.misc["background"]["game"], (0, 0))
            self.scene.draw(self.surface)
            self.hud.draw(self.surface, self.clock)
            render_text(window=self.surface, text=str(round(self.clock.get_fps())) + "", pos=rta_dual(0.92, 0.02), color=var.WHITE)
            surface = pygame.transform.scale(self.surface, var.res_size)

        self.window.blit(surface, (0, 0))
        pygame.display.update()

    def single_loop(self):
        """
        method performs a single iteration of the game loop. This can be overridden to add extra functionality before and
        after the game loop and octagon. call update() to perform a raw iteration and render() to render stuff out
        """
        self._update()
        self.update()
        self.render()

    def start_loop(self):
        self.prev_time = time.time()
        self.run = True
        while self.run:
            self.clock.tick(60)
            self.single_loop()
