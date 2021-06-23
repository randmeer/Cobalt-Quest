import time

import pygame

from utils import globs
from utils.images import gui_background_texture, background_texture
from sprites import gui
from utils.__init__ import relToAbsDual, setGlobalDefaults, setGameDefaults, setupWindow, resizeWindow, showPauseScreen

class LevelTemplate:

    def __init__(self, name='{name}'):
        """
        level class. inherit in local levelsubclass and draw game on game_surface
        :param name: level name or number
        """
        self.name = name

        setGlobalDefaults()
        setGameDefaults()
        self.window = setupWindow()
        self.background = pygame.transform.scale(background_texture, (globs.height, globs.height))
        self.gui_background = pygame.transform.scale(gui_background_texture, (globs.height, globs.height))
        self.game_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
        self.gui_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
        self.guisprite = gui.GUI()

        self.prev_time = time.time()
        self.resizeupdate = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.auto_render = True
        self.events = []

    def single_loop(self):
        """
        method performs a single loop of the game loop. This can be overridden to add extra functionality before and
        after the game loop and render. call _single_loop() to perform a raw loop and and render() to render stuff out
        """
        self._single_loop()
        self.render()

    def _single_loop(self):
        """
        local method of single_loop
        """
        self.clock.tick(60)
        self.now = time.time()
        delta_time = self.now - self.prev_time
        if delta_time > 1:
            self.delta_time = 0.01
        self.prev_time = self.now

        self.click = False
        mousepos = pygame.mouse.get_pos()

        self.events = list(pygame.event.get())
        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                globs.quitgame = True
            # keyevents
            if event.type == pygame.KEYDOWN:
                # pausekey
                if event.key == pygame.K_ESCAPE:
                    showPauseScreen(window=self.window, mainsurf=self.game_surface)
                    self.resizeupdate = True

            if event.type == pygame.VIDEORESIZE or self.resizeupdate:
                self.resizeupdate = False
                w, h = pygame.display.get_surface().get_size()
                resizeWindow(w, h)
                self.game_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
                self.gui_surface = pygame.Surface(relToAbsDual(1, 1), pygame.SRCALPHA, 32)
                self.background = pygame.transform.scale(background_texture, (relToAbsDual(1, 1)))
                self.gui_background = pygame.transform.scale(gui_background_texture, (relToAbsDual(1, 1)))
                # gui_surface = pygame.transform.scale(gui_surface_original, (relToAbsDual(1, 0.06)))
                self.guisprite.resize()

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
        self.game_surface.blit(self.background, (0, 0))
        self.gui_surface.blit(self.gui_background, relToAbsDual(0, 0))

        self.guisprite.draw(self.gui_surface)
        # game_surface.blit(gui_surface, (0, 0))
        # utils.renderIngameText(game_surface)
        # utils.renderText(window=game_surface, text=str(round(clock.get_fps())) + "",
        #                 position=relToAbsDual(0.92, 0.02),
        #                 color=globs.WHITE, size=relToAbs(0.048))
        self.window.blit(self.game_surface, (0, 0))
        self.window.blit(self.gui_surface, relToAbsDual(1, 0))
        pygame.display.update()
