from .models import YearlyReport, MonthlyReport

# ANSI color codes
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


def print_yearly_report(report: YearlyReport) -> None:
    """
    Print yearly weather report (Task 1).
    
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
    
    print(f"Highest: {report.highest_temp}C on {highest_month} {highest_day}")
    print(f"Lowest: {report.lowest_temp}C on {lowest_month} {lowest_day}")
    print(f"Humidity: {report.max_humidity}% on {humidity_month} {humidity_day}")


def print_monthly_report(report: MonthlyReport, year: int, month: int) -> None:
    """
    Print monthly weather report (Task 2).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    print(f"Highest Average: {int(report.avg_highest_temp)}C")
    print(f"Lowest Average: {int(report.avg_lowest_temp)}C")
    print(f"Average Mean Humidity: {int(report.avg_mean_humidity)}%")


def print_chart_report(report: MonthlyReport, year: int, month: int) -> None:
    """
    Print chart report with separate high and low temperature bars (Task 3).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    month_name = get_month_name(month)
    print(f"{month_name} {year}")
    
    # Sort by day
    sorted_readings = sorted(report.daily_readings, key=lambda r: r.day)
    
    for reading in sorted_readings:
        if reading.max_temp is not None and reading.min_temp is not None:
            # Format day with leading zero
            day_str = f"{reading.day:02d}"

            # High temperature in red
            high_bar = "+" * max(0, reading.max_temp)
            print(f"{day_str} {RED}{high_bar}{RESET} {reading.max_temp}C")

            # Low temperature in blue
            low_bar = "+" * max(0, reading.min_temp)
            print(f"{day_str} {BLUE}{low_bar}{RESET} {reading.min_temp}C")


def print_combined_chart_report(report: MonthlyReport, year: int, 
                                month: int) -> None:
    """
    Print combined chart with high and low temperature in one line (Task 5 - BONUS).
    
    Args:
        report: MonthlyReport object
        year: Year
        month: Month
    """
    month_name = get_month_name(month)
    print(f"{month_name} {year}")
    
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

            print(f"{day_str} {BLUE}{blue_bar}{RESET}{RED}{red_bar}{RESET} {min_val}C - {max_val}C")


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
