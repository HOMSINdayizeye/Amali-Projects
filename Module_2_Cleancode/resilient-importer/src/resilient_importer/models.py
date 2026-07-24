"""Data models for the resilient importer.

Uses Python dataclasses to provide structured, typed representations
of domain objects passed between parser, validator, and repository.
"""

from dataclasses import dataclass


@dataclass
class User:
    """Represents a single user record imported from CSV."""

    user_id: str
    name: str
    email: str
