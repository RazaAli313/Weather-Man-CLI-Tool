import re
import calendar
from weatherman.models import Date
from weatherman.constants import Regex


def format_date_to_month_day(date_str: str, regex_pattern: Regex) -> Date:
    date = Date()
    pattern = regex_pattern.value if hasattr(regex_pattern, 'value') else regex_pattern
    date_match = re.match(pattern, date_str)
    if date_match:
        if 'year' in date_match.groupdict() and date_match.group('year'):
            date.year = date_match.group('year')
        month = date_match.groupdict().get('month')
        if month:
            month_index = int(month)
            date.month = calendar.month_abbr[month_index]
        if 'day' in date_match.groupdict() and date_match.group('day'):
            date.day = int(date_match.group('day'))
    return date
    