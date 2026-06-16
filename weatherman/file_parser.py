import csv
import re
from typing import List, Optional
from weatherman.models import WeatherReading
from weatherman.constants import YEAR_MONTH_DAY_PATTERN


class WeatherFileParser:
    def _process_row_date(self,row_data: dict, date_key: str) -> Optional[re.Match]:
        date_str = row_data.get(date_key, "")
        compiled_pattern = re.compile(YEAR_MONTH_DAY_PATTERN)
        return compiled_pattern.match(date_str)

    def _parse_readings(self,row_data: dict) -> dict:
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

    def _read_csv(self,file_path):
        with open(file_path, 'r', encoding='utf-8') as weather_file:
            reader = csv.DictReader(weather_file)

            fieldnames = [
                field.strip()
                for field in (reader.fieldnames or [])
            ]

            date_key = fieldnames[0] if fieldnames else None

            rows = []

            for row in reader:
                row_data = {
                    key.strip(): value.strip()
                    for key, value in row.items()
                    if key is not None and value is not None
                }

                rows.append(row_data)

        return rows, date_key

    def parse_files(self, files_matched: List) -> List[WeatherReading]:
        readings = []

        for file_path in files_matched:
            rows, date_key = self._read_csv(file_path)

            for row_data in rows:
                date_match = self._process_row_date(
                    row_data,
                    date_key
                )

                year = int(date_match.group('year'))
                month = int(date_match.group('month'))
                day = int(date_match.group('day'))
                parsed_values = self._parse_readings(row_data)

                readings.append(WeatherReading(
                    date=row_data.get(date_key, ""),
                    day=day,
                    month=month,
                    year=year,
                    maximum_temperature=parsed_values["Max TemperatureC"],
                    mean_temperature=parsed_values["Mean TemperatureC"],
                    min_temperature=parsed_values["Min TemperatureC"],
                    maximum_humidity=parsed_values["Max Humidity"],
                    mean_humidity=parsed_values["Mean Humidity"],
                    min_humidity=parsed_values["Min Humidity"]
                ))

        readings.sort(
            key=lambda r: (r.year, r.month, r.day)
        )

        return readings
