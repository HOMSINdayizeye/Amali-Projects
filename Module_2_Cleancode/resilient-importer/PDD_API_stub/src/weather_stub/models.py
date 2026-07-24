"""Data models for weather responses."""

from dataclasses import dataclass


@dataclass
class Forecast:
    """Represents a weather forecast for a city."""
    city: str
    temperature_celsius: float
    condition: str
