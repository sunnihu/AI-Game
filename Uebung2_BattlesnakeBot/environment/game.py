import numpy as np
from typing import List
from environment.models.snake import Snake, SnakePart
from environment.models.game_object import GameObject
from environment.models.fruit import Fruit
from environment.models.wall import Wall
from environment.models.grid_map import GridMap
from environment.models.empty_field import EmptyField
from environment.models.position import Position
from environment.models.constants import Direction


class Game:
    """
    Diese Klasse implementiert die Spiellogik von Snake
    """
    def __init__(self,
                 width,
                 height,
                 num_snakes,
                 num_fruits,
                 finish_when_winner=True
                 ):
        """
        Erstellt ein Game Objekt mit den spezifizierten Parametern
        :param width: Breite des Spielfeldes
        :param height: Höhe des Spielfeldes
        :param num_snakes: Anzahl der Schlangen
        :param num_fruits: Anzahl der Früchte
        :param finish_when_winner: Wenn True, wird das Spiel beendet,
        sobald ein Gewinner fest steht. Ansonsten geht das Spiel weiter, bis alle Snakes gestorben sind
        """
        self.width = width
        self.height = height
        self.objects: List[GameObject] = []
        self.snakes: List[Snake] = []
        self.grid_cache: GridMap = None
        self.finished = False
        self.finish_when_winner = finish_when_winner

        # Wände erzeugen
        for x in range(width):
            for y in range(height):
                if (
                    x == 0
                    or y == 0
                    or x == width - 1
                    or y == height - 1
                ):
                    self._place_wall(x, y)

        self._place_fruits_randomly(num_fruits)
        self._place_snakes_randomly(num_snakes)

    def get_snake(self, snake_idx: int):
        """
        Gibt die Snake mit der ID snake_idx zurück. Die IDs starten bei 0
        :param snake_idx: Index der Snake
        """
        return self.snakes[snake_idx]

    def get_walls(self)-> List[Wall]:
        """
        Gibt alle Wände auf dem Spielfeld zurück
        """
        walls = []

        for game_object in self.objects:
            if isinstance(game_object, Wall):
                walls.append(game_object)

        return walls

    def get_fruits(self)-> List[Fruit]:
        """
        Gibt alle Früchte auf dem Spielfeld zurück
        """
        fruits = []

        for game_object in self.objects:
            if isinstance(game_object, Fruit):
                fruits.append(game_object)

        return fruits

    def number_of_snakes(self)-> int:
        """
        Gibt die Anzahl der Snakes zurück
        """
        return len(self.snakes)

    def get_winner(self):
        """
        Gibt den Gewinner zurück
        :return: None, wenn unentschieden oder das Spiel gespielt wurde, bis die letzte Snake gestorben ist
        """
        if not self.is_finished:
            return None

        snakes_alive = [s for s in self.snakes if s.is_dead() is False]

        if len(snakes_alive) == 1:
            return snakes_alive[0]
        else:
            return None

    def check_finished(self):
        """
        Überprüft, ob das Spiel beendet wurde, weil eine Snake gewonnen hat und es ein Unentschieden gibt.
        """

        snakes_alive = [s for s in self.snakes if s.is_dead() is False]
        if self.finish_when_winner and len(snakes_alive) <= 1:
            self.finished = True
        elif len(snakes_alive) <= 0:
            self.finished = True

    def is_finished(self):
        """
        Gibt zurück, ob das Spiel beendet ist
        """
        return self.finished

    def move_snakes(self, actions: List[Direction])-> bool:
        """
        Bewegt die Schlangen in die angegebenen Richtungen
        Anschließend wird geprüft, ob ein Gewinner fest steht oder es ein Unentschieden gibt

        :param actions: Liste aus Directions, in die sich die Schlangen bewegen sollen
        :return: Gibt zurück, ob das Spiel beendet wurde
        """

        if self.finished:
            return True

        for snake_idx, snake in enumerate(self.snakes):

            action = actions[snake_idx]

            if action is None:
                continue

            snake.move_head(action)

        fruits_eaten = 0

        for snake_idx, snake in enumerate(self.snakes):
            if snake.is_dead():
                continue

            collided = self._collided(snake)
            ate_fruit = self._ate_fruit(snake)
            starved = snake.is_dead()

            if ate_fruit:
                fruits_eaten += 1

            if not collided and not starved:
                if ate_fruit:
                    snake.ate_fruit()

            else:
                snake.die()

        self._place_fruits_randomly(fruits_eaten)

        self.check_finished()
        self._grid_cache_invalidate()

        return self.finished

    def _collided(self, snake: Snake)-> bool:
        """
        Prüft, ob die Schlange mit einer Wand oder einer anderen Schlange kollidiert ist
        :param snake: Schlange, die geprüft wird
        :return: True, wenn die Schlange kollidiert
        """

        snake_head = snake.get_head()

        hit_wall = False
        for game_object in self.objects:
            if Game.is_obstacle(game_object):
                if game_object.same_position(snake_head):
                    hit_wall = True

        hit_snake = False
        for s in self.snakes:
            for s_body_idx, s_body in enumerate(s.body):
                if s_body.same_position(snake_head):
                    if s_body_idx != 0:
                        # wenn die Snake eine andere Snake trifft
                        hit_snake = True
                    else:
                        # Wenn sich zwei Köpfe treffen, gewinnt die längere
                        if snake != s and len(snake.body) <= len(s.body):
                            hit_snake = True

        return hit_wall or hit_snake

    def _ate_fruit(self, snake: Snake)-> bool:
        """
        Prüft, ob die Schlange eine Frucht gegessen hat
        :param snake: Schlange, die geprüft wird
        :return: True, wenn eine Frucht gegessen wurde
        """
        ate_fruit = False
        snake_head = snake.get_head()

        for fruit in self.get_fruits():
            if fruit.same_position(snake_head):
                self.objects.remove(fruit)
                ate_fruit = True

        return ate_fruit

    def _is_available(self, field: Position)-> bool:
        """
        Gibt an ob die Position field noch frei ist
        :param field: Position auf dem Spielfeld
        :return: True, wenn noch nicht von einer Schlange oder einem Objekt blockiert
        """
        if field is None:
            return False

        available = True
        for game_object in self.objects:
            if game_object.same_position(field):
                available = False

        for snake in self.snakes:
            for snake_field in snake.body:

                if snake_field.same_position(field):
                    available = False

        return available

    def _place_wall(self, x: int, y: int):
        """
        Platziert eine Wand bei x, y Koordinaten
        :param x:
        :param y:
        :return:
        """
        wall = Wall(x, y)
        self.objects.append(wall)

    def _place_fruits_randomly(self, nb_fruits: int):
        """
        Platziert Früchte an einer zufälligen Position auf dem Spielfeld
        :param nb_fruits: Anzahl der zufällig zu platzierenden Früchte
        :return:
        """
        padding = 2

        for _ in range(nb_fruits):
            field = None
            while not self._is_available(field):
                x_position = np.random.randint(padding, self.width - padding)
                y_position = np.random.randint(padding, self.height - padding)
                field = Position(x_position, y_position)

            fruit = Fruit(field.x, field.y)
            self.objects.append(fruit)

    def _place_snakes_randomly(self, nb_snakes: int):
        """
        Platziert Schlangen an einer zufälligen Position auf dem Spielfeld
        :param nb_snakes: Anzahl der zu platzierenden Schlangen
        :return:
        """
        padding = 1
        for _ in range(nb_snakes):
            field = None
            while not self._is_available(field):
                x_position = np.random.randint(padding, self.width - padding)
                y_position = np.random.randint(padding, self.height - padding)
                field = Position(x_position, y_position)

            snake = Snake(field.x, field.y)
            self.snakes.append(snake)

    def get_grid(self)-> GridMap:
        if self.grid_cache is None:
            self._grid_cache_build()

        return self.grid_cache

    def _grid_cache_build(self):

        grid_cache: GridMap = GridMap(self.width, self.height)

        for game_object in self.objects:
            grid_cache.set_object(game_object)

        for snake in self.snakes:
            for snake_field in snake.body:
                grid_cache.set_object(snake_field)

        self.grid_cache = grid_cache

    def _grid_cache_invalidate(self):
        self.grid_cache = None

    @staticmethod
    def is_obstacle(game_object: GameObject):
        """
        Prüft, ob das GameObject überwindbar ist oder nicht. Früchte sind z.B. kein Hindernis
        """

        if game_object is None:
            return False

        if isinstance(game_object, EmptyField):
            return False
        elif isinstance(game_object, Wall):
            return True
        elif isinstance(game_object, SnakePart):
            return True
        elif isinstance(game_object, Fruit):
            return False
        else:
            print('unknown game object')
            return None
