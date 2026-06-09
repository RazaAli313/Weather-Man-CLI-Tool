from weatherman.models import LoaderClass
from .parser import parse
from typing import List


#Three whitelines after imports skipped to fulfill PEP-8 standard
def load_directory(directory_path: str, arguments_types: List[str],
                   timelines: List[str]) -> None:
    """
    This is the Function to load the weatherfiles 
    directory in the memory.
    """
    request = LoaderClass(directory_path, arguments_types, timelines)
    parse(request.directory_path, request.arguments_types, request.timelines)


        