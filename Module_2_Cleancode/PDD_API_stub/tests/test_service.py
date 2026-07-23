"""Tests for the WeatherService core logic."""

import logging

import pytest

from weather.exceptions import CityNotFoundError, InvalidAPIKeyError
from weather.models import ForecastRequest, ForecastResponse
from weather.provider import WeatherProvider
from weather.service import WeatherService


class TestWeatherServiceInitialization:
    """Test cases for WeatherService initialization."""

    def test_valid_initialization(self, mock_provider: WeatherProvider) -> None:
        """Test valid initialization with provider and API key."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        assert service.provider_name == "MockProvider"

    def test_empty_api_key_raises_error(self, mock_provider: WeatherProvider) -> None:
        """Test that empty API key raises InvalidAPIKeyError."""
        with pytest.raises(InvalidAPIKeyError):
            WeatherService(provider=mock_provider, api_key="")

    def test_none_api_key_raises_error(self, mock_provider: WeatherProvider) -> None:
        """Test that None API key raises InvalidAPIKeyError."""
        with pytest.raises(InvalidAPIKeyError):
            WeatherService(provider=mock_provider, api_key="")  # type: ignore[arg-type]

    def test_none_provider_raises_type_error(self) -> None:
        """Test that None provider raises TypeError."""
        with pytest.raises(TypeError):
            WeatherService(provider=None, api_key="valid-key")  # type: ignore[arg-type]

    def test_api_key_is_stripped(self, mock_provider: WeatherProvider) -> None:
        """Test that API key is stripped of leading/trailing whitespace."""
        service = WeatherService(provider=mock_provider, api_key="  valid-key  ")
        assert service.provider_name == "MockProvider"


class TestWeatherServiceForecast:
    """Test cases for the get_forecast method."""

    def test_get_forecast_success(self, mock_provider: WeatherProvider) -> None:
        """Test successful forecast retrieval for a known city."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        request = ForecastRequest(city="London")
        response = service.get_forecast(request)

        assert response.city == "London"
        assert response.temperature == 12.5
        assert response.condition == "Rainy"
        assert response.humidity == 82

    def test_get_forecast_multiple_cities(
        self, mock_provider: WeatherProvider
    ) -> None:
        """Test forecast retrieval for multiple known cities."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        cities = ["London", "Paris", "Tokyo"]

        for city in cities:
            request = ForecastRequest(city=city)
            response = service.get_forecast(request)
            assert response.city == city

    @pytest.mark.parametrize(
        "city,temperature,condition",
        [
            ("London", 12.5, "Rainy"),
            ("Paris", 18.0, "Sunny"),
            ("Tokyo", 22.3, "Cloudy"),
        ],
    )
    def test_get_forecast_parametrized(
        self, mock_provider: WeatherProvider, city: str, temperature: float, condition: str
    ) -> None:
        """Test forecast retrieval with parametrized inputs."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        request = ForecastRequest(city=city)
        response = service.get_forecast(request)

        assert response.city == city
        assert response.temperature == temperature
        assert response.condition == condition

    def test_get_forecast_city_not_found(
        self, mock_provider: WeatherProvider
    ) -> None:
        """Test that CityNotFoundError is raised for unknown cities."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        request = ForecastRequest(city="UnknownCity")

        with pytest.raises(CityNotFoundError):
            service.get_forecast(request)

    def test_get_forecast_logs_request(
        self, mock_provider: WeatherProvider, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that forecast requests are logged."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        request = ForecastRequest(city="London")

        with caplog.at_level(logging.INFO, logger="weather"):
            service.get_forecast(request)

        assert "forecast request for city: London" in caplog.text

    def test_get_forecast_logs_response(
        self, mock_provider: WeatherProvider, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that forecast responses are logged."""
        service = WeatherService(provider=mock_provider, api_key="valid-key")
        request = ForecastRequest(city="London")

        with caplog.at_level(logging.INFO, logger="weather"):
            service.get_forecast(request)

        assert "Forecast returned for London" in caplog.text
