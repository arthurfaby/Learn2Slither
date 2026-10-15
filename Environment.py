import pygame
from pygame import Surface
import config
from GameConfig import GameConfig
from custom_types import QStateType
from enums.CellType import CellType
import random

from enums.EnvironmentEvent import EnvironmentEvent
from enums.SnakeDirection import SnakeDirection
from utils.check_cell_in_board import check_cell_in_board


class Environment:
    game_config: GameConfig
    screen: Surface | None
    board: list[list[CellType]]
    snake_direction: tuple[int, int]
    snake_head: tuple[int, int]
    snake_body: list[tuple[int, int]]
    direction_has_been_used: bool
    duration: int
    steps_without_eating: int

    def __init__(self, screen: Surface | None, game_config: GameConfig):
        self.screen = screen
        self.game_config = game_config
        self.board = [
            [CellType.EMPTY for _ in range(self.game_config.board_size)] for _
            in range(self.game_config.board_size)]
        self.snake_direction = (1, 0)
        self.snake_head = (0, 0)
        self.snake_body = []
        self.direction_has_been_used = True
        self.duration = 0
        self.steps_without_eating = 0
        self.board_info_dict = {
            CellType.EMPTY: 'O',
            CellType.SNAKE: 'S',
            CellType.GREEN_APPLE: 'G',
            CellType.RED_APPLE: 'R'
        }
        self.__create_snake()
        for _ in range(config.DEFAULT_GREEN_APPLES):
            self.__add_green_apple()
        for _ in range(config.DEFAULT_RED_APPLES):
            self.__add_red_apple()

    def update(self, action: SnakeDirection | None = None) -> EnvironmentEvent:
        if action is not None:
            self.__update_direction_from_action(action)
        self.steps_without_eating += 1
        if self.steps_without_eating >= config.MAX_STARVATION_STEPS:
            return EnvironmentEvent.DIED

        self.duration += 1
        self.direction_has_been_used = True

        new_head_x = self.snake_head[0] + self.snake_direction[0]
        new_head_y = self.snake_head[1] + self.snake_direction[1]

        is_tail_cell = (new_head_x, new_head_y) == self.snake_body[0]
        if (not check_cell_in_board(
                self.game_config.board_size,
                new_head_x,
                new_head_y)
                or (self.board[new_head_x][new_head_y] == CellType.SNAKE
                    and not is_tail_cell)):
            return EnvironmentEvent.DIED

        if self.board[new_head_x][new_head_y] == CellType.GREEN_APPLE:
            self.steps_without_eating = 0
            event = EnvironmentEvent.EATEN_GREEN_APPLE

        elif self.board[new_head_x][new_head_y] == CellType.RED_APPLE:
            self.__decrease_snake_length()
            if len(self.snake_body) == 0:
                return EnvironmentEvent.DIED
            self.steps_without_eating = 0
            event = EnvironmentEvent.EATEN_RED_APPLE
        else:
            event = EnvironmentEvent.NOTHING

        if event != EnvironmentEvent.EATEN_GREEN_APPLE:
            tail_x, tail_y = self.snake_body.pop(0)
            self.board[tail_x][tail_y] = CellType.EMPTY

        self.snake_body.append((new_head_x, new_head_y))
        self.board[new_head_x][new_head_y] = CellType.SNAKE
        self.snake_head = (new_head_x, new_head_y)

        if event == EnvironmentEvent.EATEN_GREEN_APPLE:
            self.__add_green_apple()
        elif event == EnvironmentEvent.EATEN_RED_APPLE:
            self.__add_red_apple()

        return event

    def restart(self):
        self.__init__(self.screen, self.game_config)

    def draw(self):
        if not self.game_config.visualize:
            return
        # Draw cells for snake game
        for x in range(self.game_config.board_size):
            for y in range(self.game_config.board_size):
                rect = (x * self.game_config.cell_size,
                        y * self.game_config.cell_size,
                        self.game_config.cell_size, self.game_config.cell_size)
                pygame.draw.rect(self.screen, self.board[y][x].get_color(),
                                 rect, int(self.game_config.cell_size))
                if self.snake_head[0] == y and self.snake_head[1] == x:
                    pygame.draw.rect(self.screen, config.SNAKE_HEAD_COLOR,
                                     rect,
                                     int(self.game_config.cell_size))
                pygame.draw.rect(self.screen, config.CELL_BORDER_COLOR, rect,
                                 1)

    def __update_direction_from_action(self, action: SnakeDirection):
        direction_map = {
            SnakeDirection.UP: (-1, 0),
            SnakeDirection.DOWN: (1, 0),
            SnakeDirection.LEFT: (0, -1),
            SnakeDirection.RIGHT: (0, 1),
        }
        new_dir = direction_map[action]
        opposite = (-self.snake_direction[0], -self.snake_direction[1])
        if new_dir != opposite:
            self.snake_direction = new_dir

    def __decrease_snake_length(self):
        if len(self.snake_body) >= 1:
            tail_x, tail_y = self.snake_body.pop(0)
            self.board[tail_x][tail_y] = CellType.EMPTY

    def __get_random_empty_cell(self) -> tuple[int, int]:
        while True:
            x = random.randint(0, self.game_config.board_size - 1)
            y = random.randint(0, self.game_config.board_size - 1)
            if self.board[x][y] == CellType.EMPTY:
                return x, y

    def __is_cell_empty(self, x: int, y: int) -> bool:
        return self.board[x][y] == CellType.EMPTY

    def __create_snake(self):
        x, y = self.__get_random_empty_cell()
        # Randomly shuffle directions to try
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        random.shuffle(directions)
        # Try to place the snake in one of the directions
        for dx, dy in directions:
            can_place = True
            for i in range(config.SNAKE_INITIAL_LENGTH):
                nx, ny = x + i * dx, y + i * dy
                # Check if the cell is within bounds and empty
                if not check_cell_in_board(self.game_config.board_size, nx,
                                           ny) or not self.__is_cell_empty(nx,
                                                                           ny):
                    can_place = False
                    break
            if can_place:
                # Place the snake
                self.snake_direction = (dx, dy)
                for i in range(config.SNAKE_INITIAL_LENGTH):
                    nx, ny = x + i * dx, y + i * dy
                    self.snake_body.append((nx, ny))
                    self.snake_head = (nx, ny)
                    self.board[nx][ny] = CellType.SNAKE
                return

    def __add_green_apple(self):
        x, y = self.__get_random_empty_cell()
        self.board[x][y] = CellType.GREEN_APPLE

    def __add_red_apple(self):
        x, y = self.__get_random_empty_cell()
        self.board[x][y] = CellType.RED_APPLE

    def print_snake_info(self, session_recap: str,
                         action: SnakeDirection | None,
                         state: QStateType, reward: int):

        info = ""

        head_x, head_y = self.snake_head
        vhead_x, vhead_y = head_x + 1, head_y + 1

        board_size = self.game_config.board_size
        board_size_with_walls = board_size + 2
        for x in range(board_size_with_walls):
            for y in range(board_size_with_walls):
                if x == vhead_x or y == vhead_y:
                    if (x == 0 or y == 0 or x == board_size_with_walls - 1 or
                            y == board_size_with_walls - 1):
                        info += 'W'
                    elif x == vhead_x and y == vhead_y:
                        info += 'H'
                    else:
                        info += self.board_info_dict[self.board[x - 1][y - 1]]
                else:
                    info += ' '

            info += '\n'
        action_name = action.name if action is not None else "---"
        info += (f"{state} -> "
                 f"Choosed {action_name:<10} (Reward: {reward}){'':<10}\n")
        info += session_recap + '\n'
        print(info, end='')
        total_lines = self.game_config.board_size + 4
        print(f"\033[{total_lines}F", end='')
