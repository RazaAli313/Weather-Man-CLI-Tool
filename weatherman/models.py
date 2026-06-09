from dataclasses import dataclass


#Three whitelines after imports skipped to fulfill PEP 8 standard
@dataclass
class LoaderClass:
    directory_path:str
    arguments_types:list[str]
    timelines:list[str]
    