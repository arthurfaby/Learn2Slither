import pygame
import config
from Agent import Agent
from Environment import Environment
from Interpreter import Interpreter
from enums.EnvironmentEvent import EnvironmentEvent

fps = 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
    pygame.display.set_caption(config.APP_NAME)
    clock = pygame.time.Clock()
    env = Environment(screen)
    interpreter = Interpreter(env)
    agent = Agent()
    agent.load_model()
    running = True
    last_move_time = 0
    generation = 1
    current_state = interpreter.get_state()
    max_length = 0
    max_duration = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                env.check_key_pressed(event.key)

        screen.fill(config.BACKGROUND_COLOR)
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > config.MOVE_DELAY_MS:
            action = agent.get_action(current_state, is_training=False)
            environment_event = env.update(action)
            next_state = interpreter.get_state()
            reward = interpreter.get_reward(environment_event)
            agent.learn(current_state, action, reward, next_state)
            current_state = next_state
            if environment_event == EnvironmentEvent.DIED:
                if len(env.snake_body) > max_length:
                    max_length = len(env.snake_body)
                if env.duration > max_duration:
                    max_duration = env.duration
                print(f"Generation {generation:4d} ended. Length was {len(env.snake_body):3d}. Max length so far: {max_length:3d}. Max duration : {max_duration:4d}.  Epsilon: {agent.epsilon:.4f}\r", end="")
                generation += 1
                agent.update_epsilon()
                env.restart()
                current_state = interpreter.get_state()
            last_move_time = current_time
        if fps > 0:
            env.draw()
            pygame.display.flip()
            clock.tick(fps)
    # agent.save_model()


if __name__ == '__main__':
    main()