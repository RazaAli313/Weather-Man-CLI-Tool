from weatherman.models import LoaderClass
from weatherman.file_parser import parse
from typing import List


def load_directory(directory_path: str, arguments_types: List[str],
                   year_months: List[str]) -> None:
    
    request = LoaderClass(directory_path, arguments_types, year_months)
    parse(request.directory_path, request.arguments_types, request.year_months)


        