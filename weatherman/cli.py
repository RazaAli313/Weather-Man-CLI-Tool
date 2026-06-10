import argparse


class AppendPair(argparse.Action):
    """Preserve the order of flag/value pairs as they are provided."""

    def __call__(self, parser, namespace, values, option_string=None):
        if not hasattr(namespace, "argument_types"):
            setattr(namespace, "argument_types", [])
            setattr(namespace, "year_months", [])

        namespace.argument_types.append(option_string)
        namespace.year_months.append(values)


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


def parse_cli_arguments() -> tuple[str, list[str], list[str]]:
    parser = build_parser()
    args = parser.parse_args()

    argument_types = getattr(args, "argument_types", [])
    year_months = getattr(args, "year_months", [])

    if not argument_types or not year_months:
        parser.print_help()
        raise SystemExit(1)

    return args.directory_path, argument_types, year_months