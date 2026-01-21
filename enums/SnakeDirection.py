from enum import Enum


class SnakeDirection(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_value(self) -> int:
        return self.value