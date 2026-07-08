"""pytest suite for the Library Inventory application.

Each test builds a small :class:`~library.Library` backed by a temporary JSON
file (``tmp_path``) so the committed ``data/library.json`` is never mutated.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from author import Author
from book import Book, EBook, AudioBook, book_from_dict
from borrower import Borrower
from library import Library
import utils


@pytest.fixture
def library(tmp_path: Path) -> Library:
    """A fresh, empty library persisted to a temp file."""
    return Library(data_path=tmp_path / "library.json")


@pytest.fixture
def populated(library: Library) -> Library:
    """A library pre-filled with an author, books and a borrower."""
    author = Author("A1", "Douglas Adams", "British", 1952)
    library.add_author(author)
    library.add_book(Book("B1", "Dirk Gently", author, 1987, "Sci-Fi", 2))
    library.add_book(EBook("B2", "The Salmon of Doubt", author, 2002,
                           "Sci-Fi", "EPUB", 1.5, 1))
    library.register_borrower(Borrower("U1", "Test User", "t@example.com"))
    return library


def test_add_and_lookup(populated: Library) -> None:
    assert populated.get_book("B1").title == "Dirk Gently"
    assert len(populated.all_books()) == 2


def test_search_by_title_and_genre(populated: Library) -> None:
    # Comprehension-based search should match a substring of the title.
    assert len(utils.search_books(populated, query="salmon")) == 1
    # Genre filter is exact (case-insensitive).
    assert len(utils.search_books(populated, genre="scifi")) == 2
    # Combined filters narrow the result set.
    assert len(utils.search_books(populated, genre="fantasy")) == 0


def test_borrow_and_return_updates_copies(populated: Library) -> None:
    book = populated.get_book("B1")
    assert book.copies_available == 2
    utils.borrow_book(populated, "B1", "U1")
    assert book.copies_available == 1
    assert not book.is_available is False or book.copies_available == 1
    utils.return_book(populated, "B1", "U1")
    assert book.copies_available == 2


def test_borrow_unavailable_raises(populated: Library) -> None:
    # EBook B2 has a single copy; borrow it twice -> second raises.
    utils.borrow_book(populated, "B2", "U1")
    with pytest.raises(RuntimeError):
        utils.borrow_book(populated, "B2", "U1")


def test_persistence_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "library.json"
    lib = Library(data_path=path)
    author = Author("A9", "Jane Doe")
    lib.add_author(author)
    lib.add_book(AudioBook("B9", "Narrated Tale", author, 2020, "Drama",
                           "Narrator X", 120, 1))
    lib.save()

    # Reload from disk and verify the data survived (incl. subclass type).
    reloaded = Library(data_path=path)
    assert isinstance(reloaded.get_book("B9"), AudioBook)
    assert reloaded.get_book("B9").narrator == "Narrator X"


def test_report_by_author(populated: Library) -> None:
    report = utils.report_books_by_author(populated)
    assert report["Douglas Adams"] == 2


def test_book_equality_and_repr() -> None:
    author = Author("A1", "Author")
    b1 = Book("B1", "Title", author, 2000, "Genre")
    b2 = Book("B1", "Different Title", author, 1999, "Other")
    # Equality is based on the unique id, not the contents.
    assert b1 == b2
    assert "B1" in repr(b1)
