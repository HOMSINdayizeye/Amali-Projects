"""Abstract base provider interface for weather data sources."""

from abc import ABC, abstractmethod

from .models import ForecastResponse


class WeatherProvider(ABC):
    """Interface for weather data providers.

    Implementations of this abstract class provide weather data
    from various sources (mock, real APIs, databases, etc.).
    """

    @abstractmethod
    def get_forecast(self, city: str) -> ForecastResponse:
        """Retrieve forecast data for a specific city.

        Args:
            city: Name of the city to retrieve forecast for.

        Returns:
            ForecastResponse containing weather data for the city.

        Raises:
            CityNotFoundError: If the city is not available in the provider.
        """
