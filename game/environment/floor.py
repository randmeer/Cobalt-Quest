import time
import pygame

from octagon.utils import get_setting, img, var
from octagon.environment import Environment

from game import globs
from game.sprite.projectile import shuriken, arrow
from game.sprite.attack import dagger, hands, katana
from game.overlay import pause, inventory, end_screen, console, alert
from game.sprite.entity.player import Player
from game.sprite.entity.apprentice import Apprentice
from game.sprite.particle import environment


def show_floor(window):
    floor = Floor(window=window)
    floor.start_loop()
    if floor.quitgame:
        return "quit"
    return

# "id": ["category", "description", max durability/stack_size, leftclick, rightclick]
items = {
    "unset":    ["weapon",      "your hands",                               None,   hands.Punch,        hands.Block],
    "dagger":   ["weapon",      "a very interesting dagger description",    None,   dagger.Stab,        dagger.Swing],
    "katana":   ["weapon",      "a very interesting katana description",    200,    katana.Slash,       katana.Vortex],
    "bow":      ["weapon",      "a very interesting bow description",       100,    arrow.Arrow,        None],
    "rande":    ["weapon",      "test item",                                None,   dagger.Stab,        None],
    "shuriken": ["projectile",  "a very interesting shuriken description",  99,     shuriken.Shuriken,  None],
    "arrow":    ["projectile",  "a very interesting arrow description",     99,     arrow.Arrow,        None]
}


class Floor(Environment):

    def __init__(self, window):
        Environment.__init__(self, window,
                             f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json",
                             f"./data/savegames/{get_setting('current_savegame')}/inventory.json",
                             Player,
                             [Apprentice],
                             items=items)
        self.particles.append(environment.Cinder(env=self))
        self.quitgame = False

    def update(self):
        """
        updates the game surface and handles user input
        """

        if self.player.health <= 0:
            self.invjson["health"] = 100
            self.invjson["deaths"] += 1
            self.invjson.save()
            end_screen.end_screen(window=self.window, background=self.surface.copy(), end="defeat")
            self.end_loop()

        for event in self.events:
            # quitevent
            if event.type == pygame.QUIT:
                self.end_loop()
                self.quitgame = True

            # keyevents
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_overlay(pause.Pause)
                    self.prev_time = time.time()
                elif event.key == pygame.K_e:
                    self.scene.draw(self.surface)
                    self.hud.save_hotbar()
                    inventory.show_inventory(window=self.window, background=self.surface, itemdict=self.items)
                    self.hud.load_hotbar()
                    self.hud.update()
                    self.prev_time = time.time()
                elif event.key == pygame.K_t:
                    try:
                        exec(console.console(self.window, self.surface))
                    except:
                        alert.Alert(self.window, self.surface, {"message": "THAT DOESN'T SEEM RIGHT..."})

        if globs.quitgame:
            self.end_loop()
            self.quitgame = True