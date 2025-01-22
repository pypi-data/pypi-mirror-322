from argparse import ArgumentParser
import sys
from ._version import __version__

try:
    from ewoksorange.canvas.main import main as ewoksorange_main
except ImportError:
    ewoksorange_main = None


def main(argv=None):
    parser = ArgumentParser(add_help=False)

    parser.add_argument(
        "--version",
        action="store_true",
        help="Display version",
    )
    if argv is None:
        argv = sys.argv
    options, _ = parser.parse_known_args(argv[1:])

    if options.version:
        print(f"Darfix version: {__version__}")
        return
    if ewoksorange_main is None:
        raise ImportError("Install darfix[full] to use the Orange canvas.")
    ewoksorange_main()


if __name__ == "__main__":
    sys.exit(main())
