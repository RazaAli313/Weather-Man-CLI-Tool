from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WeatherReading:
    """Data structure for holding each weather reading."""
    date: str
    day: int
    month: int
    year: int
    maximum_temperature: Optional[int]
    mean_temperature: Optional[int]
    min_temperature: Optional[int]
    maximum_humidity: Optional[int]
    mean_humidity: Optional[int]
    min_humidity: Optional[int]


@dataclass
class YearlyReport:
    """Data structure for yearly calculation results."""
    highest_temperature: int
    highest_temperature_day: str
    lowest_temperature: int
    lowest_temperature_day: str
    maximum_humidity: int
    maximum_humidity_day: str


@dataclass
class MonthlyReport:
    """Data structure for monthly calculation results."""
    avg_highest_temperature: float
    avg_lowest_temperature: float
    avg_mean_humidity: float
    daily_readings: list = field(default_factory=list)


@dataclass
class Loader:

    directory_path: str
    arguments_types: list[str]
    year_months: list[str]
    