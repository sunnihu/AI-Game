import os
import json
from environments.Environment import Environment
from environments.Environment import Position
from environments.Board import Board


class EnvironmentLoader:

    def __init__(self, map_directory_path):
        self.base_path = map_directory_path

    def available_environments(self):
        """
        Returns a list of all available maps in the directory
        :return:
        """
        available_maps = []
        for file in os.listdir(self.base_path):
            if file.endswith(".json"):
                available_maps.append(file.rstrip(".json"))

        return available_maps

    def convert_coordinate(self, coordinate):
        """
        Convert single coordinate from list to tuple
        :param coordinate: List of two ints
        :return:
        """
        return Position(coordinate[0], coordinate[1])

    def convert_coordinates(self, coordinate_list, reward_list=None):
        """
        Convert list of coordinates to list of tuples
        :param coordinate_list: List of List of two ints
        :return:
        """
        result = []
        for index, entry in enumerate(coordinate_list):
            if reward_list is not None:
                reward = reward_list[index]
            else:
                reward = None

            result.append(self.convert_coordinate(entry))
        return result

    def load_map(self, map_name: str) -> Environment:
        """
        Loads map with provided map_name from base path
        :param map_name: map name as string (to see all possible maps call available_maps())
        :return: Environment object of map
        """
        # parse json
        filepath = self.base_path + "/" + map_name + ".json"
        print("Loading map: " + filepath)

        with open(filepath, "r") as file:
            data = json.load(file)

        # generate random start position or read the provided start position
        if data["start_position"] == "random":
            start_position = None
        else:
            start_position = self.convert_coordinate(data["start_position"])

        # construct Board object
        board = Board(width=data["width"],
                      height=data["height"],
                      blocked_positions=self.convert_coordinates(data["blocked_positions"]),
                      end_positions=self.convert_coordinates(data["end_positions"]),
                      end_rewards=data["end_rewards"],
                      default_reward=data["default_reward"])

        # construct Environment object
        return Environment(board, start_position)