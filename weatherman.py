from weatherman.file_loader import load_directory
from weatherman.cli_parser import parse_cli_arguments


def main() -> None:
    """Main entry point that delegates CLI parsing and directory loading."""
    directory_path, argument_types, year_months = parse_cli_arguments()
    load_directory(directory_path, argument_types, year_months)

if __name__ == "__main__":
    main()
