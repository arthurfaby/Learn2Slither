# Learn2Slither

## Setup

Tested with Python 3.10.12 and Python 3.12.13. Other Python versions have not been tested.

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Commands

```bash
# Run with default settings
python3 Learn2Slither.py

# Train without visualization and save the model
python3 Learn2Slither.py --visual off --sessions 10000 --save models/my_model.pkl

# Load a model for evaluation
python3 Learn2Slither.py --load models/my_model.pkl --dont-learn

# Play manually with the arrow keys
python3 Learn2Slither.py --manual

# Run step by step
python3 Learn2Slither.py --step-by-step

# Show all options
python3 Learn2Slither.py --help
```

## Options

| Option | Description | Default |
| --- | --- | --- |
| `-h`, `--help` | Show help and exit. | |
| `-s`, `--save PATH` | Save the model when the run ends. | |
| `-l`, `--load PATH` | Load an existing model. | |
| `-dl`, `--dont-learn` | Disable learning. | Off |
| `-sbs`, `--step-by-step` | Advance one step at a time. | Off |
| `-v`, `--visual on\|off` | Enable or disable visualization. | `on` |
| `-n`, `--sessions N` | Number of sessions (positive integer). | `100` |
| `-ss`, `--snake-speed N` | Speed in cells per second, from 0 to 1000; 0 pauses movement. | `50` |
| `-bs`, `--board-size N` | Square board size, from 5 to 50. | `10` |
| `-m`, `--manual` | Control the snake with the arrow keys. | Off |

`--step-by-step` requires `--visual on`. `--save` cannot be combined with `--dont-learn`.

## Keyboard controls

| Key | Action |
| --- | --- |
| Arrow keys | Move the snake in manual mode. |
| Up / Down | Increase / decrease speed in AI mode. |
| `S` | Toggle step-by-step mode. |
| Space | Advance one step in step-by-step mode. |
| `L` | Toggle learning. |
| Escape | Quit. |
