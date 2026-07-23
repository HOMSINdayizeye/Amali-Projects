"""Book domain model and the ``Book`` class hierarchy.

This module defines:

* :class:`LibraryResource` -- the abstract base class (ABC) that defines the
  common contract for everything the library can track.
* :class:`Book` -- the base (physical) book with copy-count management.
* :class:`EBook` -- a digital book (adds file format + size).
* :class:`AudioBook` -- an audio book (adds narrator + duration).

``EBook`` and ``AudioBook`` demonstrate inheritance and reuse of parent
behaviour via ``super()``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from author import Author


class LibraryResource(ABC):
    """Abstract base class for any resource the library manages.

    Establishes a shared identity (``resource_id``) and a common interface
    (:meth:`resource_type`) so heterogeneous resources can live in the same
    inventory and be treated polymorphically.
    """

    def __init__(self, resource_id: str) -> None:
        # Private attribute accessed only through the ``resource_id`` property.
        self._resource_id = resource_id.strip().upper()

    @property
    def resource_id(self) -> str:
        """Read-only stable identifier for this resource."""
        return self._resource_id

    @property
    @abstractmethod
    def resource_type(self) -> str:
        """Human readable type label, e.g. 'Book' or 'EBook'."""
        raise NotImplementedError

    def __repr__(self) -> str:
        # Safe default; subclasses provide richer representations.
        return f"{type(self).__name__}(id={self._resource_id!r})"


class Book(LibraryResource):
    """A book in the library inventory.

    Copy counts are encapsulated: ``copies_available`` can never exceed
    ``copies_total`` because it is recomputed through the setter.
    """

    def __init__(
        self,
        book_id: str,
        title: str,
        author: Author,
        year: int,
        genre: str,
        copies_total: int = 1,
    ) -> None:
        # Call the ABC initialiser to set the shared resource id.
        super().__init__(book_id)
        self._title = title.strip()
        self._author = author
        self._year = year
        self._genre = genre.strip()
        # ``copies_total`` is the source of truth; ``copies_available`` starts
        # equal to it (a brand new book has all copies on the shelf).
        self._copies_total = self._normalize_copies(copies_total)
        self._copies_available = self._copies_total

    @staticmethod
    def _normalize_copies(value: int) -> int:
        """Clamp copy counts to a non-negative integer."""
        return max(0, int(value))

    # ------------------------------------------------------------------
    # Properties (encapsulation)
    # ------------------------------------------------------------------
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value.strip()

    @property
    def author(self) -> Author:
        return self._author

    @property
    def year(self) -> int:
        return self._year

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def copies_total(self) -> int:
        return self._copies_total

    @copies_total.setter
    def copies_total(self, value: int) -> None:
        value = self._normalize_copies(value)
        self._copies_total = value
        # Never keep more available copies than we actually own.
        if self._copies_available > value:
            self._copies_available = value

    @property
    def copies_available(self) -> int:
        return self._copies_available

    @property
    def resource_type(self) -> str:
        return "Book"

    @property
    def is_available(self) -> bool:
        """True when at least one physical copy is on the shelf."""
        return self._copies_available > 0

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------
    def borrow_copy(self) -> None:
        """Lend one available copy.

        Raises:
            RuntimeError: if no copies are currently available.
        """
        if self._copies_available <= 0:
            raise RuntimeError(f"No available copies of '{self._title}'.")
        self._copies_available -= 1

    def return_copy(self) -> None:
        """Return one copy to the shelf.

        Raises:
            RuntimeError: if every copy is already accounted for (i.e. the
            book was not actually borrowed).
        """
        if self._copies_available >= self._copies_total:
            raise RuntimeError(f"All copies of '{self._title}' are already in.")
        self._copies_available += 1

    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Book(id={self.resource_id!r}, title={self._title!r}, "
            f"author={self._author.name!r}, year={self._year}, "
            f"available={self._copies_available}/{self._copies_total})"
        )

    def __str__(self) -> str:
        return (
            f"{self._title} by {self._author.name} ({self._year}) "
            f"[{self.resource_id}]"
        )

    def __eq__(self, other: object) -> bool:
        """Books compare equal by their unique resource id."""
        if not isinstance(other, Book):
            return NotImplemented
        return self.resource_id == other.resource_id

    def __hash__(self) -> int:
        return hash(self.resource_id)

    # ------------------------------------------------------------------
    # (De)serialisation
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """Serialize to a plain dict for JSON storage."""
        return {
            "kind": "book",
            "book_id": self.resource_id,
            "title": self._title,
            "author_id": self._author.author_id,
            "year": self._year,
            "genre": self._genre,
            "copies_total": self._copies_total,
            "copies_available": self._copies_available,
        }


class EBook(Book):
    """A digital book. Extends :class:`Book` with format and file size."""

    def __init__(
        self,
        book_id: str,
        title: str,
        author: Author,
        year: int,
        genre: str,
        file_format: str = "PDF",
        file_size_mb: float = 0.0,
        copies_total: int = 1,
    ) -> None:
        # Reuse the parent constructor for all shared book state.
        super().__init__(book_id, title, author, year, genre, copies_total)
        self.file_format = file_format.upper()
        self.file_size_mb = float(file_size_mb)

    @property
    def resource_type(self) -> str:
        return "EBook"

    def __repr__(self) -> str:
        return (
            f"EBook(id={self.resource_id!r}, title={self.title!r}, "
            f"author={self.author.name!r}, format={self.file_format}, "
            f"size={self.file_size_mb}MB)"
        )

    def to_dict(self) -> dict:
        # Extend the parent serialisation with ebook-specific fields.
        data = super().to_dict()
        data["kind"] = "ebook"
        data["file_format"] = self.file_format
        data["file_size_mb"] = self.file_size_mb
        return data


class AudioBook(Book):
    """An audio book. Extends :class:`Book` with narrator and duration."""

    def __init__(
        self,
        book_id: str,
        title: str,
        author: Author,
        year: int,
        genre: str,
        narrator: str,
        duration_minutes: int,
        copies_total: int = 1,
    ) -> None:
        super().__init__(book_id, title, author, year, genre, copies_total)
        self.narrator = narrator.strip()
        self.duration_minutes = int(duration_minutes)

    @property
    def resource_type(self) -> str:
        return "AudioBook"

    def __repr__(self) -> str:
        return (
            f"AudioBook(id={self.resource_id!r}, title={self.title!r}, "
            f"author={self.author.name!r}, narrator={self.narrator!r}, "
            f"minutes={self.duration_minutes})"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["kind"] = "audiobook"
        data["narrator"] = self.narrator
        data["duration_minutes"] = self.duration_minutes
        return data


def book_from_dict(data: dict, authors_by_id: dict[str, Author]) -> Book:
    """Factory that rebuilds the correct ``Book`` subclass from a dict.

    The concrete type is decided by the stored ``kind`` field, then the
    shared copy state is restored afterwards.
    """
    author = authors_by_id[data["author_id"]]
    kind = data.get("kind", "book")

    if kind == "ebook":
        book: Book = EBook(
            book_id=data["book_id"],
            title=data["title"],
            author=author,
            year=data["year"],
            genre=data["genre"],
            file_format=data.get("file_format", "PDF"),
            file_size_mb=data.get("file_size_mb", 0.0),
            copies_total=data["copies_total"],
        )
    elif kind == "audiobook":
        book = AudioBook(
            book_id=data["book_id"], 
            title=data["title"],
            author=author,
            year=data["year"],
            genre=data["genre"],
            narrator=data.get("narrator", "Unknown"),
            duration_minutes=data.get("duration_minutes", 0),
            copies_total=data["copies_total"],
        )
    else:
        book = Book(
            book_id=data["book_id"],
            title=data["title"],
            author=author,
            year=data["year"],
            genre=data["genre"],
            copies_total=data["copies_total"],
        )

    # Restore the persisted availability (the constructor assumes all in).
    book._copies_available = data.get("copies_available", data["copies_total"])
    return book
