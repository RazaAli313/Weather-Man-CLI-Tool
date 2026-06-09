from pathlib import Path
from .calculator import calculate



def parse(directory_path:str,argument_types:[str],timelines:[str])->None:
    directory_path=Path(directory_path)
    for timeline in timelines:
        print(timeline)
        for file in directory_path.iterdir():
          if timeline in file.name:
            calculate(file)



