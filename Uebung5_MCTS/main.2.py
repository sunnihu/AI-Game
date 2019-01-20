from human import Human
from mcts.player import Player
from play import make_env, play


def main():
    player_1 = Player(1, make_env(), simulation_time=1.0)
    # TODO: Uncomment to play against the agent
    # player_2 = Human(-1, make_env())
    player_2 = Player(-1, make_env(), simulation_time=0.1)
    episodes = 1
    play(episodes, player_1, player_2)


if __name__ == "__main__":
    main()
