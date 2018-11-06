from .game import Game
from agents.BaseAgent import BaseAgent
from typing import List
from environment.models.constants import Color
from .game_renderer import GameRenderer
import pygame
import numpy as np
import sys


class BattlesnakeEnvironment:
    def __init__(
            self,
            width: int,
            height: int,
            num_fruits: int,
            agents: List[BaseAgent]
    ):
        self.width = width
        self.height = height
        self.num_snakes = len(agents)
        self.num_fruits = num_fruits
        self.agents: List[BaseAgent] = agents
        self.game: Game = None
        self.game_renderer = GameRenderer(width, height, self.num_snakes)

    def reset(self):
        self.game = Game(self.width, self.height, self.num_snakes, self.num_fruits)

        default_colors = [
            Color.SNAKE_1_DEFAULT,
            Color.SNAKE_2_DEFAULT,
            Color.SNAKE_3_DEFAULT,
            Color.SNAKE_4_DEFAULT,
        ]

        # Wenn keine eigene Farbe gesetzt ist, Standardfarbe für Snake setzen
        for idx in range(self.num_snakes):
            agent = self.agents[idx]
            snake = self.game.get_snake(idx)

            snake_color = agent.get_color()
            snake_name = agent.get_name(idx)
            if snake_color is None:
                color_index = min(idx, len(default_colors) - 1)
                snake_color = default_colors[color_index]

            snake.set_color(snake_color)
            snake.set_name(snake_name)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                self.user_key_pressed(event.key)

            elif event.type == pygame.QUIT:
                print("Game quit by user!")
                pygame.quit()
                sys.exit()

    def step(self):

        actions = []

        for idx in range(self.num_snakes):
            agent = self.agents[idx]
            snake = self.game.get_snake(idx)

            possible_actions = snake.possible_actions()

            agent_action = None
            if not snake.is_dead():
                selected_agent_action = agent.act(self.game, idx)

                if selected_agent_action in possible_actions:
                    agent_action = selected_agent_action
                else:
                    print('action of snake {} not possible. Select random action'.format(snake.get_name()))
                    agent_action = np.random.choice(possible_actions)

            actions.append(agent_action)

        self.game.move_snakes(actions)

    def render(self):
        self.game_renderer.display(self.game)

    def user_key_pressed(self, key):

        if key == pygame.K_r:
            print('user pressed reset')
            self.reset()
        else:
            for agent in self.agents:
                agent.user_key_pressed(key)
