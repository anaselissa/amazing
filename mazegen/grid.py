from mazegen.cell import Cell
import random
from collections import deque
from mazegen.colore_file import ret_dict as colores


NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000
ALL = NORTH | EAST | SOUTH | WEST
RESET = colores["RESET"]
WALL_COLORS = colores["WALL_COLORS"]
ENTRY_COLORS = colores["ENTRY_COLORS"]
EXIT_COLORS = colores["EXIT_COLORS"]
PATH_COLORS = colores["PATH_COLORS"]
PATTERN_42_COLORS = colores["PATTERN_42_COLORS"]
visited_lst: list[Cell] = []
path_choices: list[str] = ["N", "E", "S", "W"]
path_str: list[str] = []


class Grid:
    """
    Manages the maze grid structure, generation algorithms,
    and visualization..
    """
    def __init__(self, Hight: int, Width: int):
        """
        Initializes the grid dimensions and path lists.

        Args:
            Hight (int): Total number of rows.
            Width (int): Total number of columns.
        """
        self.Hight = Hight
        self.Width = Width
        self.ver_list: list[Cell] = []
        self.hor_list: list[Cell] = []
        self.top_right: list[Cell] = []
        self.down_right: list[Cell] = []

    def sseed(self, seed: int) -> None:
        """
        Sets the random seed for reproducible maze generation.

        Args:
            seed (int): The seed value. Ignored if <= 0.
        """
        if seed <= 0:
            return
        else:
            random.seed(seed)

    def create_maze(self) -> list[list[Cell]]:
        """
        Creates a 2D grid filled with unvisited Cell objects.

        Returns:
            list[list[Cell]]: A 2D list representing the grid.
        """
        grid = []
        for i in range(self.Hight):
            row = []
            for j in range(self.Width):
                c = Cell(j, i)
                row.append(c)
            grid.append(row)
        return grid

    def maze_hexa(self, grid: list[list[Cell]], entry: tuple,
                  exit: tuple, output_file: str) -> None:
        """
        Writes the maze, entry, exit, and path to a file in hexadecimal format.

        Args:
            grid (list[list[Cell]]): The generated maze grid.
            entry (tuple): Entry coordinates (x, y).
            exit (tuple): Exit coordinates (x, y).
            output_file (str): Destination file path.
        """
        hexa: list[str] = ["0", "1", "2", "3", "4", "5", "6",
                           "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        with open(output_file, "w") as file:
            for row in grid:
                for cell in row:
                    file.write(hexa[cell.walls])
                file.write("\n")
            file.write(f"\n{entry[0]}, {entry[1]}")
            file.write(f"\n{exit[0]}, {exit[1]}\n")
            for i in path_str:
                file.write(i)
            file.write("\n")

    def cell_nebs(self, grid: list[list[Cell]]) -> None:
        """
        Assigns the 4 cardinal neighbors(North, East, South, West)to
        each cell.

        Args:
            grid (list[list[Cell]]): The maze grid.
        """
        for row in grid:
            for i in row:
                if i.y > 0:
                    i.neb[0] = grid[i.y - 1][i.x]
                if i.x < len(grid[0]) - 1:
                    i.neb[1] = grid[i.y][i.x + 1]
                if i.y < len(grid) - 1:
                    i.neb[2] = grid[i.y + 1][i.x]
                if i.x > 0:
                    i.neb[3] = grid[i.y][i.x - 1]

    def logo_42(self, grid: list[list[Cell]]) -> list[Cell]:
        """
        Embeds a '42' pattern in the center of the grid if size permits.

        Args:
            grid (list[list[Cell]]): The maze grid.

        Returns:
            list[Cell]: A list of cells forming the '42' logo.
        """
        lst_42: list[Cell] = []
        if self.Hight < 9 or self.Width < 7:
            return lst_42
        med_height: int = int(self.Hight / 2)
        med_width: int = int(self.Width / 2)
        ls: list[tuple[int, int]] = [
                (med_height, med_width - 1),
                (med_height, med_width - 2),
                (med_height, med_width - 3),
                (med_height - 1, med_width - 3),
                (med_height - 2, med_width - 3),
                (med_height + 1, med_width - 1),
                (med_height + 2, med_width - 1),
                (med_height, med_width + 1),
                (med_height + 1, med_width + 1),
                (med_height + 2, med_width + 1),
                (med_height + 2, med_width + 2),
                (med_height + 2, med_width + 3),
                (med_height, med_width + 3),
                (med_height, med_width + 2),
                (med_height - 1, med_width + 3),
                (med_height - 2, med_width + 3),
                (med_height - 2, med_width + 2),
                (med_height - 2, med_width + 1)
                ]
        for row in grid:
            for cell in row:
                for y, x in ls:
                    if y == cell.y:
                        if x == cell.x:
                            lst_42.append(cell)
                            cell.visited = True
                            cell.y = -10
                            cell.x = -10
        return lst_42

    def print_grid_as_walls(self, grid: list[list[Cell]], ver_list: list[Cell],
                            hor_list: list[Cell], enter: Cell,
                            exit: Cell, colore_index: int,
                            show_path: bool) -> None:
        """
        Prints the maze to the terminal using ASCII characters and ANSI colors.

        Args:
            grid (list[list[Cell]]): The maze grid.
            ver_list (list[Cell]): Cells forming the vertical path.
            hor_list (list[Cell]): Cells forming the horizontal path.
            enter (Cell): Entry cell.
            exit (Cell): Exit cell.
            colore_index (int): Color theme index.
            show_path (bool): True to display the shortest path,
            False to hide it.
        """
        for row in grid:
            for cell in row:
                print("+", end="")
                if cell.walls & NORTH:
                    print(WALL_COLORS[colore_index] + "═══" + RESET, end="")
                else:
                    print("   ", end="")
            print("+")
            for cell in row:
                if cell.walls & WEST:
                    print(WALL_COLORS[colore_index] + "║" + RESET, end="")
                else:
                    print(" ", end="")
                if cell.x == -10 & cell.y == -10:
                    print(PATTERN_42_COLORS[colore_index] + "███" + RESET,
                          end="")
                elif cell.x == enter.x and cell.y == enter.y:
                    print(ENTRY_COLORS[colore_index] + "▶▶ " + RESET, end="")
                elif cell.x == exit.x and cell.y == exit.y:
                    print(EXIT_COLORS[colore_index] + " ■ " + RESET, end="")
                elif cell in ver_list and not show_path:
                    print(PATH_COLORS[colore_index] + " | ", end="")
                elif cell in hor_list and not show_path:
                    print(PATH_COLORS[colore_index] + " ─ " + RESET, end="")
                else:
                    print("   ", end="")
            if row[-1].walls & EAST:
                print(WALL_COLORS[colore_index] + "║" + RESET)
            else:
                print(" ")
        for cell in grid[-1]:
            print("+", end="")
            if cell.walls & SOUTH:
                print(WALL_COLORS[colore_index] + "═══" + RESET, end="")
            else:
                print("   ", end="")
        print("+")

    def open_walls(self, curr: Cell, ne_in: int) -> bool:
        """
        Opens the wall between the current cell and a specified neighbor.

        Args:
            curr (Cell): The current cell.
            ne_in (int): Index of the neighbor (0=N, 1=E, 2=S, 3=W).

        Returns:
            bool: True if wall was successfully opened, False otherwise.
        """
        neighbor = curr.neb[ne_in]
        if neighbor is None:
            return False
        if ne_in == 0:
            if neighbor.walls & SOUTH:
                neighbor.walls = neighbor.walls - SOUTH
            if curr.walls & NORTH:
                curr.walls = curr.walls - NORTH
            return True
        elif curr.neb[ne_in] and ne_in == 1:
            if neighbor.walls & WEST:
                neighbor.walls = neighbor.walls - WEST
            if curr.walls & EAST:
                curr.walls = curr.walls - EAST
            return True
        elif curr.neb[ne_in] and ne_in == 2:
            if neighbor.walls & NORTH:
                neighbor.walls = neighbor.walls - NORTH
            if curr.walls & SOUTH:
                curr.walls = curr.walls - SOUTH
            return True
        elif curr.neb[ne_in] and ne_in == 3:
            if neighbor.walls & EAST:
                neighbor.walls = neighbor.walls - EAST
            if curr.walls & WEST:
                curr.walls = curr.walls - WEST
            return True
        return False

    def close_walls(self, curr: Cell, ne_in: int) -> bool:
        """
        Closes the wall between the current cell and a specified neighbor.

        Args:
            curr (Cell): The current cell.
            ne_in (int): Index of the neighbor.

        Returns:
            bool: True if wall was successfully closed, False otherwise.
        """
        neighbor = curr.neb[ne_in]
        if neighbor is None:
            return False
        if ne_in == 0:
            if not neighbor.walls & SOUTH:
                neighbor.walls = neighbor.walls + SOUTH
            if not curr.walls & NORTH:
                curr.walls = curr.walls + NORTH
            return True
        elif curr.neb[ne_in] and ne_in == 1:
            if not neighbor.walls & WEST:
                neighbor.walls = neighbor.walls + WEST
            if not curr.walls & EAST:
                curr.walls = curr.walls + EAST
            return True
        elif curr.neb[ne_in] and ne_in == 2:
            if not neighbor.walls & NORTH:
                neighbor.walls = neighbor.walls + NORTH
            if not curr.walls & SOUTH:
                curr.walls = curr.walls + SOUTH
            return True
        elif curr.neb[ne_in] and ne_in == 3:
            if not neighbor.walls & EAST:
                neighbor.walls = neighbor.walls + EAST
            if not curr.walls & WEST:
                curr.walls = curr.walls + WEST
            return True
        return False

    def close_42(self, grid: list[list[Cell]]) -> None:
        """
        Closes all walls for the cells forming the '42' logo.

        Args:
            grid (list[list[Cell]]): The maze grid.
        """
        lst_42: list[Cell] = self.logo_42(grid)
        for row in grid:
            for cell in row:
                for cell in lst_42:
                    cell.walls = 15

    def open_corner(self, grid: list[list[Cell]]) -> None:
        """
        Ensures the four corners of the maze have open corridors.

        Args:
            grid (list[list[Cell]]): The maze grid.
        """
        corner: list[Cell] = [grid[0][0], grid[0][self.Width - 1],
                              grid[self.Hight - 1][0],
                              grid[self.Hight - 1][self.Width - 1]
                              ]
        self.open_walls(corner[0], 1)
        self.open_walls(corner[0], 2)
        self.open_walls(corner[1], 3)
        self.open_walls(corner[1], 2)
        self.open_walls(corner[2], 0)
        self.open_walls(corner[2], 1)
        self.open_walls(corner[3], 3)
        self.open_walls(corner[3], 1)

    def road_maker(self, curr: Cell) -> None:
        """
        Generates the maze paths using Depth-First Search (DFS) backtracking.

        Args:
            curr (Cell): The starting cell for generation.
        """
        visited_lst.clear()
        count = 0
        in_n: list[int] = []
        open: list[int] = []
        the_choice: list[int]
        while len(visited_lst) != 1 or count == 1:
            if not curr.visited:
                visited_lst.append(curr)
            curr.visited = True
            if any(curr.neb):
                if curr.visited_neb() != curr.count_neb():
                    if curr.count_neb() == 4:
                        open = [1]
                    elif curr.count_neb() == 3:
                        open = [1]
                    elif curr.count_neb() == 2:
                        open = [2]
                    num_of_open = random.choice(open)
                    for val_ind in range(4):
                        neighbor = curr.neb[val_ind]
                        if neighbor and not neighbor.visited:
                            in_n.append(curr.neb.index(curr.neb[val_ind]))
                            # if not (curr.walls & (the_choice * 2)):
                    if num_of_open <= len(in_n):
                        the_choice = random.sample(in_n, num_of_open)
                    else:
                        the_choice = random.sample(in_n, len(in_n))
                    for choi in the_choice:
                        self.open_walls(curr, choi)
                    in_n.clear()
                    next_cell = curr.neb[random.choice(the_choice)]
                    assert next_cell is not None
                    curr = next_cell
                    in_n.clear()

                elif curr.neb and curr.visited_neb() == curr.count_neb():
                    if len(visited_lst) > 1:
                        visited_lst.pop()
                        curr = visited_lst[-1]
            count += 1

    def bfs_search(self, start_cell: Cell, exit_point: Cell) -> list[Cell]:
        """
        Finds the shortest path from start to exit using Breadth-First Search.

        Args:
            start_cell (Cell): The entry cell.
            exit_point (Cell): The exit cell.

        Returns:
            list[Cell]: A list of cells representing the shortest path.
        """
        queue: deque[Cell] = deque()
        queue.append(start_cell)
        visited: set = {start_cell}
        parent: dict = {}
        walls = [NORTH, EAST, SOUTH, WEST]
        while queue:
            current = queue.popleft()
            if current == exit_point:
                break
            for index, neighbor in enumerate(current.neb):
                if (
                    neighbor
                    and neighbor not in visited
                    and not (current.walls & walls[index])
                ):
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        path: list[Cell] = []
        current = exit_point
        while current != start_cell:
            path.append(current)
            current = parent[current]
        path.append(start_cell)
        path.reverse()
        return path

    def direction_ver_hor(self, start_cell: Cell,
                          exit_cell: Cell) -> tuple[list[Cell],
                                                    list[Cell]]:
        """
        Splits the solved path into vertical and horizontal movement lists.

        Args:
            start_cell (Cell): The entry cell.
            exit_cell (Cell): The exit cell.

        Returns:
            tuple[list[Cell], list[Cell]]: Two lists containing vertical and
            horizontal path cells.
        """
        lst = self.bfs_search(start_cell, exit_cell)
        path_str.clear()
        count_1 = 1
        count_2 = 0
        while count_1 < len(lst):
            if lst[count_1].x - lst[count_1 - 1].x != 0:
                if lst[count_2].x - lst[count_2 + 1].x > 0:
                    path_str.append("W")
                elif lst[count_2].x - lst[count_2 + 1].x < 0:
                    path_str.append("E")
                self.hor_list.append(lst[count_1])
            elif lst[count_1].y - lst[count_1 - 1].y != 0:
                if lst[count_2].y - lst[count_2 + 1].y < 0:
                    path_str.append("S")
                elif lst[count_2].y - lst[count_2 + 1].y > 0:
                    path_str.append("N")
                self.ver_list.append(lst[count_1])
            count_1 += 1
            count_2 += 1
        return self.ver_list, self.hor_list

    def close_walls_perfect(self,  start_cell: Cell, exit_cell: Cell) -> None:
        """
        Adjusts walls to ensure a perfect maze (single path) between entry and
        exit.

        Args:
            start_cell (Cell): The entry cell.
            exit_cell (Cell): The exit cell.
        """
        lst = self.bfs_search(start_cell, exit_cell)
        count = 0
        for cell in lst:
            while count % 2 == 0:
                self.close_walls(cell, 0)
                self.close_walls(cell, 1)
                self.close_walls(cell, 2)
                self.close_walls(cell, 3)
                count += 1
        count = 0
        while count < len(lst) - 1:
            if lst[count].x - lst[count + 1].x != 0:
                if lst[count].x - lst[count + 1].x > 0:
                    self.open_walls(lst[count], 3)
                elif lst[count].x - lst[count + 1].x < 0:
                    self.open_walls(lst[count], 1)
            if lst[count].y - lst[count + 1].y != 0:
                if lst[count].y - lst[count + 1].y < 0:
                    self.open_walls(lst[count], 2)
                elif lst[count].y - lst[count + 1].y > 0:
                    self.open_walls(lst[count], 0)
            count += 1
        return

    def is_42(self, cell: Cell) -> bool:
        """
        Checks if a given cell is part of the '42' logo pattern.

        Args:
            cell (Cell): The cell to check.

        Returns:
            bool: True if the cell is part of the logo, False otherwise.
        """
        return cell.x == -10 and cell.y == -10

    def open_count(self, cell: Cell) -> int:
        """
        Counts the number of open doors (missing walls) in a cell.

        Args:
            cell (Cell): The cell to evaluate.

        Returns:
            int: The number of open doors.
        """
        count = 0
        for index, neighbor in enumerate(cell.neb):
            if neighbor is None or self.is_42(neighbor):
                continue
            elif index == 0 and not (cell.walls & NORTH):
                count += 1
            elif index == 2 and not (cell.walls & SOUTH):
                count += 1
            elif index == 1 and not (cell.walls & EAST):
                count += 1
            elif index == 3 and not (cell.walls & WEST):
                count += 1
        return count

    def open_more_walls(self, grid: list[list[Cell]]) -> None:
        """
        Opens additional walls to create loops for non-perfect (Pac-Man) mazes.

        Args:
            grid (list[list[Cell]]): The maze grid.
        """
        for row in grid:
            for cell in row:
                if self.is_42(cell):
                    continue
                if self.open_count(cell) > 1:
                    continue
                if self.open_count(cell) == 1:
                    for index, neb in enumerate(cell.neb):
                        if not neb or self.is_42(neb):
                            continue
                        elif cell.walls & NORTH and index == 0:
                            self.open_walls(cell, 0)
                            break
                        elif cell.walls & SOUTH and index == 2:
                            self.open_walls(cell, 2)
                            break
                        elif cell.walls & EAST and index == 1:
                            self.open_walls(cell, 1)
                            break
                        elif cell.walls & WEST and index == 3:
                            self.open_walls(cell, 3)
                            break
        return
