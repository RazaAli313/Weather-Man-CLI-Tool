import re
import calendar
from typing import List, Optional
from weatherman.models import WeatherReading, YearlyReport, MonthlyReport
from weatherman.constants import Regex
from weatherman.utils import format_date_to_month_day
from weatherman.models import Date

def concatenate_month_day(date: Date) -> str:
    formatted_date = f"{date.month} {date.day}"
    return formatted_date


class WeatherCalculator:

    def calculate_yearly_statistics(self, readings: List[WeatherReading]) -> Optional[YearlyReport]:
        report = None
        readings_with_maximum_temperature = [reading for reading in readings if reading.maximum_temperature is not None]
        readings_with_minimum_temperature = [reading for reading in readings if reading.min_temperature is not None]
        readings_with_maximum_humidity = [reading for reading in readings if reading.maximum_humidity is not None]

        if readings_with_maximum_temperature and readings_with_minimum_temperature and readings_with_maximum_humidity:
            highest_temperature_reading = max(readings_with_maximum_temperature, key=lambda reading: reading.maximum_temperature)
            highest_temperature = highest_temperature_reading.maximum_temperature
            highest_temperature_day = concatenate_month_day(format_date_to_month_day(highest_temperature_reading.date,Regex.YearMonthDay))

            lowest_temperature_reading = min(readings_with_minimum_temperature, key=lambda reading: reading.min_temperature)
            lowest_temperature = lowest_temperature_reading.min_temperature
            lowest_temperature_day = concatenate_month_day(format_date_to_month_day(lowest_temperature_reading.date,Regex.YearMonthDay))

            maximum_humidity_reading = max(readings_with_maximum_humidity, key=lambda reading: reading.maximum_humidity)
            maximum_humidity = maximum_humidity_reading.maximum_humidity
            maximum_humidity_day = concatenate_month_day(format_date_to_month_day(maximum_humidity_reading.date,Regex.YearMonthDay))

            report = YearlyReport(
                highest_temperature=highest_temperature,
                highest_temperature_day=highest_temperature_day,
                lowest_temperature=lowest_temperature,
                lowest_temperature_day=lowest_temperature_day,
                maximum_humidity=maximum_humidity,
                maximum_humidity_day=maximum_humidity_day
            )
        return report

    def calculate_monthly_statistics(self, readings: List[WeatherReading]) -> Optional[MonthlyReport]:
        report = None
        maximum_temperatures = [reading.maximum_temperature for reading in readings if reading.maximum_temperature is not None]
        minimum_temperatures = [reading.min_temperature for reading in readings if reading.min_temperature is not None]
        mean_humidities = [reading.mean_humidity for reading in readings if reading.mean_humidity is not None]

        if maximum_temperatures and minimum_temperatures and mean_humidities:
            average_highest_temperature = sum(maximum_temperatures) / len(maximum_temperatures)
            average_lowest_temperature = sum(minimum_temperatures) / len(minimum_temperatures)
            average_mean_humidity = sum(mean_humidities) / len(mean_humidities)

            report = MonthlyReport(
                average_highest_temperature=average_highest_temperature,
                average_lowest_temperature=average_lowest_temperature,
                average_mean_humidity=average_mean_humidity,
                daily_readings=readings
            )
        return report
