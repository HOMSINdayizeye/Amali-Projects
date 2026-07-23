# TDD-Based Weather API Service Stub

A mock Weather API service built with rigorous Test-Driven Development (TDD), pytest, and clean architecture adhering to SOLID principles.

## Project Structure

```
PDD_API_stub/
├── src/
│   └── weather/
│       ├── __init__.py
│       ├── service.py        # WeatherService with dependency injection
│       ├── provider.py       # Abstract WeatherProvider interface
│       ├── models.py         # Dataclasses for requests/responses
│       ├── exceptions.py     # Custom exception hierarchy
│       └── logging_config.py # Structured logging setup
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures and MockProvider
│   └── test_service.py       # Comprehensive test suite
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Architecture

The project follows SOLID principles:

- **Single Responsibility**: Each module has a distinct purpose (service orchestration, data modeling, provider abstraction, logging, exceptions).
- **Open/Closed**: New weather providers can be added by implementing `WeatherProvider` without changing `WeatherService`.
- **Liskov Substitution**: `MockProvider` fully implements the `WeatherProvider` interface.
- **Interface Segregation**: `WeatherProvider` exposes a minimal interface focused on forecast retrieval.
- **Dependency Inversion**: `WeatherService` depends on the abstract `WeatherProvider` rather than concrete implementations.

## TDD Methodology

Every feature follows the Red-Green-Refactor cycle:

1. **Red**: Write a failing test defining the expected behavior.
2. **Green**: Write the minimum production code to pass the test.
3. **Refactor**: Improve code structure while keeping all tests green.

## Setup

```bash
pip install -r requirements.txt
pip install pre-commit
pre-commit install
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run only specific test class
pytest tests/test_service.py::TestWeatherServiceForecast

# Run with verbose output
pytest -v
```

## Coverage Target

Near 100% test coverage is enforced via `pytest-cov` and `pyproject.toml` configuration with a minimum of 90% coverage required to pass.

## Dependencies

- **pytest**: Test framework
- **pytest-mock**: Mocking support
- **pytest-cov**: Coverage reporting
- **coverage.py**: Code coverage measurement
- **black**: Code formatting
- **ruff**: Linting
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality

## Git Workflow

This project uses trunk-based development:

1. Create a short-lived feature branch from `main`.
2. Implement changes following TDD.
3. Open a Pull Request for peer review.
4. Merge after review and all checks pass.

Configured quality gates include:
- `pre-commit` hooks for Black, Ruff, and mypy.
- pytest test suite with high coverage enforcement.
