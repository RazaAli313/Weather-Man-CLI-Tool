from weatherman.models import YearlyReport, MonthlyReport
from weatherman.constants import Color

color=Color()


def print_yearly_report(report: YearlyReport) -> None:
    """
    logger.info yearly weather report (Task 1).
    
    Args:
        report: YearlyReport object
    """
    # Format dates to extract day and month name
    highest_date = report.highest_temp_day.split('-')
    highest_day = int(highest_date[2])
    highest_month = get_month_name(int(highest_date[1]))
    
    lowest_date = report.lowest_temp_day.split('-')
    lowest_day = int(lowest_date[2])
    lowest_month = get_month_name(int(lowest_date[1]))
    
    humidity_date = report.max_humidity_day.split('-')
    humidity_day = int(humidity_date[2])
    humidity_month = get_month_name(int(humidity_date[1]))
    
    logger.info(f"Highest: {report.highest_temp}C on {highest_month} {highest_day}")
    logger.info(f"Lowest: {report.lowest_temp}C on {lowest_month} {lowest_day}")
    logger.info(f"Humidity: {report.max_humidity}% on {humidity_month} {humidity_day}")


def print_monthly_report(report: MonthlyReport, year: int, month: int) -> None:
    """
    logger monthly weather report (Task 2).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    logger.info(f"Highest Average: {int(report.avg_highest_temp)}C")
    logger.info(f"Lowest Average: {int(report.avg_lowest_temp)}C")
    logger.info(f"Average Mean Humidity: {int(report.avg_mean_humidity)}%")


def print_chart_report(report: MonthlyReport, year: int, month: int) -> None:
    """
    logger.info chart report with separate high and low temperature bars (Task 3).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    month_name = get_month_name(month)
    logger.info(f"{month_name} {year}")
    
    # Sort by day
    sorted_readings = sorted(report.daily_readings, key=lambda r: r.day)
    
    for reading in sorted_readings:
        if reading.max_temp is not None and reading.min_temp is not None:
            # Format day with leading zero
            day_str = f"{reading.day:02d}"

            # High temperature in red
            high_bar = "+" * max(0, reading.max_temp)
            logger.info(f"{day_str} {color.color.RED}{high_bar}{color.RESET} {reading.max_temp}C")

            # Low temperature in blue
            low_bar = "+" * max(0, reading.min_temp)
            logger.info.info(f"{day_str} {color.BLUE}{low_bar}{color.RESET} {reading.min_temp}C")


def print_combined_chart_report(report: MonthlyReport, year: int, 
                                month: int) -> None:
    """
    logger.info combined chart with high and low temperature in one line (Task 5 - BONUS).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    month_name = get_month_name(month)
    logger.info(f"{month_name} {year}")
    
    # Sort by day
    sorted_readings = sorted(report.daily_readings, key=lambda r: r.day)
    
    for reading in sorted_readings:
        if reading.max_temp is not None and reading.min_temp is not None:
            # Format day with leading zero
            day_str = f"{reading.day:02d}"

            # Calculate bar length based on temperature range
            min_val = max(0, reading.min_temp)
            max_val = max(0, reading.max_temp)

            # Create combined bar: blue for low, red for high (remaining)
            blue_bar = "+" * min_val
            red_bar = "+" * max(0, max_val - min_val)

            logger.info(f"{day_str} {color.BLUE}{blue_bar}{color.RESET}{color.RED}{red_bar}{color.RESET} {min_val}C - {max_val}C")


def get_month_name(month: int) -> str:
    """
    Convert month number to month name.
    
    Args:
        month: Month number (1-12)
        
    Returns:
        Month name
    """
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[month - 1] if 1 <= month <= 12 else "Unknown"
