# Resilient Data Importer CLI

A command-line tool that reliably imports user data from a CSV file into a simulated JSON database.

## Features

- CSV parsing with validation
- Custom exception hierarchy
- Structured logging
- Repository pattern for storage
- Type hints and dataclasses

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

## Usage

```powershell
python -m resilient_importer.cli users.csv
```

## Testing

```powershell
pytest
coverage run -m pytest
coverage report
```
