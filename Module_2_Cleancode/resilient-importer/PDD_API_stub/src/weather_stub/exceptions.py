"""Custom exceptions for the weather service."""


class CityNotFoundError(Exception):
    """Raised when a city is not found in the mock database."""
    pass


class InvalidAPIKeyError(Exception):
    """Raised when an invalid API key is provided."""
    pass
