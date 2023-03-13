from players.BasePlayer import BasePlayer


class HumanPlayer(BasePlayer):
    def __init__(self, keyboard_input, verbose):
        super().__init__(verbose)
        self.keyboard_input = keyboard_input

    def __str__(self):
        return super().__str__() + f' ({self.keyboard_input})'
