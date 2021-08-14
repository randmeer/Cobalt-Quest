import time
import pygame
from utils import globs, mousepos
from utils.images import background_texture, Texture
from render.sprites import gui
from utils import setGlobalDefaults, setGameDefaults, setupWindow
from gui.overlay import pause_screen

class LevelTemplate:

    def __init__(self, window, name='{name}'):
        """
        level class. inherit in local levelsubclass and draw game on game_surface
        :param name: level name or number
        """
        self.name = name

        setGlobalDefaults()
        setGameDefaults()
        self.window = window
        self.game_surface = pygame.Surface(globs.SIZE, pygame.SRCALPHA)
        self.guisprite = gui.IngameGUI()

        self.prev_time = time.time()
        self.resizeupdate = False
        self.clock = pygame.time.Clock()
        self.run = True
        self.auto_render = True
        self.events = []

        # IGNORE THOSE TEXTURES FOR NOW, BUT WE'LL NEED THEM LATER

        #self.maptex = Texture("resources/textures/map.png")
        #self.playeruptex = Texture("resources/textures/player_animation_up.png")
        #self.playerdowntex = Texture("resources/textures/player_animation_down.png")
        #self.playerrighttex = Texture("resources/textures/player_animation_right.png")
        #self.playerlefttex = Texture("resources/textures/player_animation_left.png")
        #self.playeridletex = Texture("resources/textures/player_animation_idle.png")
        #self.apprenticedowntex = Texture("resources/textures/apprentice_animation_down.png")
        #self.apprenticeuptex = Texture("resources/textures/apprentice_animation_up.png")
        #self.apprenticerighttex = Texture("resources/textures/apprentice_animation_right.png")
        #self.apprenticelefttex = Texture("resources/textures/apprentice_animation_left.png")
        #self.apprenticeidletex = Texture("resources/textures/apprentice_animation_idle.png")
        #self.wielderdowntex = Texture("resources/textures/wielder_animation_down.png")
        #self.wielderuptex = Texture("resources/textures/wielder_animation_up.png")
        #self.wielderrighttex = Texture("resources/textures/apprentice_animation_right.png")
        #self.wielderlefttex = Texture("resources/textures/apprentice_animation_left.png")
        #self.testrun = 0
        #self.testsurf = pygame.Surface((1100, 1100))
        #self.testsurf.fill((255, 255, 255))

    def single_loop(self):
        """
        method performs a single loop of the game loop. This can be overridden to add extra functionality before and
        after the game loop and render. call _single_loop() to perform a raw loop and and render() to render stuff out
        """
        self.game_loop()
        self.render()

    def game_loop(self):
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
                    self.guisprite.set_selectangle(self.guisprite.weapon-1)
                if event.button == pygame.BUTTON_WHEELDOWN:
                    self.guisprite.set_selectangle(self.guisprite.weapon+1)
            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_screen(window=self.window, background=self.game_surface)
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
        self.game_surface.blit(background_texture, (0, 0))
        self.guisprite.draw(self.game_surface)
        surface = pygame.transform.scale(self.game_surface, globs.res_size)
        self.window.blit(surface, (0, 0))

        # utils.renderText(window=game_surface, text=str(round(clock.get_fps())) + "",
        #                 position=relToAbsDual(0.92, 0.02),
        #                 color=globs.WHITE, size=relToAbs(0.048))


        #self.window.blit(self.maptex.get(), (0, 0))
        #self.window.blit(self.testsurf, (0, 0))
        #self.window.blit(self.playerdowntex.get(), (500, self.testrun + 500))
        #self.window.blit(self.playeruptex.get(), (500, 500 - self.testrun))
        #self.window.blit(self.playerrighttex.get(), (self.testrun + 500, 500))
        #self.window.blit(self.playerlefttex.get(), (500 - self.testrun, 500))
        #self.window.blit(self.playeridletex.get(), (500, 500))
        #self.window.blit(self.apprenticedowntex.get(), (500, int(self.testrun/2 + 500)))
        #self.window.blit(self.apprenticeuptex.get(), (500, 500 - int(self.testrun/2)))
        #self.window.blit(self.apprenticerighttex.get(), (int(self.testrun/2) + 500, 500))
        #self.window.blit(self.apprenticelefttex.get(), (int(500 - self.testrun/2), 500))
        #self.window.blit(self.apprenticeidletex.get(), (600, 500))
        #self.window.blit(self.wielderdowntex.get(), (400, int(self.testrun/2 + 500)))
        #self.window.blit(self.wielderuptex.get(), (400, 500 - int(self.testrun/2)))
        #self.testrun += 2
        pygame.display.update()
