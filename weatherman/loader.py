import re
from pathlib import Path
from calendar import month_abbr
from typing import List

class WeatherDirectoryLoader:
    def __init__(self, directory_path: str) -> None:
        self.base_path = Path(directory_path)

    def load_matching_files(self, argument: str) -> List[Path]:
        files_matched = []
        match = re.match(r"^(?P<year>\d{4})(?:/(?P<month>\d{1,2}))?$", argument)
        if match:
            year_val = match.group('year')
            month_val = match.group('month')
            if month_val:
                month_idx = int(month_val)
                if 1 <= month_idx <= 12:
                    month_name = month_abbr[month_idx]
                    file_regex = re.compile(rf".*_{year_val}_{month_name}.*\.txt$", re.IGNORECASE)
                    files_matched = [file_path for file_path in self.base_path.iterdir() if file_path.is_file() and file_regex.match(file_path.name)]
            else:
                file_regex = re.compile(rf".*_{year_val}_.*\.txt$", re.IGNORECASE)
                files_matched = [file_path for file_path in self.base_path.iterdir() if file_path.is_file() and file_regex.match(file_path.name)]
        return files_matched
