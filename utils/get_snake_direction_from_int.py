from enums.SnakeDirection import SnakeDirection


def get_snake_direction_from_int(direction_int: int) -> SnakeDirection:
    match direction_int:
        case 0:
            return SnakeDirection.UP
        case 1:
            return SnakeDirection.RIGHT
        case 2:
            return SnakeDirection.DOWN
        case 3:
            return SnakeDirection.LEFT
        case _:
            raise ValueError("Invalid direction integer")
