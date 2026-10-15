import config
from Environment import Environment
from enums.CellType import CellType
from enums.EnvironmentEvent import EnvironmentEvent
from custom_types.QStateType import QStateType
from utils.check_cell_in_board import check_cell_in_board


class Interpreter:
    env: Environment

    def __init__(self, env: Environment):
        self.env = env

    def get_reward(self, event: EnvironmentEvent) -> int:
        match event:
            case (EnvironmentEvent.EATEN_GREEN_APPLE
                  | EnvironmentEvent.BOARD_FULL):
                return config.GREEN_APPLE_REWARD
            case EnvironmentEvent.EATEN_RED_APPLE:
                return config.RED_APPLE_REWARD
            case EnvironmentEvent.DIED:
                return config.DEATH_REWARD
        return config.NOTHING_REWARD

    def __is_danger(self, x, y):
        if not check_cell_in_board(self.env.game_config.board_size, x, y):
            return 1

        if self.env.board[x][y] == CellType.SNAKE:
            return 1

        if self.env.board[x][y] == CellType.RED_APPLE:
            return 1
        return 0

    def __get_green_apple_distance(self, dx, dy):
        distance = 1
        while True:
            # Get the coordinates of the cell in the given
            # direction at the current distance
            nx = self.env.snake_head[0] + (dx * distance)
            ny = self.env.snake_head[1] + (dy * distance)

            # If we are out of the board -> no green apple seen
            if not check_cell_in_board(self.env.game_config.board_size, nx,
                                       ny):
                return 0

            cell = self.env.board[nx][ny]

            # If we see a Snake or a Red Apple -> stop searching because danger
            if cell == CellType.SNAKE or cell == CellType.RED_APPLE:
                return 0

            # If we see a Green Apple -> return 1
            if cell == CellType.GREEN_APPLE:
                return 1

            # Continue searching
            distance += 1

    def get_state(self) -> QStateType:
        head_x, head_y = self.env.snake_head

        danger_up = self.__is_danger(head_x - 1, head_y)
        danger_down = self.__is_danger(head_x + 1, head_y)
        danger_left = self.__is_danger(head_x, head_y - 1)
        danger_right = self.__is_danger(head_x, head_y + 1)

        apple_up = self.__get_green_apple_distance(-1, 0)
        apple_down = self.__get_green_apple_distance(1, 0)
        apple_left = self.__get_green_apple_distance(0, -1)
        apple_right = self.__get_green_apple_distance(0, 1)

        return (
            danger_up, danger_right, danger_down, danger_left,
            apple_up, apple_right, apple_down, apple_left,
        )
