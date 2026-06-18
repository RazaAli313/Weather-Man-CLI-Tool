from enum import Enum


class Color(Enum):
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

YEAR_MONTH_PATTERN=r"^(?P<year>\d{4})(?:/(?P<month>\d{1,2}))?$"
YEAR_MONTH_DAY_PATTERN=r"^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$"
