import config


def check_cell_in_board(x: int, y: int) -> bool:
    return 0 <= x < config.BOARD_SIZE and 0 <= y < config.BOARD_SIZE