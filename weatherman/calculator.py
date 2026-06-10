from weatherman.models import WeatherReading, YearlyReport, MonthlyReport
from weatherman import report_generator
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
    yearly_readings = [r for r in readings if r.year == year]

    result = None

    if yearly_readings:
        highest_temp = -999
        highest_temp_day = ""
        lowest_temp = 999
        lowest_temp_day = ""
        max_humidity = -1
        max_humidity_day = ""

        for reading in yearly_readings:
            if reading.max_temp and reading.max_temp > highest_temp:
                highest_temp = reading.max_temp
                highest_temp_day = reading.date

            if reading.min_temp and reading.min_temp < lowest_temp:
                lowest_temp = reading.min_temp
                lowest_temp_day = reading.date

            if reading.max_humidity and reading.max_humidity > max_humidity:
                max_humidity = reading.max_humidity
                max_humidity_day = reading.date

        result = YearlyReport(
            highest_temp=highest_temp,
            highest_temp_day=highest_temp_day,
            lowest_temp=lowest_temp,
            lowest_temp_day=lowest_temp_day,
            max_humidity=max_humidity,
            max_humidity_day=max_humidity_day
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
    monthly_readings = [r for r in readings if r.year == year and r.month == month]

    result = None

    if monthly_readings:
        total_highest = 0
        total_lowest = 0
        total_humidity = 0
        count_highest = 0
        count_lowest = 0
        count_humidity = 0

        for reading in monthly_readings:
            if reading.max_temp:
                total_highest += reading.max_temp
                count_highest += 1

            if reading.min_temp:
                total_lowest += reading.min_temp
                count_lowest += 1

            if reading.mean_humidity:
                total_humidity += reading.mean_humidity
                count_humidity += 1

        avg_highest = total_highest / count_highest if count_highest > 0 else 0
        avg_lowest = total_lowest / count_lowest if count_lowest > 0 else 0
        avg_humidity = total_humidity / count_humidity if count_humidity > 0 else 0

        result = MonthlyReport(
            avg_highest_temp=avg_highest,
            avg_lowest_temp=avg_lowest,
            avg_mean_humidity=avg_humidity,
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

    try:
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
    except ValueError as e:
        logger.info(f"Error parsing year_month {year_month}: {e}")

