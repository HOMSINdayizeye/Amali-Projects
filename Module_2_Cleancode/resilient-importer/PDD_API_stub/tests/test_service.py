import pytest
from weather_stub.exceptions import CityNotFoundError
from weather_stub.service import WeatherService


class TestWeatherService:
    def test_get_forecast_returns_known_city(self):
        service = WeatherService()
        result = service.get_forecast("Nairobi")
        assert result.city == "Nairobi"
        assert result.temperature_celsius == 25.0
        assert result.condition == "Sunny"
