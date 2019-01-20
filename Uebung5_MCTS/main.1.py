import numpy as np

from play import make_env, play
from evaluation.player import Player
from evaluation.random_player import RandomPlayer
from human import Human


def main():
    player_1 = Player(1, make_env())
    # TODO: Uncomment to play against the agent
    #player_2 = Human(-1, make_env())
    player_2 = RandomPlayer(-1, make_env())
    episodes = 50
    outcomes = play(episodes, player_1, player_2)
    print("Score: {}".format(np.mean(outcomes)))


if __name__ == "__main__":
    main()
