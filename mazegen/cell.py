from typing import Optional
NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000
ALL = NORTH | EAST | SOUTH | WEST


class Cell:
    """Represents a single cell in the maze grid."""
    def __init__(self, x: int, y: int):
        """
        Initializes cell coordinates, walls, and state.

        Args:
            x (int): The x-coordinate (column).
            y (int): The y-coordinate (row).
        """
        self.x = x
        self.y = y
        self.walls = ALL
        self.neb: list[Optional[Cell]] = [None, None, None, None]
        self.visited = False

    def count_neb(self) -> int:
        """
        Counts the number of valid (non-None) neighbors.

        Returns:
            int: The total number of valid neighbors (0-4).
        """
        count = 0
        for n in self.neb:
            if n:
                count += 1
            else:
                continue
        return count

    def visited_neb(self) -> int:
        """
        Counts the number of visited neighbors.

        Returns:
            int: The total number of visited neighbors.
        """
        vist: int = 0
        for i in self.neb:
            if i and i.visited:
                vist += 1
            else:
                continue
        return vist
