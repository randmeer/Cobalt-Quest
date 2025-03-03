import time
import pygame
import QuickJSON
import copy
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from octagon.state import State
from octagon.utils import var, cout, mp_scene, play_sound
from octagon.environment import hud, camera
from octagon.environment.object import block, Object


class Environment(State):

    def __init__(self, window: pygame.Surface, envjsonpath: str, invjsonpath: str, player: type, entity: list[type],
                 items: dict, ):
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
        self.items = items
        self.surface = pygame.Surface(var.SIZE, pygame.SRCALPHA)
        self.envjson = QuickJSON.QJSON(envjsonpath)
        self.invjson = QuickJSON.QJSON(invjsonpath)
        self.hud = hud.HUD(self)
        self.clock = pygame.time.Clock()

        # index entities and projectiles
        self.PlayerObj = player
        self.EntityObj = {}
        for i in entity:
            self.EntityObj[str(i.__name__).lower()] = i

        # declare variables for later use
        self.blocks, self.entities, self.particles, self.projectiles, self.melee, self.events, self.pathfinder_grid, self.pathfinder_blocks = [], [], [], [], [], [], [], []
        self.now, self.prev_time, self.delta_time, self.cooldown, self.sidelength = 0, 0, 0, 0, 0
        self.player, self.scene, self.pathfinder = None, None, None
        self.run, self.click = True, False
        self.load()
        self.do_exit = False
        self.exit_command = False

    def show_overlay(self, overlay_obj, arguments=None):
        if arguments is None:
            arguments = {}
        command = "rerun"
        returnvalue = None
        while command == "rerun":
            overlay = overlay_obj(window=self.window, background=self.surface, arguments=arguments)
            command, returnvalue = overlay.execute()
        if command == "quit":
            self.do_exit = True
            self.exit_command = "quit"
        play_sound("click")
        return returnvalue

    def load(self):
        """
        loads the json of the respective floor and creates all the specified
        block & entity classes and the player class
        """

        # load environment/inventory json
        self.envjson.load()
        self.invjson.load()
        self.sidelength = self.envjson["size"] * 16 * 2
        self.player = self.PlayerObj(env=self, pos=(self.envjson["player"][0], self.envjson["player"][1]), health=self.invjson["health"], mana=self.invjson["mana"])

        # read and convert blocks to Block()'s in list
        blocks = list(self.envjson["blocks"])
        """
        for i in range(self.envjson["size"] * 2):
            for j in range(self.envjson["size"] * 2):
                blocks.json[i][j] = random.choice([0, 2])
        """
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

        # pathfinder
        self.pathfinder_blocks = copy.deepcopy(self.envjson["blocks"])
        for i in range(len(self.pathfinder_blocks)):
            for j in range(len(self.pathfinder_blocks)):
                if self.pathfinder_blocks[i][j] == 0:
                    self.pathfinder_blocks[i][j] = 1
                elif self.pathfinder_blocks[i][j] != 0:
                    self.pathfinder_blocks[i][j] = 0
        self.pathfinder_grid = Grid(matrix=self.pathfinder_blocks)
        self.pathfinder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)

        # read and convert entitys/projectiles to instances of their classes
        for i in self.envjson["entities"]:
            args = list(i)
            args.pop(0)
            self.entities.append(self.EntityObj[i[0]](env=self, args=args))
        for i in self.envjson["projectiles"]:
            args = list(i)
            args.pop(0)
            self.projectiles.append(self.items[i[0]][3](env=self, args=args))

        # create scene and set camera target
        self.scene = camera.Scene(self)
        self.scene.camera.follow(target=self.player)

    def save(self):
        self.envjson["entities"] = []
        self.envjson["projectiles"] = []
        for i in self.entities:
            args = i.save()
            if args:
                self.envjson["entities"].append([str(type(i).__name__).lower()] + args)
        for i in self.projectiles:
            args = i.save()
            if args:
                self.envjson["projectiles"].append([str(type(i).__name__).lower()] + args)
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

        # count down cooldown
        if self.cooldown > 0:
            self.cooldown -= self.delta_time

        # update objects
        self.mousepos = mp_scene(scene=self.scene)
        self.scene.update()
        self.hud.update()

        # handle events
        self.key = pygame.key.get_pressed()
        f3 = self.key[pygame.K_F3]
        self.events = list(pygame.event.get())
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if f3:
                    if event.key == pygame.K_b:
                        var.show_hitboxes = not var.show_hitboxes
                        cout("show_hitboxes = " + str(var.show_hitboxes))
                    elif event.key == pygame.K_g:
                        var.debug_scene = not var.debug_scene
                        cout("debug_scene = " + str(var.debug_scene))
                    elif event.key == pygame.K_r:
                        var.render_all = not var.render_all
                        cout("render_all = " + str(var.render_all))
                    elif event.key == pygame.K_i:
                        var.debug_performance = not var.debug_performance
                        cout("debug_performance = " + str(var.debug_performance))
                        self.hud.frametimes = [0, 0]
                    elif event.key == pygame.K_v:
                        var.debug_environment = not var.debug_environment
                        cout("debug_environment = " + str(var.debug_environment))
                    elif event.key == pygame.K_l:
                        self.scene.do_lighting = not self.scene.do_lighting
                        cout("do_lighting = " + str(self.scene.do_lighting))
                    elif event.key == pygame.K_h:
                        var.no_hud = not var.no_hud
                        cout("no_hud = " + str(var.no_hud))
                    elif event.key == pygame.K_f:
                        var.fps_overlay = not var.fps_overlay
                        cout("fps_overlay = " + str(var.fps_overlay))
                elif event.key == pygame.K_1:
                    self.hud.set_selectangle(0)
                elif event.key == pygame.K_2:
                    self.hud.set_selectangle(1)
                elif event.key == pygame.K_3:
                    self.hud.set_selectangle(2)
                elif event.key == pygame.K_4:
                    self.hud.set_selectangle(3)
                elif event.key == pygame.K_5:
                    self.hud.set_selectangle(4)
                elif event.key == pygame.K_6:
                    self.hud.set_selectangle(5)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cooldown <= 0:
                    if event.button == pygame.BUTTON_LEFT:
                        # left mousebutton clicked
                        item = self.items[self.hud.hotbar[self.hud.slot][0]]
                        if item[3] is not None:
                            # this item object will append itself to the correct array and handle cooldown etc.
                            item[3](self)

                    elif event.button == pygame.BUTTON_RIGHT:
                        # right mousebutton clicked
                        item = self.items[self.hud.hotbar[self.hud.slot][0]]
                        if item[4] is not None:
                            # this item object will append itself to the correct array and handle cooldown etc.
                            item[4](self)

                if event.button == pygame.BUTTON_WHEELUP:
                    self.hud.set_selectangle(self.hud.slot - 1)
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    self.hud.set_selectangle(self.hud.slot + 1)

    def update(self):
        pass

    def _render(self):
        """
        renders the gui and game surface
        """

        if var.debug_scene:
            self.scene.draw(self.window)
        else:
            self.scene.draw(self.surface)
            if not var.no_hud:
                self.hud.draw(self.surface)
            self.window.blit(pygame.transform.scale(self.surface, var.res_size), (0, 0))

        pygame.display.update()

    def _single_loop(self):
        """
        method performs a single iteration of the game loop. This can be overridden to add extra functionality before and
        after the game loop and octagon. call _update() to perform a raw iteration and _render() to render stuff out
        """
        self._update()
        self._render()
        self.update()

    def execute(self):
        self.prev_time = time.time()
        self.run = True
        while self.run:
            self.clock.tick(var.FPS)
            self._single_loop()

        self.save()
