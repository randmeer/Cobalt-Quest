import time
import pygame

from octagon.utils import get_setting, img
from octagon.environment import Environment

from game import globs
from game.sprite.projectile import shuriken, arrow
from game.sprite.attack import dagger, hands, katana
from game.overlay import pause, inventory, end_screen
from game.sprite.entity.player import Player
from game.sprite.entity.apprentice import Apprentice
from game.sprite.particle import environment


# "id": ["category", "description", max durability/stack_size, leftclick, rightclick]
items = {
    "unset":    ["weapon",      "your hands",                               None,   hands.Punch,        hands.Block],
    "dagger":   ["weapon",      "a very interesting dagger description",    None,   dagger.Stab,        dagger.Swing],
    "katana":   ["weapon",      "a very interesting katana description",    200,    katana.Slash,       katana.Vortex],
    "bow":      ["weapon",      "a very interesting bow description",       100,    arrow.Arrow,        None],
    "rande":    ["weapon",      "test item",                                None,   dagger.Stab,        None],
    "shuriken": ["projectile",  "a very interesting shuriken description",  99,     shuriken.Shuriken,  None],
    "arrow":    ["projectile",  "a very interesting arrow description",     99,     None,               None]
}


class Floor(Environment):

    def __init__(self, window):
        globs.set_global_defaults()
        Environment.__init__(self, window,
                             f"./data/savegames/{get_setting('current_savegame')}/dungeons/{globs.dungeon_str}/{globs.floor_str}.json",
                             f"./data/savegames/{get_setting('current_savegame')}/inventory.json",
                             Player,
                             [Apprentice],
                             items=items)
        self.particles.append(environment.Cinder(env=self))

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
                globs.quitgame = True

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
                elif event.key == pygame.K_SPACE and self.player.mana > 0:
                    self.player.dash()

        # end loop if exittomenu order is detected
        if globs.exittomenu:
            self.end_loop()
            globs.menu = True
