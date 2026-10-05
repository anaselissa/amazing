
*This activity has been created as part of the 42 curriculum by aaleassa and okasawnh.*
# A-Maze-ing

## Overview

A-Maze-ing is a Python maze generator developed as part of the 42 curriculum.

The program reads maze settings from a configuration file, generates a maze according to the selected mode, displays it in the terminal, and writes the result to an output file using hexadecimal wall encoding.

The project supports two maze modes:

- `PERFECT=True`
  - Generates a perfect maze
  - Keeps the maze connected
  - Avoids loops
  - Provides a valid path between entry and exit

- `PERFECT=False`
  - Generates a more open, Pac-Man-like board
  - Includes loops and alternative routes
  - Reduces dead ends

The project also includes:

- Seed-based reproducible generation
- Shortest-path search
- Terminal visualization
- Show/hide path
- Multiple color themes
- Hexadecimal output
- A visible `42` pattern when the maze size allows it

## Team

### Anas Alissa — `aaleassa`

Main contributions:

- Configuration parsing and validation (`read_config.py`)
- Shortest-path search using BFS and path reconstruction
- Output integration, colors, themes, and terminal output refinement

### Omar Khasawneh — `okasawnh`

Main contributions:

- Maze generation logic (DFS-based generation and backtracking)
- Cell and grid handling
- Maze rendering in terminal, hexadecimal conversion, and direction conversion (`N`, `E`, `S`, `W`)

### Shared Work

- Final output design and integration between generation and solving
- Debugging coordinates, neighbors, and wall consistency
- Git collaboration and merging

## Maze Representation

Each cell stores four walls (North, East, South, West) using bit flags:

```text
North = 0001
East  = 0010
South = 0100
West  = 1000
```

- A wall bit set to `1` means the wall is closed.
- A wall bit set to `0` means the wall is open.

Examples:

- `0011` means North and East are closed.
- `1010` is `A` in hexadecimal.

Each cell is therefore stored as one hexadecimal digit.

## Algorithms

### Maze Generation

The maze is generated mainly using **Depth-First Search (DFS) with backtracking**.

1. Start from a cell and mark it as visited.
2. Choose an unvisited neighbor and open the wall between them.
3. Move to the neighbor and continue until blocked, then backtrack.

Additional adjustments are applied depending on `PERFECT=True` or `PERFECT=False`.

### Shortest Path

The shortest path is found using **Breadth-First Search (BFS)** since all moves have equal cost. The path is reconstructed and converted into directions (`N`, `E`, `S`, `W`).

## Configuration File

Example (`config.txt`):

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Supported Keys

| Key | Description |
| --- | --- |
| `WIDTH` | Number of columns |
| `HEIGHT` | Number of rows |
| `ENTRY` | Entry coordinates as `x,y` |
| `EXIT` | Exit coordinates as `x,y` |
| `OUTPUT_FILE` | Output file name |
| `PERFECT` | Maze mode |
| `SEED` | Optional seed |

Lines starting with `#` are treated as comments.

## Output Format

The output file contains:

1. The maze row by row in hexadecimal.
2. An empty line.
3. Entry coordinates.
4. Exit coordinates.
5. The shortest path using `N`, `E`, `S`, and `W`.

## Terminal Display & Interactive Options

The maze is displayed directly in the terminal using custom wall characters, entry markers (`▶`), exit markers (`■`), and the `42` pattern (`███`).

While the program is running, the user can:

1. Re-generate a new maze.
2. Show/Hide the path.
3. Change the maze theme/colors.
4. Quit.

## Project Structure

```text
.
├── a_maze_ing.py
├── cell.py
├── grid.py
├── read_config.py
├── colore_file.py
├── config.txt
├── Makefile
└── README.md
```

### File Roles

- `a_maze_ing.py` — main entry point and interactive CLI
- `cell.py` — cell representation and wall/neighbor tracking
- `grid.py` — grid logic, generation algorithms, solving, and terminal rendering
- `read_config.py` — configuration parsing and Pydantic validation
- `colore_file.py` — terminal colors and themes configuration

## Build and Run

### Requirements

- Python 3.10+
- pip
- Terminal with ANSI color support

### Commands

- **Install dependencies:** `make install`
- **Run program:** `make run`
- **Debug:** `make debug`
- **Lint:** `make lint` / `make lint-strict`
- **Clean:** `make clean`

## Reusability & Package Documentation

The maze-generation logic is structured as a reusable standalone module (`mazegen`) that can be imported and integrated into external Python applications.

### Usage Example

```python
from mazegen import generate_maze

config_dict = {
    "WIDTH": 20,
    "HEIGHT": 15,
    "ENTRY": (0, 0),
    "EXIT": (19, 14),
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": True,
    "SEED": 42
}

# Generate and solve the maze programmatically
obj_grid, grid, start_cell, exit_cell, ver_list, hor_list = generate_maze(config_dict)
```

## Project Planning & Management

- **Anticipated Planning & Evolution:** Tasks were initially divided between configuration parsing/solving (Anas) and maze generation algorithms/rendering (Omar). As development progressed, modules were systematically refactored and decoupled from CLI arguments into an independent Python package (`mazegen`).

- **What Worked Well:** Strict separation of CLI interface from core maze logic, utilizing bit flags for efficient wall representation, leveraging Pydantic for validation, and collaborative Git merging.

- **What Could Be Improved:** Fine-tuning non-perfect maze generation rules (`PERFECT=False`) to balance loop creation and dead-end elimination required multiple iterative adjustments.

## Tools Used

- Python
- VS Code
- Git
- GitHub
- Pydantic
- flake8
- mypy

## AI Usage

AI tools were used as support for clarifying subject requirements, discussing bitwise wall encoding, reviewing DFS/BFS concepts, and refining documentation. All suggestions were reviewed and adapted by the team.

## Resources

- Python documentation
- Graph traversal algorithms (DFS, BFS)
- Pydantic documentation
- flake8 documentation

## Authors

- **Anas Alissa** — `aaleassa`
- **Omar Khasawneh** — `okasawnh`