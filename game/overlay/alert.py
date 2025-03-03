from octagon.gui import Overlay


class Alert(Overlay):
    def __init__(self, window, background, arguments):
        super().__init__(window, background, arguments)
        if self.get_arg("message") is None:
            raise Exception("No alert message provided")

        message = self.get_arg("message").split("\n")

        if self.get_arg("question") is not None:
            keyword = self.get_arg("question_keyword")
            if keyword is None:
                keyword = "CONFIRM"
            self.add_button(anchor="center", relsize=(0.2, 0.1), text=keyword, relpos=(0.35, 0.6), id="question_confirm")
            self.add_button(anchor="center", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.65, 0.6), id="question_cancel")
            self.add_leftclick_events()
        else:
            self.add_button(anchor="center", relsize=(0.1, 0.1), text="OK", relpos=(0.5, 0.6), id="ok")

        for i in range(len(message)):
            self.add_label(text=message[i], relpos=(0.5, 0.1 * i + 0.5 - 0.1 * len(message)), anchor="center")

        self.add_leftclick_events(self.ok, self.question_confirm, self.question_cancel)

    def ok(self):
        self.exit()

    def question_confirm(self):
        self.exit(arguments={"confirm": True})

    def question_cancel(self):
        self.exit(arguments={"confirm": False})


'''

def alert(window, background, message, color=(0, 0, 0), question=False, question_keyword="OK"):
    play_sound('alert')
    labels = []
    buttons = []
    for i in range(len(message)):
        labels.append(label.Label(text=message[i], relpos=(0.5, 0.1*i+0.5-0.1*len(message)), anchor="center"))

    if question:
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text=question_keyword, relpos=(0.35, 0.6)))
        buttons.append(button.Button(anchor="center", relsize=(0.2, 0.1), text="CANCEL", relpos=(0.65, 0.6)))
    else:
        buttons.append(button.Button(anchor="center", relsize=(0.1, 0.1), text="OK", relpos=(0.5, 0.6)))

    alert_gui = GUI(background=background, overlay=200, labels=labels, overlaycolor=color, buttons=buttons)
    alert_gui.draw(window=window)
    pygame.display.update()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)
        mp = mp_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globs.quitgame = True
                if question:
                    return False
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == var.LEFT:
                    if alert_gui.buttongroup[0].rect.collidepoint(mp):
                        play_sound('click')
                        run = False
                        if question:
                            return True
                    if question:
                        if alert_gui.buttongroup[1].rect.collidepoint(mp):
                            play_sound('click')
                            return False
            elif event.type == pygame.KEYDOWN:
                if question:
                    return False
                run = False
        alert_gui.draw(window=window)
'''