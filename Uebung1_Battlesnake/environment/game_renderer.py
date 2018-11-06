import numpy as np
from .game import Game
from environment.models.constants import Color, Direction
from environment.models.faul_fruit import FaulFruit
from environment.models.fruit import Fruit
import pygame


pygame.init()
pygame.font.init()

LEADERBOARD_WIDTH = 300
LEADERBOARD_ITEM_HEIGHT = 100
GAME_PADDING = 30


class GameRenderer:
    """
    Diese Klasse sorgt dafür, dass das Spiel mittels pygame angezeigt werden kann.
    """
    def __init__(self, game_width, game_height, nb_snakes):
        """
        Erstellt ein Fenster für das Spiel
        :param game_width: Spielfeldbreite
        :param game_height: Spielfeldhöhe
        :param nb_snakes: Anzahl der Schlangen im Leaderboard
        """

        self.pixel_per_field = 30

        game_pixel_width = game_width * self.pixel_per_field
        game_pixel_height = game_height * self.pixel_per_field

        leaderboard_pixel_height = nb_snakes*LEADERBOARD_ITEM_HEIGHT

        total_width = GAME_PADDING + game_pixel_width + GAME_PADDING + LEADERBOARD_WIDTH + GAME_PADDING
        total_height = GAME_PADDING + max(game_pixel_height, leaderboard_pixel_height) + GAME_PADDING

        self.screen = pygame.display.set_mode((total_width, total_height))

        pygame.display.set_caption('KI-Labor Battlesnake')

        self.surface_game = pygame.Surface((game_pixel_width, game_pixel_height))
        self.surface_leaderboard = pygame.Surface((LEADERBOARD_WIDTH, leaderboard_pixel_height))

        self.health_bar_rects = None
        self.game_pixel_width = game_pixel_width
        self.game_pixel_height = game_pixel_height
        self.leaderboard_pixel_height = leaderboard_pixel_height

    def display(self, game: Game):
        """
        Zeigt das Spiel an
        :param game: Game Objekt, das angezeigt wird
        :return:
        """

        # Der Hintergrund wird mit schwarz gefüllt
        self.screen.fill((0, 0, 0))

        # Die Spieloberfläche wird gezeichnet
        self.render(game, self.surface_game)
        self.render_leaderboard(game, self.surface_leaderboard)

        game_position = (GAME_PADDING, GAME_PADDING)
        self.screen.blit(self.surface_game, game_position)

        # Das Leaderboard wird gezeichnet
        leaderboard_y_start = GAME_PADDING + max((self.game_pixel_height - self.leaderboard_pixel_height) / 2, 0)
        leaderboard_position = (GAME_PADDING + self.game_pixel_width + GAME_PADDING, leaderboard_y_start)
        self.screen.blit(self.surface_leaderboard, leaderboard_position)

        # Wenn das Spiel gewonnen wurde, Info anzeigen
        if game.is_finished():
            winner = game.get_winner()

            if game.finish_when_winner:
                if winner is not None:
                    message = winner.get_name() + ' hat gewonnen'
                else:
                    message = 'Unentschieden'
            else:
                message = 'Spiel beendet'

            font = pygame.font.Font(None, 40)
            text = font.render(message, True, (255, 255, 255))

            text_rect = text.get_rect()
            text_x = self.screen.get_width() / 2 - text_rect.width / 2
            text_y = self.screen.get_height() / 2 - text_rect.height / 2
            self.screen.blit(text, [text_x, text_y])

        # GUI aktualisieren
        pygame.display.flip()

    def game_to_pixel_coordinates(self, game_x, game_y):
        """
        Umrechnung der Spielfeldkoordinaten in Pixelkoordinaten
        """
        return game_x*self.pixel_per_field, game_y*self.pixel_per_field

    def box_coordinates(self, game_x, game_y):
        """
        Diese Funktion berechnet die Eckpunkte in Pixelkoordinaten eines Feldes
        """
        x_min, y_min = self.game_to_pixel_coordinates(game_x, game_y)
        x_max, y_max = self.game_to_pixel_coordinates(game_x + 1, game_y + 1)
        return x_min, y_min, x_max - 1, y_max - 1

    @staticmethod
    def rotate_points_around_center(pts, cnt, degrees):
        """
        Rotiert die Punkte pts um das Zentrum cnt um die angegebene Gradzahl
        :param pts: Punkte, die rotiert werden sollen
        :param cnt: Zentrum der Rotation
        :param degrees: Grad um die rotiert werden soll
        :return: rotierte Punkte
        """
        ang = degrees / 180*np.pi
        return np.dot(pts - cnt, np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])) + cnt

    @staticmethod
    def flip_points_around_center(pts, cnt, vertical=False, horizontal=False):

        flip_mult = np.eye(2, 2)

        if vertical:
            flip_mult[0, 0] = -1

        if horizontal:
            flip_mult[1, 1] = -1

        return np.dot(pts - cnt, flip_mult) + cnt

    @staticmethod
    def rotate_points(direction: Direction, pts, center):
        """
        Rotiert Punkte, sodass sie anschließend in die Richtung direction ausgerichtet sind
        Grundausrichtung ist Direction.RIGHT
        """

        if direction == Direction.UP:
            return GameRenderer.rotate_points_around_center(pts, center, -90)

        elif direction == Direction.RIGHT:
            return pts

        elif direction == Direction.DOWN:
            return GameRenderer.rotate_points_around_center(pts, center, 90)

        elif direction == Direction.LEFT:
            return GameRenderer.flip_points_around_center(pts, center, vertical=True)

        else:
            print('ERROR unknown head direction')

    def render(self, game: Game, surface: pygame.Surface):
        """
        Visualisierung des Spiels

        :param game: aktuelles Spiel
        :param surface: pygame surface (Fenster)
        """

        surface.fill(Color.background)
        # AUFGABE 1: Implementierung der Battlesnake Oberfläche

        for wall in game.get_walls():
            x_y = self.game_to_pixel_coordinates(wall.x, wall.y)
            # Draw a rectangle outline
            pygame.draw.rect(surface, Color.wall, [x_y[0], x_y[1], self.pixel_per_field, self.pixel_per_field])

        for snake in game.get_snakes():
            for i, body in enumerate(snake.body):
                x_y = self.game_to_pixel_coordinates(body.x, body.y)
                x = x_y[0]
                y = x_y[1]
                pre = self.game_to_pixel_coordinates(snake.body[i - 1].x, snake.body[i - 1].y)
                pre_x = pre[0]
                pre_y = pre[1]
                # 10 pixel
                r = int(self.pixel_per_field / 5)
                if i == 1:
                    if pre_x == x:
                        if pre_y > y:
                            tr1 = [[pre_x, pre_y], [pre_x + self.pixel_per_field - 1, pre_y], [pre_x, pre_y + self.pixel_per_field - 1]]
                            tr2 = [[pre_x + self.pixel_per_field/2 - 1, pre_y], [pre_x + self.pixel_per_field - 1, pre_y], [pre_x + self.pixel_per_field - 1, pre_y + self.pixel_per_field - 1]]
                            circle = [pre_x + r, pre_y + r]
                        else:
                            tr1 = [[x, y], [x + self.pixel_per_field - 1, y], [pre_x, pre_y]]
                            tr2 = [[x + self.pixel_per_field/2 - 1, y], [x + self.pixel_per_field - 1, y], [pre_x + self.pixel_per_field - 1, pre_y]]
                            circle = [x + r, y - r]
                    if pre_y == y:
                        if pre_x > x:
                            tr1 = [[pre_x, pre_y], [pre_x + self.pixel_per_field - 1, pre_y], [pre_x, pre_y + self.pixel_per_field - 1]]
                            tr2 = [[pre_x, pre_y + self.pixel_per_field/2 - 1], [pre_x, pre_y + self.pixel_per_field - 1], [pre_x + self.pixel_per_field - 1, pre_y + self.pixel_per_field - 1]]
                            circle = [pre_x + r, pre_y + r]
                        else:
                            tr1 = [[x, y], [x, y + self.pixel_per_field - 1], [pre_x, pre_y]]
                            tr2 = [[x, y + self.pixel_per_field/2 - 1], [x, y + self.pixel_per_field - 1], [pre_x, pre_y + self.pixel_per_field - 1]]
                            circle = [x - r, y + r]
                    pygame.draw.polygon(surface, snake.color, tr1)
                    pygame.draw.polygon(surface, snake.color, tr2)
                    pygame.draw.rect(surface, snake.color, [x, y, self.pixel_per_field, self.pixel_per_field])
                    pygame.draw.circle(surface, (0, 0, 0), circle, int(r/3))
                if i > 1:
                    if i == len(snake.body) - 1:
                        triangle1 = 0
                        if pre_x == x:
                            if pre_y > y:
                                triangle1 = [[pre_x, pre_y], [pre_x + self.pixel_per_field - 1, pre_y], [x + self.pixel_per_field/2 - 1, y]]
                            else:
                                triangle1 = [[x, y], [x + self.pixel_per_field - 1, y], [x + self.pixel_per_field/2 - 1, y + self.pixel_per_field - 1]]
                        if pre_y == y:
                            if pre_x > x:
                                triangle1 = [[pre_x, pre_y], [pre_x, pre_y + self.pixel_per_field - 1], [x, y + self.pixel_per_field/2 - 1]]
                            else:
                                triangle1 = [[x, y], [x, y + self.pixel_per_field - 1], [x + self.pixel_per_field - 1, y + self.pixel_per_field/2 - 1]]
                        pygame.draw.polygon(surface, snake.color, triangle1)

                    else:
                        pygame.draw.rect(surface, snake.color, [x, y, self.pixel_per_field, self.pixel_per_field])

        fruits = game.get_fruits()
        for fruit in fruits:
            x_y = self.game_to_pixel_coordinates(fruit.x, fruit.y)
            r = int(0.5 * self.pixel_per_field)
            if isinstance(fruit, FaulFruit):
                pygame.draw.circle(surface, Color.fruit, [x_y[0] + r, x_y[1] + r], r-2, 5)
            else:
                pygame.draw.circle(surface, Color.fruit, [x_y[0] + r, x_y[1] + r], r-2)

    def render_leaderboard(self, game: Game, surface: pygame.Surface):
        """
        Leaderboard zeichnen
        :param game: aktuelles Spiel
        :param surface: pygame surface (Fenster)
        """

        surface_width = surface.get_width()

        for i in range(game.number_of_snakes()):
            x_start = 0
            y_start = i*LEADERBOARD_ITEM_HEIGHT

            snake = game.get_snake(i)
            snake_name = snake.get_name()
            snake_health = max(snake.get_health(), 0)
            snake_color = snake.get_color()

            # myfont = pygame.font.SysFont('Comic Sans MS', 30)
            myfont = pygame.font.Font('fonts/karla/Karla-Regular.ttf', 25)
            textsurface = myfont.render(snake_name, True, (255, 255, 255))

            surface.blit(textsurface, (x_start, y_start))

            bar_y_start = y_start + 50

            background_bar_color = GameRenderer.mix_colors(snake_color, Color.background, 0.5)
            background_bar_rect = pygame.Rect(x_start, bar_y_start, surface_width, 30)
            pygame.draw.rect(surface, background_bar_color, background_bar_rect)

            if snake_health > 0:
                bar_rect = pygame.Rect(x_start, bar_y_start, snake_health/100*surface_width, 30)
                pygame.draw.rect(surface, snake_color, bar_rect)

    @staticmethod
    def mix_colors(color_a, color_b, ratio):
        """
        Mischt zwei Farben
        :param color_a:
        :param color_b:
        :param ratio: Verhältnis der Mischung. 0 entsprecht nur Farbe B und 1 nur Farbe A
        :return:
        """
        return ratio * np.array(color_a) + (1 - ratio) * np.array(color_b)