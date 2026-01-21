from enum import Enum

import config


class CellType(Enum):
    EMPTY = 0
    SNAKE = 1
    GREEN_APPLE = 2
    RED_APPLE = 3

    def get_color(self):
        match self:
            case CellType.EMPTY:
                return config.CELL_BACKGROUND_COLOR
            case CellType.SNAKE:
                return config.SNAKE_COLOR
            case CellType.GREEN_APPLE:
                return config.GREEN_APPLE_COLOR
            case CellType.RED_APPLE:
                return config.RED_APPLE_COLOR
