"""Weather service implementation."""

from weather_stub.exceptions import CityNotFoundError
from weather_stub.models import Forecast


class WeatherService:
    """Mock weather service that returns predefined forecasts."""

    def __init__(self):
        self._mock_data = {
            "Nairobi": Forecast(city="Nairobi", temperature_celsius=25.0, condition="Sunny"),
            "Mombasa": Forecast(city="Mombasa", temperature_celsius=30.0, condition="Hot"),
            "Kisumu": Forecast(city="Kisumu", temperature_celsius=22.0, condition="Cloudy"),
        }

    def get_forecast(self, city: str) -> Forecast:
        """Get forecast for a city.

        Args:
            city: Name of the city.

        Returns:
            Forecast object with weather data.

        Raises:
            CityNotFoundError: If city is not in mock database.
        """
        if city not in self._mock_data:
            raise CityNotFoundError(f"City not found: {city}")
        return self._mock_data[city]
