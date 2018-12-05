import pygame
import pygame.surfarray
import numpy as np
from settings import Action, Color, FieldType, RenderSettings
from typing import Tuple


class GameRenderer:

    def __init__(self, game_width, game_height):

        pygame.init()

        if RenderSettings.FONT_NAME == None:
            self.font = pygame.font.SysFont(RenderSettings.FONT_NAME, RenderSettings.FONT_SIZE)
            self.info_font = pygame.font.SysFont(RenderSettings.FONT_NAME, RenderSettings.INFO_FONT_SIZE)
        else:
            self.font = pygame.font.Font(RenderSettings.FONT_NAME, RenderSettings.FONT_SIZE)
            self.info_font = pygame.font.Font(RenderSettings.FONT_NAME, RenderSettings.INFO_FONT_SIZE)

        self.game_pixel_width = game_width * RenderSettings.PIXEL_PER_FIELD
        self.game_pixel_height = game_height * RenderSettings.PIXEL_PER_FIELD

        total_width = RenderSettings.GAME_PADDING + self.game_pixel_width + RenderSettings.GAME_PADDING
        total_height = RenderSettings.GAME_PADDING + self.game_pixel_height + RenderSettings.GAME_PADDING + RenderSettings.INFO_HEIGHT

        self.screen = pygame.display.set_mode((total_width, total_height))

        self.surface_game = pygame.Surface((self.game_pixel_width, self.game_pixel_height), pygame.SRCALPHA, 32)
        self.surface_q_values = pygame.Surface((self.game_pixel_width, self.game_pixel_height), pygame.SRCALPHA, 32)
        self.surface_agent = pygame.Surface((self.game_pixel_width, self.game_pixel_height), pygame.SRCALPHA, 32)
        self.surface_info = pygame.Surface((self.game_pixel_width, RenderSettings.INFO_HEIGHT), pygame.SRCALPHA, 32)

        pygame.display.set_caption('KI-Labor GridWorld')

        self.info = {}
        self.hover_areas = {}

    def game_to_pixel_coordinates(self, game_x, game_y) -> Tuple[float, float]:
        return game_x * RenderSettings.PIXEL_PER_FIELD, game_y * RenderSettings.PIXEL_PER_FIELD

    def box(self, game_x: int, game_y: int):
        x_min, y_min = self.game_to_pixel_coordinates(game_x, game_y)
        x_max, y_max = self.game_to_pixel_coordinates(game_x + 1, game_y + 1)
        return pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min)

    def inner_box(self, game_x: int, game_y: int):
        return self.box(game_x, game_y).inflate(-2, -2)

    def center_coordinates(self, game_x: int, game_y: int):
        x_top_left, y_top_left = self.game_to_pixel_coordinates(game_x, game_y)
        x_center, y_center = x_top_left + int(RenderSettings.PIXEL_PER_FIELD / 2), y_top_left + int(RenderSettings.PIXEL_PER_FIELD / 2)
        return x_center, y_center

    def text_coordinates(self, game_x: int, game_y: int, text_surface: pygame.Surface):
        width = text_surface.get_width()
        height = text_surface.get_height()
        center_x, center_y = self.center_coordinates(game_x, game_y)
        return center_x - int(width/2), center_y - int(height/2)

    def triangle(self, game_x: int, game_y: int, action: Action):
        #TODO: For simplicity: can pass rect object and access pygames center and edge methods
        center = self.center_coordinates(game_x, game_y)
        outer_top_left = self.game_to_pixel_coordinates(game_x, game_y)
        outer_top_right = self.game_to_pixel_coordinates(game_x + 1, game_y)
        outer_bottom_left = self.game_to_pixel_coordinates(game_x, game_y + 1)

        inner_top_left = (center[0] - RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD, center[1] - RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD)
        inner_top_right = (center[0] + RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD, center[1] - RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD)
        inner_bottom_left = (center[0] - RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD, center[1] + RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD)
        inner_bottom_right = (center[0] + RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD, center[1] + RenderSettings.ARROW_WIDTH * RenderSettings.PIXEL_PER_FIELD)

        center_top = (outer_top_left[0] + int(RenderSettings.PIXEL_PER_FIELD / 2), outer_top_left[1] + 1)
        center_right = (outer_top_right[0] - 1, outer_top_right[1] + int(RenderSettings.PIXEL_PER_FIELD / 2))
        center_left = (outer_top_left[0] + 1, outer_top_left[1] + int(RenderSettings.PIXEL_PER_FIELD / 2))
        center_bottom = (outer_bottom_left[0] + int(RenderSettings.PIXEL_PER_FIELD / 2), outer_bottom_left[1] - 1)

        if action == Action.UP:
            return [inner_top_left, inner_top_right, center_top]
        elif action == Action.DOWN:
            return [inner_bottom_left, inner_bottom_right, center_bottom]
        elif action == Action.LEFT:
            return [inner_top_left, inner_bottom_left, center_left]
        elif action == Action.RIGHT:
            return [inner_top_right, inner_bottom_right, center_right]

    @staticmethod
    def state_to_game_coordinates(state, board_width):
        row = int(state / board_width)
        col = state - row * board_width
        return col, row

    def update_hover(self, q_value):
        self.info["q"] = q_value
        self.redraw()

    def update_info(self, hyperparameters, epsilon: float):
        self.info["epsilon"] = epsilon
        if hyperparameters is not None:
            self.info["alpha"] = hyperparameters["alpha"]
            self.info["discount"] = hyperparameters["discount"]
        self.redraw()

    def construct_info_text_surface(self):
        string = ""
        if "alpha" in self.info and self.info["alpha"] is not None:
            string += "α: {}   ".format(self.info["alpha"])
        if "discount" in self.info and self.info["discount"] is not None:
            string += "discount: {}   ".format(self.info["discount"])
        if "epsilon" in self.info and self.info["epsilon"] is not None:
            string += "ε: {}   ".format('%.3f' % self.info["epsilon"])
        if "q" in self.info and self.info["q"] is not None:
            string += "Q-Value: {} ".format(self.info["q"])

        return self.info_font.render(string, True, Color.INFO_TEXT)

    def render(self, environment, q_values, finish_state:bool):

        # clear surfaces
        self.screen.fill(Color.BACKGROUND)
        self.surface_game.fill(Color.TRANSPARENT)
        self.surface_q_values.fill(Color.TRANSPARENT)
        self.surface_agent.fill(Color.TRANSPARENT)

        game_board = np.asarray(environment.board.board[0][:][:], dtype=np.float32)
        rewards_board = np.asarray(environment.board.board[1][:][:], dtype=np.float32)
        agent_position = environment.board.position

        agent_image = pygame.image.load(RenderSettings.AGENT_IMAGE_PATH_GOOD)
        agent_image_bad = pygame.image.load(RenderSettings.AGENT_IMAGE_PATH_BAD)
        agent_image = pygame.transform.smoothscale(agent_image, (RenderSettings.AGENT_SIZE, RenderSettings.AGENT_SIZE))
        agent_image_bad = pygame.transform.smoothscale(agent_image_bad, (RenderSettings.AGENT_SIZE, RenderSettings.AGENT_SIZE))

        for (y, x), value in np.ndenumerate(game_board):
            # draw border first
            self.surface_game.fill(Color.BORDER, self.box(x, y), special_flags=pygame.BLEND_RGBA_ADD)
            if value == FieldType.EMPTY:
                self.surface_game.fill(Color.EMPTY_FIELD, self.inner_box(x, y), special_flags=pygame.BLEND_RGBA_ADD)
            elif value == FieldType.END_POS:
                reward = rewards_board[y][x]
                textsurface = self.font.render(str(round(reward, 1)), True, Color.END_POSITION_TEXT)
                if reward >= 0:
                    self.surface_game.fill(Color.END_POSITION_GOOD, self.inner_box(x, y), special_flags=pygame.BLEND_RGBA_ADD)
                else:
                    self.surface_game.fill(Color.END_POSITION_BAD, self.inner_box(x, y), special_flags=pygame.BLEND_RGBA_ADD)
                self.surface_game.blit(textsurface, self.text_coordinates(x, y, textsurface))
            elif value == FieldType.BLOCKED:
                self.surface_game.fill(Color.WALL, self.inner_box(x, y), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                raise Exception(f"Unrecognized board value {value} at {x, y}")

            if agent_position is not None and x == agent_position.x and y == agent_position.y:
                field_x, field_y = self.center_coordinates(x, y)
                if finish_state and rewards_board[y][x] < 0:
                    self.surface_agent.blit(agent_image_bad, (field_x - RenderSettings.AGENT_SIZE/2, field_y - RenderSettings.AGENT_SIZE / 2))
                else:
                    self.surface_agent.blit(agent_image, (field_x - RenderSettings.AGENT_SIZE/2, field_y - RenderSettings.AGENT_SIZE / 2))

        if q_values is not None:

            for (x, y), value in np.ndenumerate(q_values):
                color = Color.for_q_value(value, environment.max_abs_reward_value)
                if color is None:
                    continue

                row = int(x)
                game_coords = self.state_to_game_coordinates(x, environment.board.width)
                bb = pygame.draw.polygon(self.surface_q_values, color, self.triangle(game_coords[0], game_coords[1], environment.action_space[y]))

                # best q value should not be 0.0, because Q is only exactly zero when initialized
                q_row = q_values[row][:]
                best_q_value = np.max(q_row[q_row != 0.0])

                # outline for best action
                # TODO: prettiness can be improved (render order)
                if value == best_q_value:
                    outline_triangle = self.triangle(game_coords[0], game_coords[1], environment.action_space[y])
                    pygame.draw.polygon(self.surface_q_values, Color.BEST_ARROW_OUTLINE, outline_triangle,
                                        RenderSettings.ARROW_OUTLINE_WIDTH)

                # add bounding boxes to dictionary by converting them to a hashable type
                # value is Q-value
                rounded_q = '%.3f' % value
                dict_key = str([bb.x + RenderSettings.GAME_PADDING, bb.y + RenderSettings.GAME_PADDING, bb.w, bb.h])
                self.hover_areas[dict_key] = rounded_q

        self.redraw()

    def redraw(self):

        self.surface_info.fill(Color.BACKGROUND)
        info_text = self.construct_info_text_surface()
        self.surface_info.blit(info_text, (0, int(RenderSettings.INFO_HEIGHT / 2 - info_text.get_height())))
        info_top_left = (RenderSettings.GAME_PADDING, self.screen.get_height() - RenderSettings.GAME_PADDING - RenderSettings.INFO_HEIGHT)

        top_left = (RenderSettings.GAME_PADDING, RenderSettings.GAME_PADDING)
        self.screen.blit(self.surface_game, top_left)
        self.screen.blit(self.surface_q_values, top_left)
        self.screen.blit(self.surface_agent, top_left)
        self.screen.blit(self.surface_info, info_top_left)

        pygame.display.flip()

