from environment.connect_four import ConnectFour
from human import Human


def make_env():
    return ConnectFour(6, 7)


def play(episodes, player_1, player_2):
    show_interface = isinstance(player_1, Human) or isinstance(player_2, Human)
    render_mode = "human" if show_interface else "ansi"
    outcomes = []
    for _ in range(episodes):
        environment = make_env()
        environment.render(mode=render_mode)
        while True:
            state = environment.get_state()
            if environment.active_player == player_1.player:
                action = player_1.act(state)
            else:
                action = player_2.act(state)
            environment.step(action)
            environment.render(mode=render_mode)
            outcome = environment.get_outcome()
            if outcome is not None:
                outcomes.append(outcome)
                if render_mode == "human":
                    environment.interface.showOutcome(outcome)
                if outcome == 0:
                    print("Draw!")
                else:
                    print("Player {} wins!".format(outcome))
                break
                
    return outcomes
