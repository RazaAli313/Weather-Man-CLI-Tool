import csv
import re
from typing import List
from weatherman.models import WeatherReading

class WeatherFileParser:
    def parse_files(self, files_matched: List) -> List[WeatherReading]:
        readings: List[WeatherReading] = []

        for file_path in files_matched:
            with open(file_path, 'r', encoding='utf-8') as weather_file:
                reader = csv.reader(weather_file)
                headers = next(reader, None)
                if not headers:
                    continue
                
                headers = [header_item.strip() for header_item in headers]
                date_key = next(iter(headers), None)
                if not date_key:
                    continue

                for row in reader:
                    if not row or all(cell_value.strip() == '' for cell_value in row):
                        continue
                    
                    row_data = {header_name: cell_value.strip() for header_name, cell_value in zip(headers, row)}
                    date_str = row_data.get(date_key, "")
                    if not date_str:
                        continue
                    
                    date_match = re.match(r"^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$", date_str)
                    if not date_match:
                        continue
                    
                    year = int(date_match.group('year'))
                    month = int(date_match.group('month'))
                    day = int(date_match.group('day'))

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
                        raw_value = row_data.get(field, "").strip()
                        parsed_values[field] = int(float(raw_value)) if raw_value and raw_value.replace('-', '', 1).replace('.', '', 1).isdigit() else None

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
        