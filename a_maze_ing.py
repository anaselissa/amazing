"""
Main Entry Point for the A-Maze-ing generator.

Provides an interactive CLI to read configuration, generate mazes,
and display them with togglable paths and color themes.
"""

import sys
import read_config
from mazegen.generate_maze import generate_maze, display_maze

show_path: bool = True
choices: list[str] = ["1", "2", "3", "4"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        exit()

    config_dict = read_config.ret_check(sys.argv[1])

    theme_number: int = 0
    try:
        (obj_grid, grid, start_cell, exit_cell,
         ver_list, hor_list) = generate_maze(config_dict)
    except KeyError:
        print("ERROR: ENTRY or EXIT overlaps with 42 logo")
        exit()
    display_maze(obj_grid, grid, start_cell, exit_cell,
                 ver_list, hor_list, theme_number, show_path)
    try:
        while True:
            choice = input(
                "1. Re-generate a new maze and display it.\n"
                "2. Show/Hide path from the entry to exit.\n"
                "3. Change maze theme.\n"
                "4. Quit\n"
                "Choice? (1-4): "
            )
            if choice not in choices:
                print("Please enter a number between 1 and 4.")
                continue
            if choice == "1":
                try:
                    (obj_grid, grid, start_cell, exit_cell,
                     ver_list, hor_list) = generate_maze(config_dict)
                except KeyError:
                    print("ERROR: ENTRY or EXIT in 42 logooo")
                    exit()
            elif choice == "2":
                show_path = not show_path
            elif choice == "3":
                theme_number += 1
                if theme_number > 3:
                    theme_number = 0
            elif choice == "4":
                print("end <3")
                break
            display_maze(obj_grid, grid, start_cell,
                         exit_cell, ver_list, hor_list,
                         theme_number, show_path)
    except KeyboardInterrupt:
        print("\nend <3")
        exit()
    except EOFError:
        print("\nend <3")
        exit()
