# Puzzle Visualizer

A visualization tool for studying and analyzing different types of permutation puzzles. This project provides interactive visualizations for several classic permutation puzzle types:

- LRX - A puzzle involving swapping of 2 adjacent elements
- Top Spin - A circular permutation puzzle with a special "spin" operation
- Hungarian Ring - A mechanical puzzle with rotating elements in a ring formation

## Features

- Interactive visualization of puzzle states
- Step-by-step movement tracking
- Smooth animations for all operations
- Visual representation of permutation operations
- Interactive buttons for puzzle manipulation

## Installation

1. Ensure you have Python 3.11+ installed
2. Clone this repository:

```bash
git clone https://github.com/T0chka/PuzzleVisualizer.git
cd PuzzleVisualizer
```

3. Install dependencies:

```bash
poetry install --no-root
```

## Usage

The project provides two main visualization modes:
1. Static Schematic View:

```bash
python static/task_schematic.py
```

2. Interactive Animation View:
This launches an interactive window where you can:
- Perform LRX swaps with animation
- Execute TopSpin segment flips
- Rotate Hungarian Ring elements

```bash
python interactive/task_animation.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.