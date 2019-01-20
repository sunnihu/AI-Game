import time
import typing

from environment.environment import Environment
from mcts.uct_node import UCTNode


def mcts(
    simulation_time: float, env: Environment, root_node: typing.Optional[UCTNode] = None
) -> UCTNode:
    start_time = time.time()
    root_node = UCTNode(
        state=env.get_state(),
        active_player=env.get_active_player(),
        action=None,
        parent=None,
        num_actions=env.get_num_actions(),
        valid_actions=env.get_valid_actions(),
    )
    while time.time() - start_time < simulation_time:
        leaf_node, winner = root_node.select(env)
        if winner is not None:
            leaf_node.backup(winner)
            continue
        else:
            leaf_node.expand()
            winner = leaf_node.simulate(env)
            leaf_node.backup(winner)
    return root_node
