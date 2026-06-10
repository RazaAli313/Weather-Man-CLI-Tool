from pathlib import Path
from weatherman.calculator import calculate
from weatherman.models import WeatherReading
from typing import Optional, List


def parse_weather_line(line: str) -> Optional[WeatherReading]:
    """
    Parse a single weather data line and return a WeatherReading object.
    
    Args:
        line: A CSV line from weather file
        
    Returns:
        WeatherReading object or None if parsing fails
    """
    try:
        parts = line.strip().split(',')
        if len(parts) < 9:
            return None
            
        # Parse date (format: YYYY-M-D)
        date_str = parts[0]
        date_parts = date_str.split('-')
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        
        # Parse temperatures and humidity
        max_temp = int(parts[1]) if parts[1] else None
        mean_temp = int(parts[2]) if parts[2] else None
        min_temp = int(parts[3]) if parts[3] else None
        max_humidity = int(parts[7]) if len(parts) > 7 and parts[7] else None
        mean_humidity = int(parts[8]) if len(parts) > 8 and parts[8] else None
        min_humidity = int(parts[9]) if len(parts) > 9 and parts[9] else None
        
        return WeatherReading(
            date=date_str,
            day=day,
            month=month,
            year=year,
            max_temp=max_temp,
            mean_temp=mean_temp,
            min_temp=min_temp,
            max_humidity=max_humidity,
            mean_humidity=mean_humidity,
            min_humidity=min_humidity
        )
    except (ValueError, IndexError):
        return None


def parse(directory_path: str, argument_types: List[str], 
          timelines: List[str]) -> None:
    """
    Parse weather files and generate reports based on arguments.
    
    Args:
        directory_path: Path to weather files directory
        argument_types: List of report type flags (-e, -a, -c)
        timelines: List of year/month values corresponding to each flag
    """
    directory_path = Path(directory_path)
    
    from calendar import month_abbr

    for i in range(len(timelines)):
        file_readings = []
        timeline = timelines[i]

        # Determine whether timeline is year or year/month
        target_year = None
        target_month = None
        if '/' in timeline:
            parts = timeline.split('/')
            try:
                target_year = str(int(parts[0]))
                target_month = int(parts[1])
            except ValueError:
                target_year = parts[0]
        else:
            target_year = timeline

        # Load matching weather files for this timeline
        for file in directory_path.iterdir():
            name = file.name
            match_file = False
            if target_year and target_year in name:
                if target_month:
                    # match month abbreviation (e.g., Aug)
                    abbr = month_abbr[target_month]
                    if abbr and abbr in name:
                        match_file = True
                else:
                    match_file = True

            if match_file:
                with open(file, 'r', encoding='utf-8') as f:
                    # Skip header line
                    f.readline()

                    # Read all weather lines
                    for line in f:
                        reading = parse_weather_line(line)
                        if reading:
                            file_readings.append(reading)
        
        # Calculate and generate report
        if file_readings:
            calculate(file_readings, argument_types[i], timelines[i])




