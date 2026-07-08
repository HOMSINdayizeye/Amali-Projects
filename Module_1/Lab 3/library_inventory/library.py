"""Library manager: in-memory store, JSON persistence and operations.

The :class:`Library` class owns the three core collections (authors, books,
borrowers) as dictionaries keyed by id, plus a borrowing history list. It
handles loading/saving to JSON and exposes the high-level operations used by
the CLI layer in ``main.py`` and the reusable helpers in ``utils.py``.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from author import Author
from book import Book, EBook, AudioBook, book_from_dict
from borrower import Borrower


# Default location of the JSON data file, relative to this module.
DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "library.json"


class Library:
    """Manages library resources and persists them to a JSON file."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH) -> None:
        self._data_path = Path(data_path)
        # Dictionaries map ids -> objects for O(1) lookups.
        self._authors: dict[str, Author] = {}
        self._books: dict[str, Book] = {}
        self._borrowers: dict[str, Borrower] = {}
        # Borrowing history: list of {borrower_id, book_id, borrowed_on, returned_on}.
        self._borrowings: list[dict] = []
        self.load()

    # ==================================================================
    # Persistence (file I/O)
    # ==================================================================
    def load(self) -> None:
        """Load all data from the JSON file, if it exists."""
        if not self._data_path.exists():
            return  # Fresh library: start empty.

        with self._data_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        # Rebuild authors first (books reference them by id).
        self._authors = {
            a["author_id"]: Author.from_dict(a) for a in data.get("authors", [])
        }
        authors_by_id = self._authors
        self._books = {
            b["book_id"]: book_from_dict(b, authors_by_id)
            for b in data.get("books", [])
        }
        self._borrowers = {
            br["borrower_id"]: Borrower.from_dict(br)
            for br in data.get("borrowers", [])
        }
        self._borrowings = data.get("borrowings", [])

    def save(self) -> None:
        """Persist all current data to the JSON file."""
        # Ensure the parent directory exists (e.g. first run).
        self._data_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "authors": [a.to_dict() for a in self._authors.values()],
            "books": [b.to_dict() for b in self._books.values()],
            "borrowers": [br.to_dict() for br in self._borrowers.values()],
            "borrowings": self._borrowings,
        }
        with self._data_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, default=str)

    # ==================================================================
    # Registration / add
    # ==================================================================
    def add_author(self, author: Author) -> None:
        if author.author_id in self._authors:
            raise ValueError(f"Author {author.author_id} already exists.")
        self._authors[author.author_id] = author

    def add_book(self, book: Book) -> None:
        """Add a book (or EBook/AudioBook) to the inventory."""
        if book.resource_id in self._books:
            raise ValueError(f"Book {book.resource_id} already exists.")
        self._books[book.resource_id] = book

    def register_borrower(self, borrower: Borrower) -> None:
        if borrower.borrower_id in self._borrowers:
            raise ValueError(f"Borrower {borrower.borrower_id} already exists.")
        self._borrowers[borrower.borrower_id] = borrower

    # ==================================================================
    # Lookups
    # ==================================================================
    def get_author(self, author_id: str) -> Author:
        aid = author_id.strip().upper()
        if aid not in self._authors:
            raise KeyError(f"No author with id {aid}.")
        return self._authors[aid]

    def get_book(self, book_id: str) -> Book:
        bid = book_id.strip().upper()
        if bid not in self._books:
            raise KeyError(f"No book with id {bid}.")
        return self._books[bid]

    def get_borrower(self, borrower_id: str) -> Borrower:
        bid = borrower_id.strip().upper()
        if bid not in self._borrowers:
            raise KeyError(f"No borrower with id {bid}.")
        return self._borrowers[bid]

    # ==================================================================
    # Search & filtering (comprehensions)
    # ==================================================================
    def search_books(
        self,
        query: Optional[str] = None,
        author_name: Optional[str] = None,
        genre: Optional[str] = None,
        available_only: bool = False,
    ) -> list[Book]:
        """Search the inventory using one or more optional filters.

        Uses a list comprehension to build the result set efficiently.
        """
        q = query.strip().lower() if query else None
        a = author_name.strip().lower() if author_name else None
        g = genre.strip().lower() if genre else None

        matches = [
            book
            for book in self._books.values()
            if (q is None or q in book.title.lower())
            and (a is None or a in book.author.name.lower())
            and (g is None or g == book.genre.lower())
            and (not available_only or book.is_available)
        ]
        return matches

    def books_by_author(self, author: Author) -> list[Book]:
        """All books written by the given author (dict comprehension result)."""
        return [b for b in self._books.values() if b.author == author]

    def available_books(self) -> list[Book]:
        """Books with at least one copy on the shelf."""
        return [b for b in self._books.values() if b.is_available]

    def borrowed_books(self) -> list[Book]:
        """Books that have at least one copy currently out on loan."""
        return [b for b in self._books.values() if b.copies_available < b.copies_total]

    # ==================================================================
    # Borrow / return operations
    # ==================================================================
    def borrow_book(self, book_id: str, borrower_id: str) -> None:
        """Lend a book to a borrower and record the transaction."""
        book = self.get_book(book_id)
        borrower = self.get_borrower(borrower_id)

        book.borrow_copy()          # raises if unavailable
        borrower.borrow(book.resource_id)
        self._borrowings.append(
            {
                "borrower_id": borrower.borrower_id,
                "book_id": book.resource_id,
                "borrowed_on": date.today().isoformat(),
                "returned_on": None,
            }
        )

    def return_book(self, book_id: str, borrower_id: str) -> None:
        """Return a borrowed book and close the open transaction."""
        book = self.get_book(book_id)
        borrower = self.get_borrower(borrower_id)

        borrower.return_book(book.resource_id)  # raises if not held
        book.return_copy()

        # Close the most recent open loan for this book+borrower.
        for record in reversed(self._borrowings):
            if (
                record["book_id"] == book.resource_id
                and record["borrower_id"] == borrower.borrower_id
                and record["returned_on"] is None
            ):
                record["returned_on"] = date.today().isoformat()
                break

    # ==================================================================
    # Reporting (comprehensions + grouping)
    # ==================================================================
    def report_by_author(self) -> dict[str, int]:
        """Return a dict mapping each author name to their book count."""
        return {
            author.name: len(self.books_by_author(author))
            for author in self._authors.values()
        }

    def all_authors(self) -> list[Author]:
        return list(self._authors.values())

    def all_books(self) -> list[Book]:
        return list(self._books.values())

    def all_borrowers(self) -> list[Borrower]:
        return list(self._borrowers.values())

    def borrowing_history(self) -> list[dict]:
        return list(self._borrowings)
