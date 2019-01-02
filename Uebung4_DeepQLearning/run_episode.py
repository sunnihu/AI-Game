import gym
from dqn import DQNAgent
from replay_memory import Transition


def run_episode(environment: gym.Env, agent: DQNAgent, render: bool, max_length: int):
    """
    Run one episode in the given environment with the agent.

    Arguments:
        environment {`gym.Env`} -- Environment representing the Markov Decision Process
        agent {`DQNAgent`} -- Reinforcment Learning agent that acts in the envíronment
        render {`bool`} -- Whether the frames of the episode should be rendered on the screen
        max_length {`int`} -- Maximum number of steps before the episode is terminated

    Returns:
        `float` -- Cumulated reward that the agent received during the episode
    """
    episode_reward = 0
    state = environment.reset()
    for _ in range(max_length):
        if render:
            environment.render()
        action = agent.act(state)
        next_state, reward, terminal, _ = environment.step(action)
        agent.observe(
            Transition(state, action, reward, None if terminal else next_state)
        )
        episode_reward += reward
        if terminal:
            break
        else:
            state = next_state
    return episode_reward
