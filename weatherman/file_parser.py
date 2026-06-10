from pathlib import Path
from weatherman.calculator import calculate
from weatherman.models import WeatherReading
from typing import Optional, List
from calendar import month_abbr


def parse_weather_line(line: str) -> Optional[WeatherReading]:
    """
    Parse a single weather data line and return a WeatherReading object.
    
    Args:
        line: A CSV line from weather file
        
    Returns:
        WeatherReading object or None if parsing fails
    """
    parts = line.strip().split(',')
    reading = None

    if len(parts) >= 10:
        # Parse date (format: YYYY-M-D)
        date_str = parts[0]
        date_parts = date_str.split('-')
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])

        # Parse temperatures and humidity
        max_temp = int(parts[1]) if parts[1] else None
        mean_temp = int(parts[2]) if parts[2] else None
        min_temp = int(parts[3]) if parts[3] else None
        max_humidity = int(parts[7]) if parts[7] else None
        mean_humidity = int(parts[8]) if parts[8] else None
        min_humidity = int(parts[9]) if parts[9] else None

        reading = WeatherReading(
            date=date_str,
            day=day,
            month=month,
            year=year,
            max_temp=max_temp,
            mean_temp=mean_temp,
            min_temp=min_temp,
            max_humidity=max_humidity,
            mean_humidity=mean_humidity,
            min_humidity=min_humidity
        )

    return reading


def _parse_year_month(year_month: str) -> tuple[str, Optional[int]]:
    parsed_year = year_month
    parsed_month = None

    if '/' in year_month:
        parts = year_month.split('/')
        try:
            parsed_year = str(int(parts[0]))
            parsed_month = int(parts[1])
        except ValueError:
            parsed_year = parts[0]

    return parsed_year, parsed_month


def _matches_year_month(file_name: str, target_year: str, target_month: Optional[int]) -> bool:
    matches = False

    if target_year in file_name:
        if target_month:
            abbr = month_abbr[target_month]
            matches = bool(abbr and abbr in file_name)
        else:
            matches = True

    return matches


def _read_weather_file(file_path: Path) -> list[WeatherReading]:
    readings: list[WeatherReading] = []

    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_handle.readline()

        for line in file_handle:
            reading = parse_weather_line(line)
            if reading:
                readings.append(reading)

    return readings


def _collect_readings(directory_path: Path, year_month: str) -> list[WeatherReading]:
    readings: list[WeatherReading] = []
    target_year, target_month = _parse_year_month(year_month)

    for file_path in directory_path.iterdir():
        if _matches_year_month(file_path.name, target_year, target_month):
            readings.extend(_read_weather_file(file_path))

    return readings


def parse(directory_path: str, argument_types: List[str], 
          year_months: List[str]) -> None:
    """
    Parse weather files and generate reports based on arguments.
    
    Args:
        directory_path: Path to weather files directory
        argument_types: List of report type flags (-e, -a, -c)
        year_months: List of year/month values corresponding to each flag
    """
    base_path = Path(directory_path)
    reports_count = min(len(argument_types), len(year_months))

    for index in range(reports_count):
        file_readings = _collect_readings(base_path, year_months[index])
        if file_readings:
            calculate(file_readings, argument_types[index], year_months[index])




