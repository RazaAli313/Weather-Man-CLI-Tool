from weatherman.models import WeatherReading, YearlyReport, MonthlyReport
from weatherman import report_generator
from weatherman.logger import logger
from typing import List


def calculate_yearly_report(readings: list[WeatherReading], 
                           year: int) -> YearlyReport:
    
    yearly_readings = [reading for reading in readings if reading.year == year]
    result = None

    maximum_temperature_readings = [reading for reading in yearly_readings if reading.maximum_temperature is not None]
    min_temperature_readings = [reading for reading in yearly_readings if reading.min_temperature is not None]
    maximum_humidity_readings = [reading for reading in yearly_readings if reading.maximum_humidity is not None]

    if yearly_readings and maximum_temperature_readings and min_temperature_readings and maximum_humidity_readings:
        highest_temperature_reading = max(maximum_temperature_readings, key=lambda reading: reading.maximum_temperature)
        lowest_temperature_reading = min(min_temperature_readings, key=lambda reading: reading.min_temperature)
        maximum_humidity_reading = max(maximum_humidity_readings, key=lambda reading: reading.maximum_humidity)

        result = YearlyReport(
            highest_temperature=highest_temperature_reading.maximum_temperature,
            highest_temperature_day=highest_temperature_reading.date,
            lowest_temperature=lowest_temperature_reading.min_temperature,
            lowest_temperature_day=lowest_temperature_reading.date,
            maximum_humidity=maximum_humidity_reading.maximum_humidity,
            maximum_humidity_day=maximum_humidity_reading.date
        )

    return result


def calculate_monthly_report(readings: list[WeatherReading], 
                            year: int, month: int) -> MonthlyReport:
    
    monthly_readings = [reading for reading in readings if reading.year == year and reading.month == month]
    result = None

    maximum_temperatures = [reading.maximum_temperature for reading in monthly_readings if reading.maximum_temperature is not None]
    min_temperatures = [reading.min_temperature for reading in monthly_readings if reading.min_temperature is not None]
    mean_humidity = [reading.mean_humidity for reading in monthly_readings if reading.mean_humidity is not None]

    if monthly_readings and maximum_temperatures and min_temperatures and mean_humidity:
        result = MonthlyReport(
            avg_highest_temperature=sum(maximum_temperatures) / len(maximum_temperatures),
            avg_lowest_temperature=sum(min_temperatures) / len(min_temperatures),
            avg_mean_humidity=sum(mean_humidity) / len(mean_humidity),
            daily_readings=monthly_readings
        )

    return result


def calculate(readings: List[WeatherReading], argument_type: str, 
              year_month: str) -> None:
    
    def _parse_year_month(tl: str) -> tuple[int, int]:
        parts = tl.split('/')
        if len(parts) != 2:
            raise ValueError("year_month must be in 'YYYY/MM' format")
        return int(parts[0]), int(parts[1])

    def _handle_monthly_action(readings: List[WeatherReading], tl: str, action_fn) -> None:
        year, month = _parse_year_month(tl)
        report = calculate_monthly_report(readings, year, month)
        if report:
            action_fn(report, year, month)
        else:
            logger.info(f"No data found for {year}/{month}")

    if argument_type == "-e":
        try:
            year = int(year_month)
        except ValueError:
            logger.info(f"Invalid yearly query: expected YYYY, got {year_month}")
            return

        report = calculate_yearly_report(readings, year)
        if report:
            report_generator.print_yearly_report(report)
        else:
            logger.info(f"No data found for year {year}")

    elif argument_type in ("-a", "-c", "-b"):
        action_map = {
            "-a": report_generator.print_monthly_report,
            "-c": report_generator.print_chart_report,
            "-b": report_generator.print_combined_chart_report,
        }
        action_fn = action_map[argument_type]
        _handle_monthly_action(readings, year_month, action_fn)

    else:
        logger.info(f"Unknown argument type: {argument_type}")
