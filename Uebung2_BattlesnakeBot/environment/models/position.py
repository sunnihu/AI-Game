

class Position:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def same_position(self, b: 'Position'):
        return self.x == b.x and self.y == b.y

    def to_index(self, width: int):
        return self.y*width + self.x