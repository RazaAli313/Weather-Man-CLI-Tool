from pathlib import Path
from weatherman.weather_statistics_calculator import calculate
from weatherman.constants import (
    DATE_INDEX,
    MAX_TEMP_INDEX,
    MEAN_TEMP_INDEX,
    MIN_TEMP_INDEX,
    MAX_HUMIDITY_INDEX,
    MEAN_HUMIDITY_INDEX,
    MIN_HUMIDITY_INDEX,
    MIN_FIELD_COUNT,
)
from weatherman.models import WeatherReading
from typing import Optional, List
from calendar import month_abbr

_MONTH_NAME_TO_NUMBER = {
    name.lower(): index for index, name in enumerate(month_abbr) if name
}


def _parse_optional_int(value: str) -> Optional[int]:
    parsed_value = None

    if value:
        parsed_value = int(value)

    return parsed_value


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

    if len(parts) >= MIN_FIELD_COUNT:
        # Parse date (format: YYYY-M-D)
        date_str = parts[DATE_INDEX]
        date_parts = date_str.split('-')
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])

        # Parse temperatures and humidity
        max_temp = _parse_optional_int(parts[MAX_TEMP_INDEX])
        mean_temp = _parse_optional_int(parts[MEAN_TEMP_INDEX])
        min_temp = _parse_optional_int(parts[MIN_TEMP_INDEX])
        max_humidity = _parse_optional_int(parts[MAX_HUMIDITY_INDEX])
        mean_humidity = _parse_optional_int(parts[MEAN_HUMIDITY_INDEX])
        min_humidity = _parse_optional_int(parts[MIN_HUMIDITY_INDEX])

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
        year_part, month_part = year_month.split('/', 1)
        try:
            parsed_year = str(int(year_part))
            parsed_month = int(month_part)
        except ValueError:
            parsed_year = year_part

    return parsed_year, parsed_month


def _extract_year_month_from_file_name(file_name: str) -> tuple[Optional[str], Optional[int]]:
    file_year = None
    file_month = None

    stem_parts = Path(file_name).stem.split('_')
    if len(stem_parts) >= 3:
        year_candidate = stem_parts[-2]
        month_candidate = stem_parts[-1].lower()
        if year_candidate.isdigit() and month_candidate in _MONTH_NAME_TO_NUMBER:
            file_year = year_candidate
            file_month = _MONTH_NAME_TO_NUMBER[month_candidate]

    return file_year, file_month


def _build_file_index(directory_path: Path) -> tuple[dict[str, list[Path]], dict[tuple[str, int], list[Path]]]:
    files_by_year: dict[str, list[Path]] = {}
    files_by_year_month: dict[tuple[str, int], list[Path]] = {}

    for file_path in directory_path.iterdir():
        file_year, file_month = _extract_year_month_from_file_name(file_path.name)
        if file_year:
            files_by_year.setdefault(file_year, []).append(file_path)
            if file_month:
                files_by_year_month.setdefault((file_year, file_month), []).append(file_path)

    return files_by_year, files_by_year_month


def _read_weather_file(file_path: Path) -> list[WeatherReading]:
    readings: list[WeatherReading] = []

    with open(file_path, 'r', encoding='utf-8') as file_handle:
        file_handle.readline()

        for line in file_handle:
            reading = parse_weather_line(line)
            if reading:
                readings.append(reading)

    return readings


def _collect_readings(
    files_by_year: dict[str, list[Path]],
    files_by_year_month: dict[tuple[str, int], list[Path]],
    year_month: str,
) -> list[WeatherReading]:
    readings: list[WeatherReading] = []
    target_year, target_month = _parse_year_month(year_month)

    matching_files: list[Path] = []
    if target_month is None:
        matching_files = files_by_year.get(target_year, [])
    else:
        matching_files = files_by_year_month.get((target_year, target_month), [])

    for file_path in matching_files:
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
    files_by_year, files_by_year_month = _build_file_index(base_path)
    reports_count = min(len(argument_types), len(year_months))

    for index in range(reports_count):
        file_readings = _collect_readings(files_by_year, files_by_year_month, year_months[index])
        if file_readings:
            calculate(file_readings, argument_types[index], year_months[index])




