import pygame
import args_parsing
from Agent import Agent
from GameConfig import GameConfig
from Environment import Environment
from Interpreter import Interpreter
from config import PADDING, HALF_BUTTON_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, \
    GAME_WIDTH, BUTTON_HEIGHT, APP_NAME, \
    BACKGROUND_COLOR, LEN_HISTORY_SIZE
from enums.EnvironmentEvent import EnvironmentEvent
from ui.Button import Button


class Game:
    def __init__(self, game_config: GameConfig):
        self.config = game_config

        pygame.init()
        self.screen = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)) if self.config.visualize else None
        pygame.display.set_caption(APP_NAME)
        self.font = pygame.font.SysFont('Arial', 20)
        self.clock = pygame.time.Clock()

        self.env = Environment(self.screen, self.config)
        self.interpreter = Interpreter(self.env)
        self.agent = Agent(self.config)

        self.running = True
        self.run_step = not self.config.step_by_step
        self.current_state = self.interpreter.get_state()
        self.session = 1
        self.score_history = [0 for _ in range(LEN_HISTORY_SIZE)]
        self.max_length = 0
        self.max_duration = 0
        self.last_move_time = 0

        self.buttons = self._create_buttons()

        if self.config.load_path:
            self.agent.load_model(self.config.load_path)

    def _create_buttons(self) -> list[Button]:
        """Crée et configure les boutons de l'interface."""
        return [
            Button(
                x=GAME_WIDTH + PADDING,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Speed -",
                font=self.font,
                action=lambda: self.change_speed(-5),
                background_color=(100, 0, 0),
                hover_background_color=(200, 0, 0), border_color=(200, 0, 0)
            ),
            Button(
                x=GAME_WIDTH + 2 * PADDING + HALF_BUTTON_WIDTH,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Speed +",
                font=self.font,
                action=lambda: self.change_speed(5),
                background_color=(0, 100, 0),
                hover_background_color=(0, 200, 0), border_color=(0, 200, 0)
            ),
            Button(
                x=GAME_WIDTH + PADDING,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT * 2 - PADDING * 2,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Speed --",
                font=self.font,
                action=lambda: self.change_speed(-100),
                background_color=(100, 0, 0),
                hover_background_color=(200, 0, 0), border_color=(200, 0, 0)
            ),
            Button(
                x=GAME_WIDTH + 2 * PADDING + HALF_BUTTON_WIDTH,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT * 2 - PADDING * 2,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Speed ++",
                font=self.font,
                action=lambda: self.change_speed(100),
                background_color=(0, 100, 0),
                hover_background_color=(0, 200, 0), border_color=(0, 200, 0)
            ),
            Button(
                x=GAME_WIDTH + PADDING,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT * 3 - PADDING * 3,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Toggle Learning",
                font=self.font,
                action=self.toggle_learning,
                background_color=(0, 0, 100),
                hover_background_color=(0, 0, 200), border_color=(0, 0, 200)
            ),
            Button(
                x=GAME_WIDTH + 2 * PADDING + HALF_BUTTON_WIDTH,
                y=WINDOW_HEIGHT - BUTTON_HEIGHT * 3 - PADDING * 3,
                width=HALF_BUTTON_WIDTH,
                height=BUTTON_HEIGHT,
                text="Step-by-step",
                font=self.font,
                action=self.toggle_step_by_step,
                background_color=(0, 0, 100),
                hover_background_color=(0, 0, 200), border_color=(0, 0, 200)
            ),
        ]

    def toggle_step_by_step(self):
        self.config.step_by_step = not self.config.step_by_step
        self.run_step = not self.config.step_by_step

    def toggle_learning(self):
        self.config.dont_learn = not self.config.dont_learn

    def change_speed(self, delta: int):
        self.config.snake_speed = max(0, min(1000,
                                             self.config.snake_speed + delta))

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.check_click(mouse_pos)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_speed(5)
                if event.key == pygame.K_DOWN:
                    self.change_speed(-5)
                if event.key == pygame.K_s:
                    self.toggle_step_by_step()
                if event.key == pygame.K_l:
                    self.toggle_learning()
                if event.key == pygame.K_SPACE:
                    self.run_step = True
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        for button in self.buttons:
            button.check_hover(mouse_pos)

    def logic_step(self):
        action = self.agent.get_action(self.current_state, is_training=(
            not self.config.dont_learn))
        environment_event = self.env.update(action)
        next_state = self.interpreter.get_state()
        reward = self.interpreter.get_reward(environment_event)

        self.agent.learn(self.current_state, action, reward, next_state)

        self.current_state = next_state
        return environment_event

    def draw_dashed_line(self, start_pos, end_pos, color, width=1,
                         dash_length=10, gap_length=5):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance == 0:
            return

        direction = (dx / distance, dy / distance)
        current_dist = 0

        while current_dist < distance:
            start_point = (
                x1 + direction[0] * current_dist,
                y1 + direction[1] * current_dist
            )

            end_dist = min(current_dist + dash_length, distance)
            end_point = (
                x1 + direction[0] * end_dist,
                y1 + direction[1] * end_dist
            )

            pygame.draw.line(self.screen, color, start_point, end_point, width)
            current_dist += dash_length + gap_length

    def draw_chart(self):
        if len(self.score_history) < 2:
            return

        # Area zone
        area_x = GAME_WIDTH + PADDING
        area_y = 80
        area_w = WINDOW_WIDTH - GAME_WIDTH - (2 * PADDING)
        buttons_area_height = (BUTTON_HEIGHT * 3) + (PADDING * 4)
        area_h = WINDOW_HEIGHT - area_y - buttons_area_height

        pygame.draw.rect(self.screen, (30, 30, 30),
                         (area_x, area_y, area_w, area_h))
        pygame.draw.rect(self.screen, (100, 100, 100),
                         (area_x, area_y, area_w, area_h), 1)

        scale_max = max(self.max_length * 1.1, 1)
        num_points = len(self.score_history)

        ratio_max = self.max_length / scale_max
        y_max_line = area_y + area_h - (ratio_max * area_h)

        self.draw_dashed_line(
            start_pos=(area_x, y_max_line),
            end_pos=(area_x + area_w, y_max_line),
            color=(200, 50, 50),  # Rouge
            width=1,
            dash_length=8,
            gap_length=6
        )

        text_max_label = self.font.render(f"Max: {self.max_length}", True,
                                          (200, 50, 50))
        self.screen.blit(text_max_label, (area_x + 5, y_max_line - 20))

        points = []
        for i, score in enumerate(self.score_history):
            x = area_x + (i / (num_points - 1)) * area_w
            ratio = score / scale_max
            y = area_y + area_h - (ratio * area_h)

            points.append((x, y))

        if len(points) > 1:
            pygame.draw.lines(self.screen, (0, 255, 255), False, points, 2)

    def handle_session_end(self):
        current_len = len(self.env.snake_body)
        current_dur = self.env.duration

        self.max_length = max(current_len, self.max_length)
        self.max_duration = max(current_dur, self.max_duration)

        print(
            f"Session {self.session:4d} ended. Length: {current_len:3d}. "
            f"Max Len: {self.max_length:3d}. "
            f"Max Dur: {self.max_duration:4d}.\r",
            end=""
        )
        self.score_history.append(current_len)
        if len(self.score_history) > LEN_HISTORY_SIZE:
            self.score_history.pop(0)

        if not self.config.dont_learn:
            self.agent.update_epsilon()
        self.env.restart()
        self.current_state = self.interpreter.get_state()
        self.session += 1

    def __render_texts(self):
        session_speed_length_text = self.font.render(
            f"Session {self.session:5d} | "
            f"Speed: {self.config.snake_speed:4d} | "
            f"Length: {len(self.env.snake_body):3d}",
            True, (255, 255, 255)
        )
        self.screen.blit(session_speed_length_text,
                         (GAME_WIDTH + PADDING, PADDING))

        learning_text = self.font.render(
            "Learning",
            True,
            (0, 255, 0) if not self.config.dont_learn else (255, 0, 0)
        )
        self.screen.blit(learning_text,
                         (GAME_WIDTH + PADDING,
                          2 * PADDING
                          + session_speed_length_text.get_height()))

        step_by_step_text = self.font.render(
            "Step-by-step",
            True, (0, 255, 0) if self.config.step_by_step else (255, 0, 0)
        )
        self.screen.blit(step_by_step_text,
                         (GAME_WIDTH + 2 * PADDING + HALF_BUTTON_WIDTH,
                          2 * PADDING
                          + session_speed_length_text.get_height()))

    def render(self):
        if not self.config.visualize or self.screen is None:
            return

        self.screen.fill(BACKGROUND_COLOR)

        for button in self.buttons:
            button.draw(self.screen)

        self.__render_texts()
        self.draw_chart()
        self.env.draw()
        pygame.display.flip()
        self.clock.tick(self.config.fps)

    def run(self):
        while self.running:
            if self.config.sessions_number < self.session:
                print("\nMax sessions reached.")
                break

            self.handle_input()
            if not self.running:
                break

            current_time = pygame.time.get_ticks()
            time_delta = current_time - self.last_move_time
            should_move = time_delta > (
                    1000 / self.config.snake_speed) \
                if self.config.snake_speed > 0 else False
            should_move = True if self.config.step_by_step else should_move

            if should_move and self.run_step:
                self.run_step = not self.config.step_by_step

                event = self.logic_step()

                if event == EnvironmentEvent.DIED:
                    self.handle_session_end()

                self.last_move_time = current_time

            self.render()

        if self.config.save_path:
            self.agent.save_model(self.config.save_path)
        pygame.quit()


def get_game_config_from_args():
    parser = args_parsing.argparse_init()
    args = parser.parse_args()
    if args.visual == 'off' and args.step_by_step:
        parser.error(
            "Incompatible arguments: You cannot use "
            "--step-by-step when --visual is 'off'.")
    if args.dont_learn is True and args.save is not None:
        parser.error(
            "Incompatible arguments: You cannot use "
            "--save when --dont-learn is set.")
    if args.snake_speed > 1000 or args.snake_speed < 0:
        parser.error(
            "Invalid argument: --snake-speed must be between 0 and 1000.")
    if args.board_size < 5 or args.board_size > 50:
        parser.error(
            "Invalid argument: --board-size must be between 5 and 50.")
    return GameConfig(
        save_path=args.save,
        load_path=args.load,
        dont_learn=args.dont_learn,
        step_by_step=args.step_by_step,
        visualize=args.visual == 'on',
        sessions_number=args.sessions,
        fps=60,
        snake_speed=args.snake_speed,
        board_size=args.board_size,
    )


if __name__ == '__main__':
    config_obj = get_game_config_from_args()
    game = Game(config_obj)
    game.run()
