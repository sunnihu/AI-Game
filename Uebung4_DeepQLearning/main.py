from collections import namedtuple
import json
import datetime

import gym
import numpy as np
from tensorboardX import FileWriter, summary

from run_episode import run_episode
from make_agent import make_agent


def main(exercise: str = "Aufgabe-2"):

    with open("./config.{}.json".format(exercise), mode="r") as f:
        args = json.load(
            f, object_hook=lambda d: namedtuple("X", d.keys())(*d.values())
        )

    environment = gym.make(args.env)

    input_shape = environment.observation_space.shape
    num_actions = environment.action_space.n

    output_directory = "./tmp/{}/{}".format(exercise, datetime.datetime.now())

    writer = FileWriter(output_directory)

    agent = make_agent(args, input_shape, num_actions, output_directory)

    rewards = []
    for episode in range(args.episodes):
        episode_rewards = run_episode(
            environment,
            agent,
            render=episode % args.render_episode_interval == 0,
            max_length=args.max_episode_length,
        )
        rewards.append(episode_rewards)
        if episode % args.training_interval == 0:
            for _ in range(args.training_interval):
                loss = agent.train()

            if loss and episode % (args.training_interval * 10) == 0:
                mean_rewards = np.mean(rewards)
                std_rewards = np.std(rewards)
                writer.add_summary(
                    summary=summary.scalar("dqn/loss", loss), global_step=episode
                )
                writer.add_summary(
                    summary=summary.scalar("rewards/mean", mean_rewards),
                    global_step=episode,
                )
                writer.add_summary(
                    summary=summary.scalar("rewards/standard deviation", std_rewards),
                    global_step=episode,
                )
                writer.add_summary(
                    summary=summary.scalar(
                        "dqn/epsilon", agent.exploration_strategy.epsilon
                    ),
                    global_step=episode,
                )
                print(
                    "Episode {}\tMean rewards {:f}\tLoss {:f}\tEpsilon {:f}".format(
                        episode, mean_rewards, loss, agent.exploration_strategy.epsilon
                    )
                )
                rewards.clear()

