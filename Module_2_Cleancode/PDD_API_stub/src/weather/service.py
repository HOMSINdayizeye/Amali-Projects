"""Core weather service using dependency injection and abstract providers."""

from .exceptions import CityNotFoundError, InvalidAPIKeyError
from .logging_config import logger
from .models import ForecastRequest, ForecastResponse
from .provider import WeatherProvider


class WeatherService:
    """Service for retrieving weather forecasts from a configurable provider.

    Dependency: Depends on the abstract WeatherProvider interface, not a
    concrete implementation, adhering to the Dependency Inversion Principle.
    """

    def __init__(self, provider: WeatherProvider, api_key: str) -> None:
        """Initialize the weather service.

        Args:
            provider: A concrete implementation of WeatherProvider.
            api_key: API key for authenticating with the provider.

        Raises:
            InvalidAPIKeyError: If api_key is empty or None.
            TypeError: If provider is not a WeatherProvider instance.
        """
        if not api_key or not api_key.strip():
            raise InvalidAPIKeyError("API key must not be empty.")

        if provider is None:
            raise TypeError("Provider must not be None.")

        self._provider = provider
        self._api_key = api_key.strip()

    def get_forecast(self, request: ForecastRequest) -> ForecastResponse:
        """Retrieve a weather forecast for the specified city.

        Args:
            request: ForecastRequest containing the target city.

        Returns:
            ForecastResponse with weather data for the city.

        Raises:
            CityNotFoundError: If the city is not available from the provider.
        """
        logger.info("Received forecast request for city: %s", request.city)

        response = self._provider.get_forecast(request.city)

        logger.info(
            "Forecast returned for %s: %s, %.1f°C",
            response.city,
            response.condition,
            response.temperature,
        )
        return response

    @property
    def provider_name(self) -> str:
        """Return the name of the configured provider class."""
        return type(self._provider).__name__
