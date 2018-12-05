from .game_object import GameObject
from .position import Position
from typing import List
from .empty_field import EmptyField
from .constants import Direction, DirectionUtil

class GridMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_cache: List[List[GameObject]] = [[None for _ in range(height)] for _ in range(width)]

        for x in range(width):
            for y in range(height):
                field = EmptyField(x, y)
                self.set_object(field)

    def is_valid_at(self, x: int, y: int):
        return 0 <= x < self.width and 0 <= y < self.height

    def set_object(self, game_object: GameObject):
        self.grid_cache[game_object.x][game_object.y] = game_object

    def get_object_at_position(self, position: Position):
        return self.get_object_at(position.x, position.y)

    def get_object_at(self, x: int, y: int):
        return self.grid_cache[x][y]

    def get_neighbors(self, x: int, y: int) -> List[GameObject]:
        neighbors = []

        if x >= 1:
            neighbors.append(self.get_object_at(x - 1, y))

        if y >= 1:
            neighbors.append(self.get_object_at(x, y - 1))

        if x <= self.width - 2:
            neighbors.append(self.get_object_at(x + 1, y))

        if y <= self.height - 2:
            neighbors.append(self.get_object_at(x, y + 1))

        return neighbors

    def get_neighbor(self, x: int, y: int, direction: Direction) -> GameObject:

        moved_x, moved_y = DirectionUtil.move(x, y, direction)

        if self.is_valid_at(moved_x, moved_y):
            return self.get_object_at(moved_x, moved_y)
        else:
            return None