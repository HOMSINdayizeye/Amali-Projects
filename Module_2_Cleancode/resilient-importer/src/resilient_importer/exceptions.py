"""Custom exception hierarchy for the resilient importer.

All importer-specific errors inherit from ImporterError so that
callers can catch the base class when they want to handle any
import-related failure uniformly.
"""


class ImporterError(Exception):
    """Base exception for importer errors."""

    pass


class FileFormatError(ImporterError):
    """Raised when a file format is invalid or malformed."""

    pass


class DuplicateUserError(ImporterError):
    """Raised when a duplicate user entry is detected."""

    pass


class InvalidUserDataError(ImporterError):
    """Raised when user data fails validation."""

    pass
