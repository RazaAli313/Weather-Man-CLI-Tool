import re
from pathlib import Path
from calendar import month_abbr
from typing import List
from weatherman.constants import Regex
from weatherman.utils import format_date_to_month_day

class WeatherDirectoryLoader:
    def __init__(self, directory_path: str) -> None:
        self.base_path = Path(directory_path)

    def load_matching_files(self, argument: str) -> List[Path]:
        files_matched = [] 
        date=format_date_to_month_day(argument,Regex.YearMonth)
        if date.month:
            file_regex = re.compile(rf".*_{date.year}_{date.month}.*\.txt$", re.IGNORECASE)
        else:
            file_regex = re.compile(rf".*_{date.year}_.*\.txt$", re.IGNORECASE)
        files_matched = [file_path for file_path in self.base_path.iterdir() if file_path.is_file() and file_regex.match(file_path.name)]
        return files_matched
          