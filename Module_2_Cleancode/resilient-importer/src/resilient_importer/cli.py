"""Command-line interface for the resilient importer.

Provides an ``argparse``-based entry point so the tool can be invoked as::

    python -m resilient_importer.cli users.csv --db path/to/db.json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path

from .importer import Importer


def setup_logging(verbose: bool = False) -> None:
    """Configure structured logging.

    Args:
        verbose: If True, set log level to DEBUG; otherwise INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional list of command-line arguments.  Defaults to
            ``sys.argv[1:]`` when None.

    Returns:
        Exit code: 0 on success, 1 on failure.
    """
    parser = argparse.ArgumentParser(description="Resilient Data Importer")
    parser.add_argument("csv_file", type=Path, help="Path to the CSV file to import")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("users.json"),
        help="Path to the JSON database file",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args(argv)

    setup_logging(args.verbose)

    try:
        importer = Importer(csv_path=args.csv_file, db_path=args.db)
        imported = importer.run()
        print(f"Successfully imported {len(imported)} user(s).")
        return 0
    except Exception as e:
        print(f"Import failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
