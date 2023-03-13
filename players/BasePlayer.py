class BasePlayer:
    def __init__(self, verbose):
        self.x = None
        self.y = None
        self.verbose = verbose

    def __str__(self):
        return self.__class__.__name__

    def set_starting_coordinates(self, x, y):
        self.x = x
        self.y = y
