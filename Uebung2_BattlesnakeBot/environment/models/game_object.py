from .position import Position


class GameObject(Position):

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def __str__(self):
        return '{} ({}, {})'.format(self.__class__.__name__, self.x, self.y)