from weatherman.models import YearlyReport, MonthlyReport
from weatherman.logger import logger
from weatherman.constants import Color


def print_yearly_report(report: YearlyReport) -> None:
    
    highest_date = report.highest_temperature_day.split('-')
    highest_day = int(highest_date[2])
    highest_month = get_month_name(int(highest_date[1]))
    
    lowest_date = report.lowest_temperature_day.split('-')
    lowest_day = int(lowest_date[2])
    lowest_month = get_month_name(int(lowest_date[1]))
    
    humidity_date = report.maximum_humidity_day.split('-')
    humidity_day = int(humidity_date[2])
    humidity_month = get_month_name(int(humidity_date[1]))
    
    logger.info(f"Highest: {report.highest_temperature}C on {highest_month} {highest_day}")
    logger.info(f"Lowest: {report.lowest_temperature}C on {lowest_month} {lowest_day}")
    logger.info(f"Humidity: {report.maximum_humidity}% on {humidity_month} {humidity_day}")


def print_monthly_report(report: MonthlyReport, year: int, month: int) -> None:
    
    logger.info(f"Highest Average: {int(report.avg_highest_temperature)}C")
    logger.info(f"Lowest Average: {int(report.avg_lowest_temperature)}C")
    logger.info(f"Average Mean Humidity: {int(report.avg_mean_humidity)}%")


def print_chart_report(report: MonthlyReport, year: int, month: int) -> None:
    
    month_name = get_month_name(month)
    logger.info(f"{month_name} {year}")
    
    sorted_readings = sorted(report.daily_readings, key=lambda r: r.day)
    
    for reading in sorted_readings:
        if reading.maximum_temperature is not None and reading.min_temperature is not None:
            day_str = f"{reading.day:02d}"

            high_bar = "+" * max(0, reading.maximum_temperature)
            logger.info(f"{day_str} {Color.RED.value}{high_bar}{Color.RESET.value} {reading.maximum_temperature}C")

            low_bar = "+" * max(0, reading.min_temperature)
            logger.info(f"{day_str} {Color.BLUE.value}{low_bar}{Color.RESET.value} {reading.min_temperature}C")


def print_combined_chart_report(report: MonthlyReport, year: int, month: int) -> None:
    
    month_name = get_month_name(month)
    logger.info(f"{month_name} {year}")
    sorted_readings = sorted(report.daily_readings, key=lambda r: r.day)
    
    for reading in sorted_readings:
        if reading.maximum_temperature is not None and reading.min_temperature is not None:
            day_str = f"{reading.day:02d}"
            min_val = max(0, reading.min_temperature)
            maximum_val = max(0, reading.maximum_temperature)
            blue_bar = "+" * min_val
            red_bar = "+" * max(0, maximum_val - min_val)

            logger.info(f"{day_str} {Color.BLUE.value}{blue_bar}{Color.RESET.value}{Color.RED.value}{red_bar}{Color.RESET.value} {min_val}C - {maximum_val}C")


def get_month_name(month: int) -> str:
    
    months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
    return months[month - 1] if 1 <= month <= 12 else "Unknown"
