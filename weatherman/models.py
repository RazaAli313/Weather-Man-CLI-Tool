from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WeatherReading:
    """Data structure for holding each weather reading."""
    date: str
    day: int
    month: int
    year: int
    max_temp: Optional[int]
    mean_temp: Optional[int]
    min_temp: Optional[int]
    max_humidity: Optional[int]
    mean_humidity: Optional[int]
    min_humidity: Optional[int]


@dataclass
class YearlyReport:
    """Data structure for yearly calculation results."""
    highest_temp: int
    highest_temp_day: str
    lowest_temp: int
    lowest_temp_day: str
    max_humidity: int
    max_humidity_day: str


@dataclass
class MonthlyReport:
    """Data structure for monthly calculation results."""
    avg_highest_temp: float
    avg_lowest_temp: float
    avg_mean_humidity: float
    daily_readings: list = field(default_factory=list)


@dataclass
class LoaderClass:
    """Data structure for loader configuration."""
    directory_path: str
    arguments_types: list[str]
    timelines: list[str]
    