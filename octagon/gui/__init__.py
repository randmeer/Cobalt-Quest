import pygame

from octagon.state import State
from octagon.gui import button, label, image
from octagon.utils import var, play_sound, img, mp_screen


class GUI(State):
    def __init__(self, window, background=None, overlay=True, overlay_color=(0, 0, 0), overlay_alpha=160, order=None, invisible_click=False):
        self.window = window
        self.buttons = []
        self.labels = []
        self.images = []
        self.index = {}
        self.event_leftclick_index = {}
        self.event_rightclick_index = {}
        self.event_leftclick_function = None
        self.event_rightclick_function = None
        self.event_keypress_function = None
        self.event_group_leftclick_index = {}  # {"group_id": function}
        self.event_group_rightclick_index = {}  # {"group_id": function}
        self.groups = {}  # {"group_id": [components]}
        self.group_index = {}  # {"component_id": [groups]}
        self.do_exit = False
        self.exit_command = None
        self.silent = False
        self.invisible_click = invisible_click
        if order is None:
            self.render_order = [self.buttons, self.labels, self.images]
        else:
            self.render_order = []
            for i in range(3):
                self.render_order.append(self.__dict__[order[i]])
        if background is None:
            background = img.misc["background"]["menu"]
        self.background = pygame.Surface(var.SIZE, pygame.SRCALPHA)
        self.background.blit(background, (0, 0))
        if overlay:
            overlay_surf = pygame.Surface(var.SIZE)
            overlay_surf.fill(overlay_color)
            overlay_surf.set_alpha(overlay_alpha)
            self.background.blit(overlay_surf, (0, 0))
        self.surface = pygame.Surface(var.SIZE, pygame.SRCALPHA)

    def add_button(self, text="Hello Button!", relsize=(0.3, 0.09), relpos=(0, 0), anchor="topleft", visible=True, id=None, overwrite=False, groups=None):
        bt = button.Button(text=text, relpos=relpos, anchor=anchor, relsize=relsize, visible=visible)
        self.add_component(self.buttons, bt, id, overwrite, groups)

    def add_label(self, text="Hello Label!", relpos=(0, 0), anchor="topleft", color=var.WHITE, double_size=False, id=None, overwrite=False, groups=None):
        lb = label.Label(text=text, relpos=relpos, anchor=anchor, color=color, double_size=double_size)
        self.add_component(self.labels, lb, id, overwrite, groups)

    def add_image(self, surface, relpos=(0, 0), anchor="topleft", id=None, overwrite=False, groups=None):
        im = image.Image(image=surface, relpos=relpos, anchor=anchor)
        self.add_component(self.images, im, id, overwrite, groups)

    def add_component(self, category, component, id=None, overwrite=None, groups=None):
        category.append(component)
        if id is None and groups is not None:
            raise Exception("Components need an ID to be part of a group")
        if id is not None:
            if not overwrite and id in self.index:
                    raise Exception(f"ID '{id}' already in use. To overwrite, set overwrite=True")
            self.index[id] = component
            if groups is not None:
                for i in groups:
                    self.groups[i].append(component)
                self.group_index[id] = groups

    def add_leftclick_events(self, *args):
        """add one or more functions with the name of the button that should trigger them when left-clicked"""
        eventlist = [item for item in args]
        for i in eventlist:
            self.event_leftclick_index[i.__name__] = i

    def add_rightclick_events(self, *args):
        """add one or more functions with the name of the button that should trigger them when right-clicked"""
        eventlist = [item for item in args]
        for i in eventlist:
            self.event_rightclick_index[i.__name__] = i

    def add_leftclick_function(self, function):
        """add a function to call when the left mouse button is pressed"""
        self.event_leftclick_function = function

    def add_rightclick_function(self, function):
        """add a function to call when the right mouse button is pressed"""
        self.event_rightclick_function = function

    def add_keypress_function(self, function):
        """add a function to call when any key is pressed"""
        self.event_keypress_function = function

    def add_group_leftclick_events(self, *args):
        """add a function to call when a button of a group is left-clicked"""
        eventlist = [item for item in args]
        for i in eventlist:
            self.event_group_leftclick_index[i.__name__] = i

    def add_group_rightclick_events(self, *args):
        """add a function to call when a button of a group is right-clicked"""
        eventlist = [item for item in args]
        for i in eventlist:
            self.event_group_rightclick_index[i.__name__] = i

    def add_group(self, *args):
        """add one or more groups with different names"""
        names = [item for item in args]
        for name in names:
            if name in self.groups.keys():
                raise Exception(f"Group {name} already exists")
            self.groups[name] = []

    def get_component(self, component_id):
        """get a specific component by his id"""
        return self.index[component_id]

    def get_group(self, group_id):
        """get all components in a group"""
        return self.groups[group_id]

    def get_group_index(self, component_id):
        """get all groups a component is part of"""
        return self.group_index[component_id]

    def show_overlay(self, overlay_obj, arguments=None):
        if arguments is None:
            arguments = {}
        command = "rerun"
        returnvalue = None
        while command == "rerun":
            overlay = overlay_obj(window=self.window, background=self.surface, arguments=arguments)
            command, returnvalue = overlay.execute()
        if command == "quit":
            self.exit("quit")
        play_sound("click")
        return returnvalue

    def exit(self, command=None):
        self.do_exit = True
        self.exit_command = command

    def draw(self):
        self.surface.blit(self.background, (0, 0))
        for i in range(3):
            for j in self.render_order[i]:
                j.update()
                j.draw(self.surface)
        surf = pygame.transform.scale(self.surface, var.res_size)
        self.window.blit(surf, (0, 0))
        pygame.display.update()

    def get_return(self):
        return self.exit_command

    def execute(self):
        if not self.silent:
            play_sound('click')
        clock = pygame.time.Clock()
        while True:
            clock.tick(30)
            self.mp = mp_screen()
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.exit(command="quit")
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == var.LEFT:
                        for component_id in self.index:
                            if not self.invisible_click and not self.index[component_id].visible:
                                continue
                            if self.index[component_id].rect.collidepoint(self.mp):
                                if component_id in self.event_leftclick_index:
                                    self.event_leftclick_index[component_id]()
                                if component_id in self.group_index:
                                    for group_id in self.group_index[component_id]:
                                        if group_id in self.event_group_leftclick_index:
                                            self.event_group_leftclick_index[group_id](component_id)
                        if self.event_leftclick_function is not None:
                            self.event_leftclick_function(self.mp)

                    if event.button == var.RIGHT:
                        for component_id in self.index:
                            if not self.invisible_click and not self.index[component_id].visible:
                                continue
                            if self.index[component_id].rect.collidepoint(self.mp) and self.index[component_id].visible:
                                if component_id in self.event_rightclick_index:
                                    self.event_rightclick_index[component_id]()
                                if component_id in self.group_index:
                                    for group_id in self.group_index[component_id]:
                                        if group_id in self.event_group_rightclick_index:
                                            self.event_group_rightclick_index[group_id](component_id)
                        if self.event_rightclick_function is not None:
                            self.event_rightclick_function(self.mp)

                elif event.type == pygame.KEYDOWN:
                    if self.event_keypress_function is not None:
                        self.event_keypress_function(event.key)
            if self.do_exit:
                return self.get_return()
            self.draw()


class Overlay(GUI):
    def __init__(self, window, background, arguments, **kwargs):
        super().__init__(window, background, overlay_alpha=200, **kwargs)
        self.args = arguments
        self.exit_args = None

    def get_arg(self, name):
        if name in self.args.keys():
            return self.args[name]
        else:
            return None

    def get_return(self):
        return self.exit_command, self.exit_args

    def exit(self, command=None, arguments=None):
        if arguments is None:
            arguments = {}
        self.exit_args = arguments
        self.do_exit = True
        self.exit_command = command
