from typing import List
from weatherman.loader import WeatherDirectoryLoader
from weatherman.file_parser import WeatherFileParser
from weatherman.weather_statistics_calculator import WeatherCalculator
from weatherman.report_generator import WeatherReportGenerator
from weatherman.models import WeatherReading
from weatherman.logger import logger


class WeatherManApp:
    def __init__(self, directory_path: str) -> None:
        self.loader = WeatherDirectoryLoader(directory_path)
        self.parser = WeatherFileParser()
        self.calculator = WeatherCalculator()
        self.reporter = WeatherReportGenerator()
        self.report_actions = {
            "-e": self.handle_yearly_report,
            "-a": self.handle_monthly_report,
            "-c": self.handle_bar_chart_report,
            "-b": self.handle_combined_chart_report
        }

    def handle_yearly_report(self, weather_readings: List[WeatherReading]) -> None:
        yearly_report = self.calculator.calculate_yearly_statistics(weather_readings)
        self.reporter.generate_yearly_report(yearly_report)

    def handle_monthly_report(self, weather_readings: List[WeatherReading]) -> None:
        monthly_report = self.calculator.calculate_monthly_statistics(weather_readings)
        self.reporter.generate_monthly_report(monthly_report)

    def handle_bar_chart_report(self, weather_readings: List[WeatherReading]) -> None:
        monthly_report = self.calculator.calculate_monthly_statistics(weather_readings)
        self.reporter.generate_bar_chart(monthly_report)

    def handle_combined_chart_report(self, weather_readings: List[WeatherReading]) -> None:
        monthly_report = self.calculator.calculate_monthly_statistics(weather_readings)
        self.reporter.generate_combined_bar_chart(monthly_report)

    def process_arguments(self, argument: str, argument_type: str) -> None:
        files_matched = self.loader.load_matching_files(argument)
        if files_matched:
            weather_readings = self.parser.parse_files(files_matched)
            if weather_readings:
                action = self.report_actions.get(argument_type)
                if action:
                    action(weather_readings)
            else:
                logger.info("No weather data found.")
        else:
            logger.info("No weather data found.")

    def run(self, arguments_types: List[str], year_months: List[str]) -> None:
        for argument, argument_type in zip(year_months, arguments_types):
            self.process_arguments(argument, argument_type)
