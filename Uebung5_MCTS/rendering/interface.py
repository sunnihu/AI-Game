import pygame
import numpy as np
import sys

class Colors:
    Background = (100,100,100)
    Hover = (100, 200, 100, 200)
    Transparent = (255, 255, 255, 0)

class Constants:
    padding = 20
    pixel_per_cell = 100


class Interface:

    def __init__(self, game_board : np.ndarray):
        self.initialized = False
        pass

    def initialize(self, game_board : np.ndarray):
        pygame.init()

        self.last_area_index = -1

        # load assets
        self.img_red = pygame.image.load('assets/4row_red.png')
        self.img_black = pygame.image.load('assets/4row_black.png')
        self.img_board = pygame.image.load('assets/4row_board.png')

        # scale appropriately
        self.img_red = pygame.transform.smoothscale(self.img_red, (Constants.pixel_per_cell, Constants.pixel_per_cell))
        self.img_black = pygame.transform.smoothscale(self.img_black,
                                                      (Constants.pixel_per_cell, Constants.pixel_per_cell))
        self.img_board = pygame.transform.smoothscale(self.img_board,
                                                      (Constants.pixel_per_cell, Constants.pixel_per_cell))

        self.game_cols = game_board.shape[1]
        self.game_rows = game_board.shape[0]

        self.total_width = 2 * Constants.padding + self.game_cols * Constants.pixel_per_cell
        self.total_height = 2 * Constants.padding + self.game_rows * Constants.pixel_per_cell

        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        self.surface_game = pygame.Surface((self.total_width, self.total_height))
        self.surface_overlay = pygame.Surface((self.total_width, Constants.padding), pygame.SRCALPHA, 32)

        self.hover_areas = []
        for col in range(self.game_cols):
            colRect = pygame.Rect(0, 0, Constants.pixel_per_cell, self.total_height)
            colRect.topleft = (Constants.padding + (col * Constants.pixel_per_cell), 0)
            self.hover_areas.append(colRect)

        pygame.display.set_caption('KI-Labor: 4 Gewinnt')

        pygame.display.flip()

    def render(self, board : np.ndarray):
        if not self.initialized:
            self.initialize(board)
            self.initialized = True

        print(board)
        self.last_board_state = board
        self.surface_game.fill(Colors.Background)

        # draw tokens
        spaceRect = pygame.Rect(0, 0, Constants.pixel_per_cell, Constants.pixel_per_cell)
        for x in range(self.game_cols):
            for y in range(self.game_rows):
                spaceRect.topleft = (Constants.padding + (x * Constants.pixel_per_cell), Constants.padding + (y * Constants.pixel_per_cell))
                if board[y][x] == -1:
                    self.surface_game.blit(self.img_red, spaceRect)
                elif board[y][x] == 1:
                    self.surface_game.blit(self.img_black, spaceRect)

        # draw board over the tokens
        for x in range(self.game_cols):
            for y in range(self.game_rows):
                spaceRect.topleft = (Constants.padding + (x * Constants.pixel_per_cell), Constants.padding + (y * Constants.pixel_per_cell))
                self.surface_game.blit(self.img_board, spaceRect)

        self.screen.blit(self.surface_game, (0, 0))
        pygame.display.flip()

    def highlightArea(self, area_index):
        self.surface_overlay.fill(Colors.Background)
        if area_index is None:
            return

        arrow_width = int (Constants.pixel_per_cell / 5)
        area = self.hover_areas[area_index]
        top_left = (int(area.x + area.w/2 - arrow_width), area.y)
        top_right = (int(area.x + area.w/2 + arrow_width), area.y)
        bottom = (int(area.x + area.w/2), area.y + arrow_width)

        pygame.draw.polygon(self.surface_overlay, Colors.Hover, [top_left, top_right, bottom])

        #self.screen.blit(self.surface_game, (0, 0))
        self.screen.blit(self.surface_overlay, (0, 0))

        pygame.display.flip()


    def showOutcome(self, outcome):
        myfont = pygame.font.SysFont(None, 100)
        if outcome == 0:
            text = "Unentschieden!"
        elif outcome == -1:
            text = "Mensch gewinnt!"
        elif outcome == 1:
            text = "Computer gewinnt!"
        else:
            raise Exception("unknown outcome " + outcome)

        textsurface = myfont.render(text, True, (0, 0, 0), (255, 255, 255))

        self.screen.blit(textsurface, (int(self.total_width / 2) - int(textsurface.get_width() / 2), int(self.total_height/2) - int(textsurface.get_height() / 2)))
        pygame.display.flip()
        pygame.time.wait(5000)
