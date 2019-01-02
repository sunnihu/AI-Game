from exploration import EpsilonGreedyStrategy
from replay_memory import ReplayMemory
import dqn


def make_agent(args, input_shape, num_actions: int, output_dir: str):
    replay_memory = ReplayMemory(
        max_size=args.replay_buffer_size, batch_size=args.batch_size
    )
    exploration_strategy = EpsilonGreedyStrategy(
        epsilon_max=args.epsilon_max,
        epsilon_min=args.epsilon_min,
        epsilon_decay=args.epsilon_decay,
    )

    hyper_parameters = dqn.HyperParameters(args.learning_rate, args.gamma)

    if args.dueling:
        dqn_class = dqn.make_dqn_dueling
    else:
        dqn_class = dqn.make_dqn

    if args.double:
        agent = dqn.DoubleDQNAgent(
            target_dqn=dqn_class(
                input_shape=input_shape,
                hidden_dim=args.hidden_dim,
                num_actions=num_actions,
            ),
            target_update_rate=args.target_update_rate,
            dqn=dqn_class(
                input_shape=input_shape,
                hidden_dim=args.hidden_dim,
                num_actions=num_actions,
            ),
            replay_memory=replay_memory,
            exploration_strategy=exploration_strategy,
            hyper_parameters=hyper_parameters,
            num_actions=num_actions,
            output_dir=output_dir,
        )
    else:
        agent = dqn.DQNAgent(
            dqn=dqn_class(
                input_shape=input_shape,
                hidden_dim=args.hidden_dim,
                num_actions=num_actions,
            ),
            replay_memory=replay_memory,
            exploration_strategy=exploration_strategy,
            hyper_parameters=hyper_parameters,
            num_actions=num_actions,
            output_dir=output_dir,
        )
    return agent
