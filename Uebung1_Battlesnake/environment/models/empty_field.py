from .game_object import GameObject


class EmptyField(GameObject):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)
