# Weather Man CLI

A Python command-line tool for analyzing historical Murree weather files and producing yearly summaries, monthly averages and terminal charts.

## Reports

- Yearly maximum temperature with its date
- Yearly minimum temperature with its date
- Yearly maximum humidity with its date
- Monthly average maximum temperature
- Monthly average minimum temperature
- Monthly average humidity
- Day-by-day terminal charts for a selected month

## Input

The tool expects weather files containing dated temperature and humidity observations. Select the data directory and date range using the command-line options implemented by the project.

## Setup

~~~bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
~~~

Run the CLI entry point with Python and use its help option to inspect the supported report flags:

~~~bash
python main.py --help
~~~

If the entry-point filename differs in your checkout, run the main weather CLI module present in the repository.

## Engineering concepts

- Parsing structured historical files
- Date-range filtering
- Aggregation across daily observations
- Defensive handling of missing values
- Terminal visualization
- Separation of reporting from data loading

## Expected data quality

Real weather datasets can contain missing values or inconsistent columns. The parser should skip invalid measurements without treating them as zero, because doing so would distort averages and extreme-value reports.

## Potential improvements

- Add argparse help examples
- Include a small anonymized sample dataset
- Add unit tests for parsing and aggregation
- Export reports to JSON or CSV
- Package the tool as an installable command

## Author

Built by [Muhammad Raza Ali](https://github.com/RazaAli313).
