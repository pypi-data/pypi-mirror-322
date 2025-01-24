# Stara C++

A C++ implementation of the A\* pathfinding algorithm with Python bindings using pybind11.

## Installation

```bash
pip install stara-cpp
```

## Requirements

- Python 3.12 or higher
- CMake 3.15 or higher
- C++17 compatible compiler
- Poetry (for Python dependency management)
- numpy

## Development

1. Clone the repository:

```bash
git clone https://github.com/valerius21/stara-cpp.git
cd stara-cpp
```

2. Create and activate a Poetry environment:

```bash
poetry install
poetry shell
```

3. Build and install the package:

```bash
pip install -e .
```

## Usage

### Python

```python
import numpy as np
from stara_cpp import load_maze, AStar

# Create a maze (0 = wall, ≥1 = passage)
maze = np.array([
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1],
], dtype=np.int32)

# Load maze and create pathfinder
maze_ptr = load_maze(maze)
pathfinder = AStar(maze_ptr)

# Find path from (0,0) to (4,4)
start = (0, 0)
goal = (4, 4)

try:
    path = pathfinder.find_path(start, goal)
    if path is not None:
        print("Path found:", path)
    else:
        print("No path found!")
except RuntimeError as e:
    print("Error:", str(e))
```

## API Reference

### Python API

#### `load_maze(array: np.ndarray) -> Maze`

Loads a numpy array into a C++ Maze object.

- `array`: 2D numpy array where 0 represents walls and ≥1 represents passages
- Returns: Maze object

#### `class AStar`

A\* pathfinding implementation.

##### Methods:

- `__init__(maze: Maze)`: Initialize with a maze
- `find_path(start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]`: Find path from start to goal
- `manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int`: Calculate Manhattan distance

### C++ API

#### `class Maze`

Represents the maze grid.

##### Methods:

- `isValid(int x, int y) -> bool`: Check if coordinates are within bounds
- `isWalkable(int x, int y) -> bool`: Check if position is walkable
- `getCellNeighbours(int x, int y) -> vector<tuple<int, int, int>>`: Get neighboring cells

#### `class AStar`

A\* pathfinding implementation.

##### Methods:

- `findPath(pair<int, int> start, pair<int, int> goal) -> optional<vector<pair<int, int>>>`: Find path
- `manhattanDistance(pair<int, int> pos1, pair<int, int> pos2) -> int`: Calculate heuristic

## Development

### Building from Source

1. Install development dependencies:

```bash
poetry install
```

2. Build in development mode:

```bash
poetry shell
pip install -e .
```

### Running Tests

Run the example script:

```bash
python example.py
```
