import csv
import re
from typing import List, Optional
from weatherman.models import WeatherReading
from weatherman.constants import Regex


def process_row_date(row_data: dict, date_key: str) -> Optional[re.Match]:
    date_str = row_data.get(date_key, "")
    if not date_str:
        return None
    compiled_pattern = re.compile(Regex.YearMonthDay.value)
    return compiled_pattern.match(date_str)


def parse_readings(row_data: dict) -> dict:
    target_fields = [
        "Max TemperatureC",
        "Mean TemperatureC",
        "Min TemperatureC",
        "Max Humidity",
        "Mean Humidity",
        "Min Humidity"
    ]
    parsed_values = {}
    for field in target_fields:
        raw_value = row_data.get(field, "")
        parsed_values[field] = int(raw_value) if raw_value else None
    return parsed_values


class WeatherFileParser:

    
    def parse_files(self, files_matched: List) -> List[WeatherReading]:
        readings: List[WeatherReading] = []

        for file_path in files_matched:
            with open(file_path, 'r', encoding='utf-8') as weather_file:
                reader = csv.DictReader(weather_file)
                fieldnames = [fieldname.strip() for fieldname in (reader.fieldnames or [])]
                date_key = fieldnames[0] if fieldnames else None
                if not date_key:
                    continue

                for row in reader:
                    row_data = {key.strip(): value.strip() for key, value in row.items() if key is not None and value is not None}
                    
                    date_match = process_row_date(row_data, date_key)
                    if not date_match:
                        continue
                    
                    year = int(date_match.group('year'))
                    month = int(date_match.group('month'))
                    day = int(date_match.group('day'))

                    parsed_values = parse_readings(row_data)
                    date_str = row_data.get(date_key, "")
                    
                    reading = WeatherReading(
                        date=date_str,
                        day=day,
                        month=month,
                        year=year,
                        maximum_temperature=parsed_values["Max TemperatureC"],
                        mean_temperature=parsed_values["Mean TemperatureC"],
                        min_temperature=parsed_values["Min TemperatureC"],
                        maximum_humidity=parsed_values["Max Humidity"],
                        mean_humidity=parsed_values["Mean Humidity"],
                        min_humidity=parsed_values["Min Humidity"]
                    )
                    readings.append(reading)

        readings.sort(key=lambda reading: (reading.year, reading.month, reading.day))
        return readings
