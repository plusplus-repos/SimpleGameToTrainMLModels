import json
import os

from entities.movement_strategies.circular_movement_strategy import CircularMovement
from entities.movement_strategies.diagonal_movement_strategy import DiagonalMovement
from entities.movement_strategies.horizontal_movement_strategy import HorizontalMovement
from entities.movement_strategies.vertical_movement_strategy import VerticalMovement
from levels.level import Level
from entities.enemy import Enemy
from entities.coin import Coin
from entities.wall import Wall
from entities.target_zone import TargetZone


class LevelLoader:
    """
    Static class to load all levels from JSON files.
    """

    @staticmethod
    def load_all_levels():
        """
        Load all levels from JSON files in the specified directory.

        Returns:
            list: A list of loaded levels.
        """
        directory_path = "resources/levels/"
        levels = []
        try:
            for filename in os.listdir(directory_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(directory_path, filename)
                    with open(file_path) as f:
                        level_data = json.load(f)
                        level = Level()
                        level.spawn_x = level_data["spawnX"]
                        level.spawn_y = level_data["spawnY"]
                        level.target_zone = TargetZone(**level_data["targetZone"])

                        for enemy_data in level_data["enemies"]:
                            movement_strategy = LevelLoader.get_movement_strategy(enemy_data["movementType"])
                            enemy = Enemy(
                                x=enemy_data["x"],
                                y=enemy_data["y"],
                                x_max=enemy_data["x_max"],
                                y_max=enemy_data["y_max"],
                                x_min=enemy_data["x_min"],
                                y_min=enemy_data["y_min"],
                                speed=enemy_data["speed"],
                                movement_strategy=movement_strategy
                            )
                            level.add_enemy(enemy)

                        for wall_data in level_data["walls"]:
                            wall = Wall(**wall_data)
                            level.add_wall(wall)

                        for coin_data in level_data["coins"]:
                            coin = Coin(**coin_data)
                            level.add_coin(coin)

                        level.save_initial_state()
                        levels.append(level)
        except Exception as e:
            print(f"Error loading levels from directory {directory_path}: {e}")
        return levels

    @staticmethod
    def get_movement_strategy(strategy_name):
        """
        Get the movement strategy based on the given name.

        Args:
            strategy_name (str): Name of the movement strategy.

        Returns:
            MovementStrategy: An instance of the corresponding movement strategy.

        Raises:
            ValueError: If the strategy name is unknown.
        """
        if strategy_name == "vertical":
            return VerticalMovement()
        elif strategy_name == "horizontal":
            return HorizontalMovement()
        elif strategy_name == "diagonal":
            return DiagonalMovement()
        elif strategy_name == "circular":
            return CircularMovement()
        else:
            raise ValueError(f"Unknown movement strategy: {strategy_name}")


