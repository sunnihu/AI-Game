from agents.BaseAgent import BaseAgent
import json
import numpy as np

class AgentManager:
    """
    Handles agents. Can load a configuration file and can save an agents state (e.g. Q-values)
    """

    @staticmethod
    def save_agent_state(agent: BaseAgent, filepath: str):
        state = agent.to_dictionary()
        with open(filepath, "w") as file:
            file.write(json.dumps(state))

    @staticmethod
    def load_agent_state(filepath: str):
        with open(filepath, "r") as file:
            return json.loads(file.readline())

    @staticmethod
    def load_q_values(filepath: str) -> np.ndarray:
        with open(filepath, "r") as file:
            list = json.loads(file.readline())["q_values"]
        return np.asarray(list, dtype=np.float32)