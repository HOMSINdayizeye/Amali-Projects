"""Dataclasses for Weather API request and response models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastRequest:
    """Request model for weather forecast queries."""

    city: str


@dataclass(frozen=True)
class ForecastResponse:
    """Response model for weather forecast data."""

    city: str
    temperature: float
    condition: str
    humidity: int
