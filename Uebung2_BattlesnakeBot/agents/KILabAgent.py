from .BaseAgent import BaseAgent
from environment.game import Game
from environment.models.game_object import GameObject
from environment.models.position import Position
from environment.models.snake import Snake
from environment.models.constants import Direction, ALL_DIRECTIONS, DirectionUtil
from environment.models.grid_map import GridMap
import math
from util.kl_priority_queue import KLPriorityQueue
from typing import List, Tuple, Optional
import numpy as np


class KILabAgent(BaseAgent):

    def act(self, game: Game, snake_idx: int) -> Optional[Direction]:
        snake = game.get_snake(snake_idx)
        all_snacks = game.snakes
        grid_map = game.get_grid()
        opponent = None

        for i, s in enumerate(all_snacks):
            if i == snake_idx:
                continue
            opponent = s

        head = snake.get_head()
        # print('position of head [%d, %d] and direction: %s' % (head.x, head.y, head.direction))
        fruits = game.get_fruits()
        direction = None
        for fruit in fruits:
            cost, path = KILabAgent.a_star_search(game, head, head.direction, fruit, grid_map)
            field = path[0]
            if not opponent.is_dead():
                head_op = opponent.get_head()
                op_to_fruit = abs(head_op.x - fruit.x) + abs(head_op.y - fruit.y)
                to_fruit = abs(head.x - fruit.x) + abs(head.y - fruit.y)
                if snake.length() < opponent.length():
                    if to_fruit > op_to_fruit:
                        f = grid_map.get_object_at(int(game.width/2), int(game.height/2))
                        while game.is_obstacle(f):
                            f = grid_map.get_object_at(f.x + 1, f.y + 1)
                        field = f

            delta_x = head.x - field.x
            delta_y = head.y - field.y
            if delta_y == 0:
                if delta_x > 0:
                    direction = Direction.LEFT
                else:
                    direction = Direction.RIGHT
            if delta_x == 0:
                if delta_y > 0:
                    direction = Direction.UP
                else:
                    direction = Direction.DOWN

        return direction

    @staticmethod
    def a_star_search(game: Game,
                      start_field: Position,
                      start_direction: Direction,
                      search_field: Position,
                      grid_map: GridMap) -> Tuple[int, List[any]]:

        queue = KLPriorityQueue()
        came_from = {}
        cost_so_far = {}
        path = []

        # Initialisierung
        g = 0
        start_field_h = math.sqrt((search_field.x - start_field.x) ** 2 + (search_field.y - start_field.y) ** 2)
        start_field_f = g + start_field_h
        queue.put(start_field_f, start_field)
        cost_so_far[start_field] = g
        # print('=== Position of Start [%d, %d], Determination [%d, %d], Directopn of head: %s ==='
        #      % (start_field.x, start_field.y, search_field.x, search_field.y, start_direction))

        # Schleife
        while not queue.empty():
            # liefert field mit wenigster F-Kosten
            field = queue.get()
            # print('Field with lowest f-cost [%d, %d]' % (field.x, field.y))
            if field.same_position(search_field):
                break
            # print('Not arrive the determination [%d, %d]' % (search_field.x, search_field.y))
            all_neighbors = grid_map.get_neighbors(field.x, field.y)
            neighbors = []
            if field.same_position(start_field):

                if start_direction == Direction.DOWN:
                    for neighbor in all_neighbors:
                        if game.is_obstacle(neighbor):
                            continue
                        if neighbor.y < start_field.y:
                            continue
                        for next_n in grid_map.get_neighbors(neighbor.x, neighbor.y):
                            if game.is_obstacle(next_n):
                                continue
                            neighbors.append(neighbor)

                if start_direction == Direction.UP:
                    for neighbor in all_neighbors:
                        if game.is_obstacle(neighbor):
                            continue
                        if neighbor.y > start_field.y:
                            continue
                        for next_n in grid_map.get_neighbors(neighbor.x, neighbor.y):
                            if game.is_obstacle(next_n):
                                continue
                            neighbors.append(neighbor)

                if start_direction == Direction.LEFT:
                    for neighbor in all_neighbors:
                        if game.is_obstacle(neighbor):
                            continue
                        if neighbor.x > start_field.x:
                            continue
                        for next_n in grid_map.get_neighbors(neighbor.x, neighbor.y):
                            if game.is_obstacle(next_n):
                                continue
                            neighbors.append(neighbor)

                if start_direction == Direction.RIGHT:
                    for neighbor in all_neighbors:
                        if game.is_obstacle(neighbor):
                            continue
                        if neighbor.x < start_field.x:
                            continue
                        for next_n in grid_map.get_neighbors(neighbor.x, neighbor.y):
                            if game.is_obstacle(next_n):
                                continue
                            # if next_n not in game.get_walls():
                            neighbors.append(neighbor)

                # mögliche Nachbarn von start_field untersuchen
                for neighbor in neighbors:
                    if game.is_obstacle(neighbor):
                        continue

                    if neighbor not in cost_so_far.keys():
                        # print('Add new position in {cost_so_far}: [%d, %d]' % (neighbor.x, neighbor.y))
                        cost_so_far[neighbor] = 10000000

                    g = cost_so_far[start_field] + 1
                    if g < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = g
                        # print('Update g-cost to [%d] in position: [%d, %d]' % (g, neighbor.x, neighbor.y))
                        h = math.sqrt((search_field.x - neighbor.x) ** 2 + (search_field.y - neighbor.y) ** 2)
                        f = g + h
                        queue.put(f, neighbor)
                        # print('Add neighbor (%d, %d) in queue with f = %f' % (neighbor.x, neighbor.y, f))
                        came_from[neighbor] = start_field
                        # print('came_from[neighbor(%d, %d)] = start_field(%d, %d)'
                        #      % (neighbor.x, neighbor.y, start_field.x, start_field.y))

            else:

                for neighbor in all_neighbors:
                    if game.is_obstacle(neighbor):
                        continue

                    if neighbor not in cost_so_far.keys():
                        cost_so_far[neighbor] = 10000000
                        # print('Add new position in {cost_so_far}: [%d, %d]' % (neighbor.x, neighbor.y))

                    g = cost_so_far[field] + 1
                    if g < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = g
                        # print('Update g-cost to [%d] in position: [%d, %d]' % (g, neighbor.x, neighbor.y))
                        h = math.sqrt((search_field.x - neighbor.x) ** 2 + (search_field.y - neighbor.y) ** 2)
                        f = g + h
                        queue.put(f, neighbor)
                        # print('Add neighbor (%d, %d) in queue with f = %f' % (neighbor.x, neighbor.y, f))
                        came_from[neighbor] = field
                        # print('came_from[neighbor(%d, %d)] = field(%d, %d)'
                        #      % (neighbor.x, neighbor.y, field.x, field.y))

        # Berechnung des Pfades
        path.append(search_field)
        field = came_from[search_field]
        # print('search_field comes from [%d, %d]' % (field.x, field.y))
        while not field.same_position(start_field):
            pre_field = came_from[field]
            # print('field (%d, %d) comes from pre_field (%d, %d)' % (field.x, field.y, pre_field.x, pre_field.y))
            path.append(field)
            field = pre_field

        cost = cost_so_far[search_field]
        path = path[::-1]
        for i in range(len(path)):
            field = path[i]
            # print('path-%d at field [%d, %d]' % (i, field.x, field.y))

        return cost, path

    def get_name(self, snake_idx: int):
        return 'Sunni Hu'
