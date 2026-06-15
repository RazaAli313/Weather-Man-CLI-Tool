# Weather-Man CLI Tool

A command-line tool for analyzing and reporting weather data from Murree weather files. This tool processes historical weather data and generates detailed reports on temperatureerature extremes, averages, and humidity patterns.

## Features

- **Yearly Reports**: Find highest and lowest temperatureeratures, and maximum_ humidity for a given year
- **Monthly Reports**: Calculate average temperatureeratures and humidity for specific month/year combinations
- **Chart Reports**: Generate ASCII bar charts showing temperatureerature variations for a specific month
- **Flexible Date Filtering**: Supports various date formats for querying (YYYY/M or YYYY/MM)
- **Multiple Query Types**: Combine different query types in a single run

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd Weather-Man-CLI-Tool
   ```

## Usage

The tool accepts command-line arguments in the format:

```bash
python weatherman.py /path/to/data-directory [OPTIONS]
```

### Available Options

| Option | Description | Format |
|--------|-------------|--------|
| `-e` | Extreme temperatureeratures (yearly report) | `-e YYYY` |
| `-a` | Average temperatureeratures (monthly report) | `-a YYYY/M` or `-a YYYY/MM` |
| `-c` | Chart report | `-c YYYY/M` or `-c YYYY/MM` |
| `-b` | Double Horizontal Bar report | `-b YYYY/M`


### Examples

**Get extreme temperatureeratures for 2005:**
```bash
python weatherman.py data-source/weatherfiles -e 2005
```

**Get average temperatureeratures for June 2011:**
```bash
python weatherman.py data-source/weatherfiles -a 2011/6
```

**Get chart for March 2011:**
```bash
python weatherman.py data-source/weatherfiles -c 2011/3
```

**Double Horizontal Bars:**
```bash
python weatherman.py data-source/weatherfiles -b 2011/03
```
**Combine multiple queries:**
```bash
python weatherman.py data-source/weatherfiles -c 2011/03 -a 2011/3 -e 2011
```

## Sample Output

### Yearly Report (-e)
```
Highest: 32C on August 15
Lowest: -5C on January 2
Humidity: 98% on June 20
```

### Monthly Report (-a)
```
Highest Average: 28C
Lowest Average: 18C
Average Mean Humidity: 65%
```

### Chart Report (-c)
Visual ASCII bar chart showing temperatureerature distribution for the specified month.

## Project Structure

```
Weather-Man-CLI-Tool/
├── README.md                 # Project documentation
├── weatherman.py            # Main entry point
├──.gitignore
├── data-source/
│   └── weatherfiles/        # Historical weather data files
└── weatherman/              # Main package
    ├── __init__.py
    ├── models.py            # Data structures (WeatherReading, Reports)
    ├── file_parser.py       # Weather data parsing logic
    ├──cli_parser.py         #CLI parser logic  
    ├── weather_statistics_calculator.py        # Report calculations
    ├── loader.py            # File directory loading
    ├──constants.py          # File having enum of colors for console
    ├──app.py                # WeatherMan Class
    ├──logger.py             # Logger
    └── report_generator.py   # Report formatting and display
    
```

## Data Format

Weather data files are expected to be in CSV format with the following columns:
- Date (YYYY-M-D)
- Max Temperature
- Mean Temperature
- Min Temperature
- Max Humidity
- Mean Humidity
- Min Humidity

Example:
```
2005-1-1,25,20,15,80,65,50
2005-1-2,26,21,16,82,67,52
```

## Error Handling

The tool validates:
- Minimum required arguments (path and at least one query)
- Correct flag-value pair format
- Data file readability and correct CSV format
- Valid date ranges in input files

If errors occur, the tool will display helpful error messages.

## License

This project is provided as-is for educational and analysis purposes.
