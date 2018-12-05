import numpy as np
from .game import Game
from environment.models.constants import Field, Direction
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
    def rotate_points_around_center(pts: np.ndarray, cnt: np.ndarray, degrees: float):
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
    def flip_points_around_center(pts: np.ndarray, cnt: np.ndarray, vertical=False, horizontal=False):

        flip_mult = np.eye(2, 2)

        if vertical:
            flip_mult[0, 0] = -1

        if horizontal:
            flip_mult[1, 1] = -1

        return np.dot(pts - cnt, flip_mult) + cnt

    @staticmethod
    def rotate_points(direction: Direction, pts: np.ndarray, center: np.ndarray):
        """
        Rotiert Punkte um eine Richtung
        Grundausrichtung ist  Direction.RIGHT
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

    def render(self, game, surface: pygame.Surface):

        surface.fill(Field.background)

        # Wände zeichnen
        walls = game.get_walls()
        for wall in walls:
            x_min, y_min, x_max, y_max = self.box_coordinates(wall.x, wall.y)
            pygame.draw.rect(surface, Field.wall, pygame.Rect(x_min, y_min, self.pixel_per_field, self.pixel_per_field))

        # Snakes zeichnen
        for snake_index, snake in enumerate(game.snakes):
            if snake.is_dead():
                continue

            snake_length = snake.length()
            for body_idx in range(snake_length):
                body_part = snake.get_body_part(body_idx)

                snake_color = snake.get_color()
                x_min, y_min, x_max, y_max = self.box_coordinates(body_part.x, body_part.y)

                if body_idx == 0:
                    # Kopf zeichnen

                    # Liste mit Pointen. Achtung im Format (x, y)
                    pts = [
                        [x_min, y_min],
                        [x_max, y_min],
                        [x_max, y_min + 0.1 * self.pixel_per_field],
                        [x_min + self.pixel_per_field * 0.5, y_min + 0.6 * self.pixel_per_field],
                        [x_max, y_max],
                        [x_min, y_max]
                    ]

                    pts = np.array(pts, np.int32)
                    center = np.array((x_min + 0.5 * self.pixel_per_field, y_min + 0.5 * self.pixel_per_field))

                    pts = GameRenderer.rotate_points(body_part.direction, pts, center)
                    pygame.draw.polygon(surface, snake_color, pts)

                    auge_x = int(x_min + 0.2 * self.pixel_per_field)
                    auge_y = int(y_min + 0.2 * self.pixel_per_field)
                    auge_radius = int(0.1 * self.pixel_per_field)
                    auge_center = (auge_x, auge_y)
                    auge_center = np.array(auge_center, np.int32)

                    auge_center = GameRenderer.rotate_points(body_part.direction, auge_center, center).astype(np.int)
                    pygame.draw.circle(surface, Field.background, auge_center, auge_radius)

                elif body_idx == snake_length - 1:
                    # Hinterteil zeichnen

                    # Liste mit Pointen. Achtung im Format (x, y)
                    pts = [
                        [x_max, y_max],
                        [x_min + 0.6*self.pixel_per_field, y_max],
                        [x_min + 0.3*self.pixel_per_field, y_min + 0.5*self.pixel_per_field],
                        [x_min + 0.6*self.pixel_per_field, y_min],
                        [x_max, y_min]
                    ]

                    pts = np.array(pts, np.int32)
                    center = np.array((x_min + 0.5 * self.pixel_per_field, y_min + 0.5 * self.pixel_per_field))
                    tail_direction = snake.get_body_part(body_idx - 1).direction

                    pts = GameRenderer.rotate_points(tail_direction, pts, center)
                    pygame.draw.polygon(surface, snake_color, pts)

                else:
                    pygame.draw.rect(surface, snake_color,
                                     pygame.Rect(x_min, y_min, self.pixel_per_field, self.pixel_per_field))

        # Früchte zeichnen
        fruits = game.get_fruits()
        for fruit in fruits:
            x_min, y_min, x_max, y_max = self.box_coordinates(fruit.x, fruit.y)
            center_x = int((x_min + x_max) / 2)
            center_y = int((y_min + y_max) / 2)
            radius = int(0.8*self.pixel_per_field / 2)
            center = (center_x, center_y)

            pygame.draw.circle(surface, Field.fruit, center, radius)

    def render_leaderboard(self, game: Game, surface: pygame.Surface):
        """
        Leaderboard zeichnen
        :param game: aktuelles Spiel
        :param surface: pygame surface (Fenster)
        :return:
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

            background_bar_color = GameRenderer.mix_colors(snake_color, Field.background, 0.5)
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