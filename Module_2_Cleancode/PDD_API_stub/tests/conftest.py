"""Pytest configuration and shared fixtures for weather service tests."""

import pytest

from weather.exceptions import CityNotFoundError
from weather.models import ForecastResponse
from weather.provider import WeatherProvider


class MockProvider(WeatherProvider):
    """Concrete mock provider for testing purposes."""

    def __init__(self, data: dict[str, ForecastResponse]) -> None:
        """Initialize the mock provider with predefined data.

        Args:
            data: Mapping of city names to their ForecastResponse data.
        """
        self._data = data

    def get_forecast(self, city: str) -> ForecastResponse:
        """Return mock forecast data for the given city.

        Args:
            city: Name of the city to retrieve forecast for.

        Returns:
            ForecastResponse for the city.

        Raises:
            CityNotFoundError: If the city is not in the predefined data.
        """
        if city not in self._data:
            raise CityNotFoundError(f"City '{city}' not found in provider data.")
        return self._data[city]


@pytest.fixture
def mock_provider() -> MockProvider:
    """Return a MockProvider with sample forecast data."""
    data = {
        "London": ForecastResponse(
            city="London", temperature=12.5, condition="Rainy", humidity=82
        ),
        "Paris": ForecastResponse(
            city="Paris", temperature=18.0, condition="Sunny", humidity=45
        ),
        "Tokyo": ForecastResponse(
            city="Tokyo", temperature=22.3, condition="Cloudy", humidity=60
        ),
    }
    return MockProvider(data)
