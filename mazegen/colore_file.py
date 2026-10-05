RESET = "\033[0m"

WALL_COLORS = [
    "\033[97m",  # Theme 0 - Classic: white
    "\033[90m",  # Theme 1 - Graphite: gray
    "\033[34m",  # Theme 2 - Ocean: blue
    "\033[32m",  # Theme 3 - Forest: green
]

PATH_COLORS = [
    "\033[96m",  # bright cyan
    "\033[93m",  # bright yellow
    "\033[93m",  # bright yellow
    "\033[96m",  # bright cyan
]

ENTRY_COLORS = [
    "\033[95m",  # bright magenta
    "\033[92m",  # bright green
    "\033[95m",  # bright magenta
    "\033[93m",  # bright yellow
]

EXIT_COLORS = [
    "\033[91m",  # red
    "\033[95m",  # magenta
    "\033[96m",  # cyan
    "\033[93m",  # yellow
]
PATTERN_42_COLORS = [
    "\033[90m",  # gray
    "\033[97m",  # white
    "\033[97m",  # white
    "\033[97m",  # white
]

ret_dict: dict = {"RESET": RESET,
                  "WALL_COLORS": WALL_COLORS,
                  "PATH_COLORS": PATH_COLORS,
                  "ENTRY_COLORS": ENTRY_COLORS,
                  "EXIT_COLORS": EXIT_COLORS,
                  "PATTERN_42_COLORS": PATTERN_42_COLORS
                  }
