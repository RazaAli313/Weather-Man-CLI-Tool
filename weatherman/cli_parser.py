import argparse
from weatherman.models import DirectoryLoader

class AppendPair(argparse.Action):
   
    def __call__(self, parser, namespace, year_month_values, flag=None):
        if not hasattr(namespace, "argument_types"):
            setattr(namespace, "argument_types", [])
            setattr(namespace, "year_months", [])

        namespace.argument_types.append(flag)
        namespace.year_months.append(year_month_values)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weatherman.py",
        description="Weather Man CLI Tool: generate reports from a directory of weather files",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument("directory_path", help="Path to directory containing weather files")
    parser.add_argument("-e", metavar="YEAR", action=AppendPair, help="Yearly report for YEAR")
    parser.add_argument("-a", metavar="YEAR/MONTH", action=AppendPair, help="Monthly report for YEAR/MONTH")
    parser.add_argument("-c", metavar="YEAR/MONTH", action=AppendPair, help="Chart report for YEAR/MONTH")
    parser.add_argument("-b", metavar="YEAR/MONTH", action=AppendPair, help="Combined chart report for YEAR/MONTH")

    return parser


def parse_cli_arguments() -> DirectoryLoader:
    parser = build_parser()
    args = parser.parse_args()
    
    arguments_types = getattr(args, "argument_types", [])
    year_months = getattr(args, "year_months", [])

    if not arguments_types or not year_months:
        parser.logger.info_help()
        raise SystemExit(1)
    arguments=DirectoryLoader(args.directory_path, arguments_types, year_months)
    return arguments
