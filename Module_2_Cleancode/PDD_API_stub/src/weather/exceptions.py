"""Custom exceptions for the Weather API Service."""


class WeatherServiceError(Exception):
    """Base exception for WeatherService errors."""


class InvalidAPIKeyError(WeatherServiceError):
    """Raised when the API key provided is invalid or missing."""


class CityNotFoundError(WeatherServiceError):
    """Raised when the requested city is not found in the provider database."""
