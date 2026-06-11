from weatherman.models import WeatherReading, YearlyReport, MonthlyReport
from weatherman import report_generator
from weatherman.app_logger import logger
from typing import List


def calculate_yearly_report(readings: list[WeatherReading], 
                           year: int) -> YearlyReport:
    """
    Calculate yearly weather statistics.
    
    Args:
        readings: List of WeatherReading objects
        year: Target year
        
    Returns:
        YearlyReport object with statistics
    """
    # Filter readings for the target year
    yearly_readings = [reading for reading in readings if reading.year == year]

    result = None

    valid_max_temp_readings = [reading for reading in yearly_readings if reading.max_temp is not None]
    valid_min_temp_readings = [reading for reading in yearly_readings if reading.min_temp is not None]
    valid_max_humidity_readings = [reading for reading in yearly_readings if reading.max_humidity is not None]

    if yearly_readings and valid_max_temp_readings and valid_min_temp_readings and valid_max_humidity_readings:
        highest_temp_reading = max(valid_max_temp_readings, key=lambda reading: reading.max_temp)
        lowest_temp_reading = min(valid_min_temp_readings, key=lambda reading: reading.min_temp)
        max_humidity_reading = max(valid_max_humidity_readings, key=lambda reading: reading.max_humidity)

        result = YearlyReport(
            highest_temp=highest_temp_reading.max_temp,
            highest_temp_day=highest_temp_reading.date,
            lowest_temp=lowest_temp_reading.min_temp,
            lowest_temp_day=lowest_temp_reading.date,
            max_humidity=max_humidity_reading.max_humidity,
            max_humidity_day=max_humidity_reading.date
        )

    return result


def calculate_monthly_report(readings: list[WeatherReading], 
                            year: int, month: int) -> MonthlyReport:
    """
    Calculate monthly weather statistics.
    
    Args:
        readings: List of WeatherReading objects
        year: Target year
        month: Target month
        
    Returns:
        MonthlyReport object with statistics
    """
    # Filter readings for target month
    monthly_readings = [reading for reading in readings if reading.year == year and reading.month == month]

    result = None

    valid_max_temps = [reading.max_temp for reading in monthly_readings if reading.max_temp is not None]
    valid_min_temps = [reading.min_temp for reading in monthly_readings if reading.min_temp is not None]
    valid_mean_humidity = [reading.mean_humidity for reading in monthly_readings if reading.mean_humidity is not None]

    if monthly_readings and valid_max_temps and valid_min_temps and valid_mean_humidity:
        result = MonthlyReport(
            avg_highest_temp=sum(valid_max_temps) / len(valid_max_temps),
            avg_lowest_temp=sum(valid_min_temps) / len(valid_min_temps),
            avg_mean_humidity=sum(valid_mean_humidity) / len(valid_mean_humidity),
            daily_readings=monthly_readings
        )

    return result


def calculate(readings: List[WeatherReading], argument_type: str, 
              year_month: str) -> None:
    """
    Main calculator function that routes to appropriate report generator.
    
    Args:
        readings: List of WeatherReading objects
        argument_type: Report type flag (-e, -a, or -c)
        year_month: Year or month value
    """
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
            year = int(year_month)
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
