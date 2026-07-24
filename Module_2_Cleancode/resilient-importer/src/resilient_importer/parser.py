"""CSV parser for user data.

Reads a CSV file, validates the header columns, and yields User objects
row by row.  A dedicated context-manager class is provided so callers
can use safe ``with`` semantics when opening files.
"""

import csv
from io import TextIOWrapper
from pathlib import Path
from typing import Generator

from .exceptions import FileFormatError
from .models import User


class CSVFileContext:
    """Context manager that safely opens a CSV file for reading.

    Ensures the file handle is closed after use and converts
    file-not-found errors into the project's domain exception.

    Args:
        file_path: Path to the CSV file.

    Raises:
        FileFormatError: If the file does not exist.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._file: TextIOWrapper | None = None

    def __enter__(self) -> "TextIOWrapper":
        if not self.file_path.exists():
            raise FileFormatError(f"File not found: {self.file_path}")
        self._file = open(self.file_path, newline="", encoding="utf-8")
        return self._file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        if self._file:
            self._file.close()


class CSVParser:
    """Parses CSV files containing user data."""

    REQUIRED_FIELDS = {"user_id", "name", "email"}

    def __init__(self, file_path: Path):
        """Initialise the parser with the target CSV file path.

        Args:
            file_path: Path to the CSV file to parse.
        """
        self.file_path = file_path

    def parse(self) -> Generator[User, None, None]:
        """Parse the CSV file and yield User objects.

        Yields:
            User objects constructed from each valid CSV row.

        Raises:
            FileFormatError: If the file is missing, has invalid headers,
                or a row is missing required columns.
        """
        with CSVFileContext(self.file_path) as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None or not self.REQUIRED_FIELDS.issubset(
                reader.fieldnames
            ):
                required = ", ".join(sorted(self.REQUIRED_FIELDS))
                raise FileFormatError(f"CSV must contain columns: {required}")

            for line_num, row in enumerate(reader, start=2):
                yield self._parse_row(row, line_num)

    def _parse_row(self, row: dict[str, str], line_num: int) -> User:
        """Parse a single CSV row into a User object.

        Args:
            row: A dictionary mapping column names to string values.
            line_num: The 1-based line number in the source file.

        Returns:
            A User instance populated from the row values.

        Raises:
            FileFormatError: If a required column is missing or its value
                cannot be stripped (e.g., ``None``).
        """
        try:
            return User(
                user_id=row["user_id"].strip(),
                name=row["name"].strip(),
                email=row["email"].strip(),
            )
        except (KeyError, AttributeError) as e:
            raise FileFormatError(f"Missing column {e} on line {line_num}") from e
