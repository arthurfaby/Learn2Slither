import config


class GameConfig:
    def __init__(
            self,
            save_path: str = None,
            load_path: str = None,
            dont_learn: bool = False,
            step_by_step: bool = False,
            visualize: bool = True,
            sessions_number: int = 0,
            fps: int = 60,
            snake_speed: int = 5,
            board_size: int = 10,
    ):
        self.save_path = save_path
        self.load_path = load_path
        self.dont_learn = dont_learn
        self.step_by_step = step_by_step
        self.visualize = visualize
        self.sessions_number = sessions_number
        self.fps = fps
        # If not visualizing, set snake speed to infinite (no delay)
        self.snake_speed = snake_speed if self.visualize else float('inf')
        self.board_size = board_size
        self.cell_size = config.WINDOW_HEIGHT / board_size
