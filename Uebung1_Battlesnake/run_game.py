from environment.battlesnake_environment import BattlesnakeEnvironment
from agents.RandomAgent import RandomAgent
from agents.HumanPlayer import HumanPlayer
import pygame

nb_random_player = 2
num_fruits = 1

agents = [HumanPlayer()]

for i in range(nb_random_player):
    agents.append(RandomAgent())

env = BattlesnakeEnvironment(
    width=15,
    height=15,
    num_fruits=num_fruits,
    agents=agents,
)

env.reset()
env.render()

while True:

    env.handle_input()
    env.step()
    env.render()

    pygame.time.wait(250)


