from environment.battlesnake_environment import BattlesnakeEnvironment
from agents.RandomAgent import RandomAgent
from agents.HumanPlayer import HumanPlayer
from agents.FinnAgentO import FinnAgent
from agents.KILabAgent import KILabAgent
import pygame
import time

nb_random_player = 0
num_fruits = 1

agents = [KILabAgent(), FinnAgent()]

for i in range(nb_random_player):
    agents.append(RandomAgent())

env = BattlesnakeEnvironment(
    width=15,
    height=15,
    num_fruits=num_fruits,
    agents=agents,
    act_timeout=0.2
)

env.reset()
env.render()

while True:

    step_start_time = time.time()
    env.handle_input()
    env.step()
    env.render()
    step_time = int((time.time() - step_start_time) * 1000)

    pygame.time.wait(max(0, 250 - step_time))
