import argparse
import os


def existing_file(path: str) -> str:
    """Helper function used to validate the file_input argument."""
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist")
    return path

def positive_int(value: str) -> int:
    """Helper function to ensure a positive integer is provided."""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(f"Invalid positive int value: '{value}'")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid int value: '{value}'")

def argparse_init():
    parser = argparse.ArgumentParser(
        description='Run the Learn2Slither application.',
        usage="python3 Learn2Slither.py [options]"
    )
    parser.add_argument('-s', '--save', type=str, help='Path to the model file to save.')
    parser.add_argument('-l', '--load', type=existing_file, help='Path to the model file to load.')
    parser.add_argument('-dl', '--dont-learn', action="store_true", help='Disable learning.')
    parser.add_argument('-sbs', '--step-by-step', action="store_true", help='Does the simulation runs step by step.')
    parser.add_argument('-v', '--visual', choices=['on', 'off'], default='on', help='Enable/disabled visualization.')
    parser.add_argument('-n', '--sessions', type=positive_int, help='Number of sessions to run.')
    parser.add_argument('-f', '--fps', type=positive_int, default=60, help='Frames per second for visualization (default: 60).')
    parser.add_argument('-ss', '--snake-speed', type=int, default=50, help='Snake speed in cells per second (default: 50).')
    parser.add_argument('-bs', '--board-size', type=positive_int, default=10, help='Size of the game board (default: 10).')
    return parser
