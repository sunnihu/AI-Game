from gym.envs.registration import register

from .flappy_bird_env import FlappyBirdEnv
from .pong_env import PongEnv
from .frame_stack import FrameStack

register(id="FlappyBird-v0", entry_point="flappy_bird:FlappyBirdEnv")
register(id="PongSmall-v0", entry_point="flappy_bird:PongEnv")
