from weatherman.cli_parser import parse_cli_arguments
from weatherman.app import WeatherManApp


def main() -> None:
    arguments = parse_cli_arguments()
    app = WeatherManApp(arguments.directory_path)
    app.run(arguments.arguments_types, arguments.year_months)

if __name__ == "__main__":
    main()
