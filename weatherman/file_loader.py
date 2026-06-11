from weatherman.models import Loader
from weatherman.file_parser import parse
from typing import List


def load_directory(directory_path: str, arguments_types: List[str],
                   year_months: List[str]) -> None:
    
    request = Loader(directory_path, arguments_types, year_months)
    parse(request.directory_path, request.arguments_types, request.year_months)
