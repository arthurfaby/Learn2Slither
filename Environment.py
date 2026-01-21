import pygame
from pygame import Surface
import config
from enums.CellType import CellType
import random

from enums.EnvironmentEvent import EnvironmentEvent
from enums.SnakeDirection import SnakeDirection
from utils.check_cell_in_board import check_cell_in_board


class Environment:
    screen: Surface
    board: list[list[CellType]]
    snake_direction: tuple[int, int]
    snake_head: tuple[int, int]
    snake_body: list[tuple[int, int]]
    direction_has_been_used: bool
    duration: int

    def __init__(self, screen: Surface):
        self.screen = screen
        self.board = [[CellType.EMPTY for _ in range(config.BOARD_SIZE)] for _ in range(config.BOARD_SIZE)]
        self.snake_direction = (1, 0)
        self.snake_head = (0, 0)
        self.snake_body = []
        self.direction_has_been_used = True
        self.duration = 0
        self.__create_snake()
        for _ in range(config.DEFAULT_GREEN_APPLES):
            self.__add_green_apple()
        for _ in range(config.DEFAULT_RED_APPLES):
            self.__add_red_apple()

    def update(self, action: SnakeDirection | None = None) -> EnvironmentEvent:
        if action is not None:
            self.__update_direction_from_action(action)
        self.duration += 1
        self.direction_has_been_used = True

        # Compute new head position
        new_head_x = self.snake_head[0] + self.snake_direction[0]
        new_head_y = self.snake_head[1] + self.snake_direction[1]

        # Check for collisions
        if not check_cell_in_board(new_head_x, new_head_y) or self.board[new_head_x][new_head_y] == CellType.SNAKE:
            return EnvironmentEvent.DIED

        if self.board[new_head_x][new_head_y] == CellType.GREEN_APPLE:
            self.__increase_snake_length()
            self.__add_green_apple()
            event = EnvironmentEvent.EATEN_GREEN_APPLE

        elif self.board[new_head_x][new_head_y] == CellType.RED_APPLE:
            self.__decrease_snake_length()
            self.__add_red_apple()
            if len(self.snake_body) == 0: return EnvironmentEvent.DIED
            event = EnvironmentEvent.EATEN_RED_APPLE
        else:
            event = EnvironmentEvent.NOTHING
        tail_x, tail_y = self.snake_body.pop(0)
        self.snake_body.append((new_head_x, new_head_y))
        self.board[new_head_x][new_head_y] = CellType.SNAKE
        self.snake_head = (new_head_x, new_head_y)
        self.board[tail_x][tail_y] = CellType.EMPTY

        return event

    def restart(self):
        self.__init__(self.screen)

    def draw(self):
        # Draw cells for snake game
        for x in range(config.BOARD_SIZE):
            for y in range(config.BOARD_SIZE):
                rect = (x * config.CELL_SIZE, y * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE)
                pygame.draw.rect(self.screen, self.board[y][x].get_color(), rect, int(config.CELL_SIZE))
                pygame.draw.rect(self.screen, config.CELL_BORDER_COLOR, rect, 1)

    def check_key_pressed(self, key_pressed: int):
        if not self.direction_has_been_used:
            return
        self.direction_has_been_used = False
        match key_pressed:
            case pygame.K_UP:
                if self.snake_direction != (1, 0):
                    self.snake_direction = (-1, 0)
            case pygame.K_DOWN:
                if self.snake_direction != (-1, 0):
                    self.snake_direction = (1, 0)
            case pygame.K_LEFT:
                if self.snake_direction != (0, 1):
                    self.snake_direction = (0, -1)
            case pygame.K_RIGHT:
                if self.snake_direction != (0, -1):
                    self.snake_direction = (0, 1)

    def __update_direction_from_action(self, action: SnakeDirection):
        if action == SnakeDirection.UP and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif action == SnakeDirection.DOWN and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)
        elif action == SnakeDirection.LEFT and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif action == SnakeDirection.RIGHT and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)

    def __increase_snake_length(self):
        tail_x, tail_y = self.snake_body[0]
        self.snake_body.insert(0, (tail_x, tail_y))

    def __decrease_snake_length(self):
        if len(self.snake_body) >= 1:
            tail_x, tail_y = self.snake_body.pop(0)
            self.board[tail_x][tail_y] = CellType.EMPTY

    def __get_random_empty_cell(self) -> tuple[int, int]:
        while True:
            x = random.randint(0, config.BOARD_SIZE - 1)
            y = random.randint(0, config.BOARD_SIZE - 1)
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
                if not check_cell_in_board(nx, ny) or not self.__is_cell_empty(nx, ny):
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
