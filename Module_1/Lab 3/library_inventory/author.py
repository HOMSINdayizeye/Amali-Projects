"""Author domain model.

A simple, fully-encapsulated value object representing a book author.
Equality and hashing are based on the stable ``author_id`` primary key so
authors can be stored in dictionaries and sets safely.
"""

from __future__ import annotations

from typing import Optional


class Author:
    """Represents an author tracked by the library.

    Attributes are private and exposed through read/write properties so the
    internal state can be validated/normalised on assignment.
    """

    def __init__(
        self,
        author_id: str,
        name: str,
        nationality: str = "Unknown",
        birth_year: Optional[int] = None,
    ) -> None:
        # Primary key: stored uppercased so lookups are case-insensitive.
        self._author_id = author_id.strip().upper()
        self._name = name.strip()
        self._nationality = nationality.strip()
        # birth_year may be unknown for historical authors.
        self._birth_year = birth_year

    # ------------------------------------------------------------------
    # Properties (encapsulation: getters / setters)
    # ------------------------------------------------------------------
    @property
    def author_id(self) -> str:
        """Read-only stable identifier for the author."""
        return self._author_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.strip()

    @property
    def nationality(self) -> str:
        return self._nationality

    @nationality.setter
    def nationality(self, value: str) -> None:
        self._nationality = value.strip()

    @property
    def birth_year(self) -> Optional[int]:
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value: Optional[int]) -> None:
        if value is not None and value <= 0:
            raise ValueError("birth_year must be a positive year.")
        self._birth_year = value

    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        """Unambiguous, developer-friendly representation."""
        return (
            f"Author(id={self._author_id!r}, name={self._name!r}, "
            f"nationality={self._nationality!r})"
        )

    def __str__(self) -> str:
        """Human-friendly display string."""
        return self._name

    def __eq__(self, other: object) -> bool:
        """Two authors are equal when they share the same id."""
        if not isinstance(other, Author):
            return NotImplemented
        return self._author_id == other._author_id

    def __hash__(self) -> int:
        """Allow authors to be used in sets / as dict keys."""
        return hash(self._author_id)

    # ------------------------------------------------------------------
    # (De)serialisation for JSON persistence
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Convert to a plain dict suitable for JSON storage."""
        return {
            "author_id": self._author_id,
            "name": self._name,
            "nationality": self._nationality,
            "birth_year": self._birth_year,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Author":
        """Rebuild an Author from a dict produced by :meth:`to_dict`."""
        return cls(
            author_id=data["author_id"],
            name=data["name"],
            nationality=data.get("nationality", "Unknown"),
            birth_year=data.get("birth_year"),
        )
