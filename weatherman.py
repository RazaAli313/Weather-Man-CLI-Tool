import sys
import argparse
from weatherman.loader import load_directory
from weatherman.app_logger import logger
from time import sleep


def main() -> None:
    """
    Main Entry Point Function to call loaders to load the concerned data
    of the user as per passed user's command line arguments.
    
    Usage: weatherman.py /path/to/files-dir -e 2002
           weatherman.py /path/to/files-dir -a 2005/6
           weatherman.py /path/to/files-dir -c 2011/3
           weatherman.py /path/to/files-dir -c 2011/03 -a 2011/3 -e 2011
    """
    logger.info("Starting...")
    parser = argparse.ArgumentParser(
        prog="weatherman.py",
        description="Weather Man CLI Tool: generate reports from a directory of weather files",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    class AppendPair(argparse.Action):
        """Custom action that preserves the order of flags and their values."""

        def __call__(self, parser, namespace, values, option_string=None):
            if not hasattr(namespace, 'argument_types'):
                setattr(namespace, 'argument_types', [])
                setattr(namespace, 'year_months', [])
            namespace.argument_types.append(option_string)
            namespace.year_months.append(values)

    parser.add_argument('directory_path', help='Path to directory containing weather files')
    parser.add_argument('-e', metavar='YEAR', action=AppendPair, help='Yearly report for YEAR')
    parser.add_argument('-a', metavar='YEAR/MONTH', action=AppendPair, help='Monthly report for YEAR/MONTH')
    parser.add_argument('-c', metavar='YEAR/MONTH', action=AppendPair, help='Chart report for YEAR/MONTH')
    parser.add_argument('-b', metavar='YEAR/MONTH', action=AppendPair, help='Combined chart report for YEAR/MONTH')

    args = parser.parse_args()

    directory_path = args.directory_path

    argument_types = getattr(args, 'argument_types', [])
    year_months = getattr(args, 'year_months', [])

    if not argument_types or not year_months:
        logger.info("Error: No flag-value pairs provided. See usage examples below:\n")
        parser.logger.info_help()
        return

    try:
        load_directory(directory_path, argument_types, year_months)
    except Exception as e:
        logger.info(f"Error loading files: {e}")
        logger.info("Ensure the directory path is correct and readable.")

    logger.info("Terminating...")

if __name__ == "__main__":
    # Welcome message with animation
    for i in range(14):
        logger.info("-", end="", flush=True)
        sleep(0.06)

    welcome_sentence = "Welcome to Weather Man CLI Tool"
    for word in welcome_sentence:
        logger.info(word, end="", flush=True)
        sleep(0.06)

    for i in range(14):
        logger.info("-", end="", flush=True)
        sleep(0.06)

    logger.info("\n\n")
    sleep(1)

    main()
    logger.info("--------------------------------------\n\n")
