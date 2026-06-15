import calendar
from typing import Optional
from weatherman.models import YearlyReport, MonthlyReport, Temperature, WeatherReading
from weatherman.constants import Color
from weatherman.logger import logger

class WeatherReportGenerator:
    def format_value(self, value_to_format: int) -> str:
        formatted_value_string = str(value_to_format)
        if 0 <= value_to_format < 10:
            formatted_value_string = f"{value_to_format:02d}"
        return formatted_value_string

    def generate_yearly_report(self, report: YearlyReport) -> None:
        logger.info(f"Highest: {self.format_value(report.highest_temperature)}C on {report.highest_temperature_day}")
        logger.info(f"Lowest: {self.format_value(report.lowest_temperature)}C on {report.lowest_temperature_day}")
        logger.info(f"Humidity: {self.format_value(report.maximum_humidity)}% on {report.maximum_humidity_day}")

    def generate_monthly_report(self, report: MonthlyReport) -> None:
        highest_average = round(report.average_highest_temperature)
        lowest_average = round(report.average_lowest_temperature)
        mean_humidity_average = round(report.average_mean_humidity)

        logger.info(f"Highest Average: {self.format_value(highest_average)}C")
        logger.info(f"Lowest Average: {self.format_value(lowest_average)}C")
        logger.info(f"Average Mean Humidity: {self.format_value(mean_humidity_average)}%")

    def get_temperature(self, reading: WeatherReading) -> Optional[Temperature]:
        if reading.maximum_temperature is not None and reading.min_temperature is not None:
            return Temperature(reading.min_temperature, reading.maximum_temperature)
        return None

    def display_month_year(self, report: MonthlyReport) -> None:
        first_reading = next(iter(report.daily_readings), None)
        if first_reading:
            month_name = calendar.month_name[first_reading.month]
            logger.info(f"{month_name} {first_reading.year}")

    def generate_bar_chart(self, report: MonthlyReport) -> None:
        self.display_month_year(report)
        for reading in report.daily_readings:
            temperature = self.get_temperature(reading)
            if temperature:
                day_str = f"{reading.day:02d}"
                maximum_temperature_bar = "+" * max(0, temperature.maximum_temperature)
                maximum_temperature_string = f"{self.format_value(temperature.maximum_temperature)}C"
                logger.info(f"{Color.RED.value}{day_str} {maximum_temperature_bar} {maximum_temperature_string}{Color.RESET.value}")

                minimum_temperature_bar = "+" * max(0, temperature.minimum_temperature)
                minimum_temperature_string = f"{self.format_value(temperature.minimum_temperature)}C"
                logger.info(f"{Color.BLUE.value}{day_str} {minimum_temperature_bar} {minimum_temperature_string}{Color.RESET.value}")

    def generate_combined_bar_chart(self, report: MonthlyReport) -> None:
        self.display_month_year(report)
        for reading in report.daily_readings:
            temperature = self.get_temperature(reading)
            if temperature:
                day_str = f"{reading.day:02d}"
                minimum_temperature_count = max(0, temperature.minimum_temperature)
                maximum_temperature_count = max(0, temperature.maximum_temperature)

                blue_bar = f"{Color.BLUE.value}{'+' * minimum_temperature_count}"
                red_bar = f"{Color.RED.value}{'+' * maximum_temperature_count}"
                color_reset_code = Color.RESET.value

                value_string = f"{self.format_value(temperature.minimum_temperature)}C - {self.format_value(temperature.maximum_temperature)}C"
                logger.info(f"{day_str} {blue_bar}{red_bar}{color_reset_code} {value_string}")
