from enum import Enum


class Color(Enum):
    # ANSI color codes
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"