"""Import orchestrator.

Coordinates CSV parsing, validation, and persistence.  Wraps unexpected
exceptions in the project's domain exception hierarchy so that the CLI
(and any other caller) always receives a predictable error type.
"""

import logging
from pathlib import Path
from typing import List

from .exceptions import ImporterError, InvalidUserDataError
from .models import User
from .parser import CSVParser
from .repository import UserRepository
from .validator import UserValidator

logger = logging.getLogger(__name__)


class Importer:
    """Orchestrates the data import process."""

    def __init__(
        self,
        csv_path: Path,
        db_path: Path,
        validator: UserValidator | None = None,
        repository: UserRepository | None = None,
    ):
        """Initialise the importer with paths and optional collaborators.

        Args:
            csv_path: Path to the source CSV file.
            db_path: Path to the destination JSON database file.
            validator: Optional custom validator; defaults to UserValidator().
            repository: Optional custom repository; defaults to UserRepository(db_path).
        """
        self.csv_path = csv_path
        self.db_path = db_path
        self.validator = validator or UserValidator()
        self.repository = repository or UserRepository(db_path)

    def run(self) -> List[User]:
        """Run the import process and return successfully imported users.

        Iterates over every row produced by the parser, validates each
        user, and persists valid records.  Validation failures are
        logged and re-raised so the caller can decide how to proceed.

        Returns:
            A list of User objects that were successfully imported.

        Raises:
            InvalidUserDataError: If any row fails validation.
            ImporterError: If an unexpected error occurs during import.
        """
        parser = CSVParser(self.csv_path)
        imported: List[User] = []

        for user in parser.parse():
            try:
                result = self.validator.validate(user)
                if not result.is_valid:
                    logger.warning(
                        "Validation failed for %s: %s", user.user_id, result.errors
                    )
                    raise InvalidUserDataError(f"Validation failed: {result.errors}")

                self.repository.add_user(user)
                imported.append(user)
                logger.info("Imported user: %s", user.user_id)
            except ImporterError:
                raise
            except Exception as e:
                logger.error("Unexpected error importing %s: %s", user.user_id, e)
                raise ImporterError(str(e)) from e

        return imported
