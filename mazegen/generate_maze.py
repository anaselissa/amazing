from mazegen.grid import Grid
from mazegen.cell import Cell
from typing import Any

show_path: bool = True
choices: list[str] = ["1", "2", "3", "4"]


def generate_maze(config_inf: dict) -> tuple[Grid, list[list[Cell]], Any,
                                             Any, list[Cell], list[Cell]]:
    """
    Orchestrates grid creation, maze generation, logo placement, and solving.

    Args:
        config_inf (dict): A dictionary containing configuration parameters.

    Returns:
        tuple: A tuple containing the Grid object, the 2D grid list,
          start cell, exit cell, vertical path list, and horizontal path list.
    """
    obj_grid = Grid(
        int(config_inf["HEIGHT"]),
        int(config_inf["WIDTH"])
    )
    perf: bool = config_inf["PERFECT"]
    grid = obj_grid.create_maze()
    obj_grid.sseed(config_inf["SEED"])
    obj_grid.cell_nebs(grid)
    obj_grid.logo_42(grid)
    obj_grid.road_maker(grid[0][0])
    obj_grid.close_42(grid)
    x, y = config_inf["EXIT"]
    exit_cell = grid[y][x]
    x2, y2 = config_inf["ENTRY"]
    start_cell = grid[y2][x2]
    obj_grid.open_corner(grid)
    if not perf:
        obj_grid.open_more_walls(grid)
    ver_list, hor_list = obj_grid.direction_ver_hor(start_cell, exit_cell)
    if perf:
        obj_grid.close_walls_perfect(start_cell, exit_cell)

    obj_grid.maze_hexa(grid, (x2, y2), (x, y), config_inf["OUTPUT_FILE"])
    return obj_grid, grid, start_cell, exit_cell, ver_list, hor_list


def display_maze(obj_grid: Grid, grid: list[list[Cell]],
                 start_cell: Cell, exit_cell: Cell, ver_list: list[Cell],
                 hor_list: list[Cell], theme_number: int,
                 show_path: bool) -> None:
    """
    Triggers the terminal display function for the generated maze.

    Args:
        obj_grid (Grid): The Grid instance.
        grid (list[list[Cell]]): The maze grid.
        start_cell (Cell): The entry cell.
        exit_cell (Cell): The exit cell.
        ver_list (list[Cell]): Vertical path cells.
        hor_list (list[Cell]): Horizontal path cells.
        theme_number (int): Color theme index.
        show_path (bool): True to show the path, False to hide it.
    """
    obj_grid.print_grid_as_walls(grid, ver_list, hor_list, start_cell,
                                 exit_cell, theme_number, show_path)
