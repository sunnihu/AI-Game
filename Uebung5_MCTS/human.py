import numpy as np

from environment.connect_four import ConnectFour
from mcts.mcts import mcts

import sys
import pygame

class Human:
    def __init__(self, player: int, simulation_env: ConnectFour):
        self.simulation_env = simulation_env
        self.player = player
        self.interface = simulation_env.interface

    def act(self, state: np.ndarray):
        self.simulation_env.reset(state, self.player)
        self.simulation_env.render("human")
        column = self.handleUserInteraction()

        return column


    def handleUserInteraction(self):
        print("USER TURN")
        while True:
            active_area = None
            for index, area in enumerate(self.interface.hover_areas):
                if self.simulation_env.get_valid_actions()[index] != 1:
                    continue

                if area.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    active_area = self.interface.hover_areas.index(area)

            self.interface.highlightArea(active_area)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONUP:
                    if active_area is not None:
                        return active_area



        pass