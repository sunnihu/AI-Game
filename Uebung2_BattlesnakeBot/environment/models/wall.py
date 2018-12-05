from .game_object import GameObject


class Wall(GameObject):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

