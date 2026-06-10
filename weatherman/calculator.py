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
    
    if not yearly_readings:
        return None
    
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
    
    return YearlyReport(
        highest_temp=highest_temp,
        highest_temp_day=highest_temp_day,
        lowest_temp=lowest_temp,
        lowest_temp_day=lowest_temp_day,
        max_humidity=max_humidity,
        max_humidity_day=max_humidity_day
    )


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
    
    if not monthly_readings:
        return None
    
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
    
    return MonthlyReport(
        avg_highest_temp=avg_highest,
        avg_lowest_temp=avg_lowest,
        avg_mean_humidity=avg_humidity,
        daily_readings=monthly_readings
    )


def calculate(readings: List[WeatherReading], argument_type: str, 
              timeline: str) -> None:
    """
    Main calculator function that routes to appropriate report generator.
    
    Args:
        readings: List of WeatherReading objects
        argument_type: Report type flag (-e, -a, or -c)
        timeline: Year or month value
    """
    try:
        if argument_type == "-e":
            # Yearly report
            year = int(timeline)
            report = calculate_yearly_report(readings, year)
            if report:
                report_generator.print_yearly_report(report)
            else:
                print(f"No data found for year {year}")
                
        elif argument_type == "-a":
            # Monthly report
            date_parts = timeline.split('/')
            year = int(date_parts[0])
            month = int(date_parts[1])
            report = calculate_monthly_report(readings, year, month)
            if report:
                report_generator.print_monthly_report(report, year, month)
            else:
                print(f"No data found for {year}/{month}")
                
        elif argument_type == "-c":
            # Chart report
            date_parts = timeline.split('/')
            year = int(date_parts[0])
            month = int(date_parts[1])
            report = calculate_monthly_report(readings, year, month)
            if report:
                report_generator.print_chart_report(report, year, month)
            else:
                print(f"No data found for {year}/{month}")
        elif argument_type == "-b":
            # Bonus combined chart report
            date_parts = timeline.split('/')
            year = int(date_parts[0])
            month = int(date_parts[1])
            report = calculate_monthly_report(readings, year, month)
            if report:
                report_generator.print_combined_chart_report(report, year, month)
            else:
                print(f"No data found for {year}/{month}")
    except ValueError as e:
        print(f"Error parsing timeline {timeline}: {e}")

