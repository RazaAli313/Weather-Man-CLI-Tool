from pathlib import Path


def calculate(file:Path)->int:
    with file.open('r',encoding="utf-8") as f:
        line=f.readline()
        while line:
             print(line)
             f.readline()
