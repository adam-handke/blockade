from players.BasePlayer import BasePlayer


class HumanPlayer(BasePlayer):
    def __init__(self, keyboard_input, verbose):
        super().__init__(verbose)
        self.keyboard_input = keyboard_input
        self.current_direction = None

    def __str__(self):
        return super().__str__() + f' ({self.keyboard_input})'

    def get_move(self, game_matrix, possible_moves):
        if self.current_direction in possible_moves:
            return self.current_direction
        else:
            raise ValueError(f'{self}: wrong current_direction: {self.current_direction}')
