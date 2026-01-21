import os
import pickle
import random

import config
from enums.SnakeDirection import SnakeDirection
from custom_types.QStateType import QStateType
from custom_types.QValuesType import QValuesType
from utils.get_snake_direction_from_int import get_snake_direction_from_int


class Agent:
    q_table: dict[QStateType, QValuesType]
    learning_rate: float
    discount_factor: float
    epsilon: float
    epsilon_decay: float
    min_epsilon: float

    def __init__(self):
        self.q_table = {}
        self.learning_rate = config.LEARNING_RATE
        self.discount_factor = config.DISCOUNT_FACTOR
        self.epsilon = config.DEFAULT_EPSILON
        self.epsilon_decay = config.EPSILON_DECAY
        self.min_epsilon = config.MIN_EPSILON

    def get_q_values(self, state: QStateType) -> QValuesType:
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]
        return self.q_table[state]

    def get_action(self, state, is_training=False) -> SnakeDirection:
        if  is_training and random.random() < self.epsilon:
            return random.choice([SnakeDirection.UP, SnakeDirection.DOWN, SnakeDirection.LEFT, SnakeDirection.RIGHT])  # Exploration
        else:
            q_values = self.get_q_values(state)
            # Choose the action with the highest Q-value (with random tie-breaking)
            max_q = max(q_values)
            actions_with_max_q = [get_snake_direction_from_int(i) for i, val in enumerate(q_values) if val == max_q]
            return random.choice(actions_with_max_q)

    def learn(self, state: QStateType, action: SnakeDirection, reward: int, next_state: QStateType):
        if not (0 <= action.get_value() <= 3):
            raise ValueError("Action must be between 0 and 3")
        current_q = self.get_q_values(state)[action.get_value()]
        max_future_q = max(self.get_q_values(next_state))
        # Bellman equation
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)

        self.q_table[state][action.get_value()] = new_q

    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_model(self, filepath="models/brain.pkl"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"Model saved : {filepath}")

    def load_model(self, filepath="models/brain.pkl"):
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.q_table = pickle.load(f)
            print(f"Model upload ! Memory size : {len(self.q_table)} states.")
            self.epsilon = self.min_epsilon
        else:
            print("Model not found.")