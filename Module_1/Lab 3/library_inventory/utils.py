"""Utility helpers for the Library Inventory application.

This module provides the reusable, module-level functions called for in the
lab brief:

* :func:`add_book`
* :func:`search_books`
* :func:`borrow_book`
* :func:`return_book`

Each wraps the corresponding operation on a :class:`~library.Library`
instance, so the CLI and tests can call them directly. It also contains
small presentation/reporting helpers built with comprehensions.
"""

from __future__ import annotations

from typing import Optional

from book import Book
from library import Library


# ======================================================================
# Core reusable functions
# ======================================================================
def add_book(library: Library, book: Book) -> None:
    """Add a book (or EBook/AudioBook) to the library inventory."""
    library.add_book(book)


def search_books(
    library: Library,
    query: Optional[str] = None,
    author_name: Optional[str] = None,
    genre: Optional[str] = None,
    available_only: bool = False,
) -> list[Book]:
    """Search the inventory by book id or title, author, genre and/or availability.

    The ``query`` matches against either the book's id or its title.
    """
    return library.search_books(
        query=query,
        author_name=author_name,
        genre=genre,
        available_only=available_only,
    )


def borrow_book(library: Library, book_id: str, borrower_id: str) -> None:
    """Borrow ``book_id`` on behalf of ``borrower_id``."""
    library.borrow_book(book_id, borrower_id)


def return_book(library: Library, book_id: str, borrower_id: str) -> None:
    """Return ``book_id`` on behalf of ``borrower_id``."""
    library.return_book(book_id, borrower_id)


# ======================================================================
# Reporting helpers (comprehensions for filtering/categorising)
# ======================================================================
def report_available_books(library: Library) -> list[Book]:
    """List every book that currently has copies on the shelf."""
    return library.available_books()


def report_borrowed_books(library: Library) -> list[Book]:
    """List every book that is fully checked out."""
    return library.borrowed_books()


def report_books_by_author(library: Library) -> dict[str, int]:
    """Return a dict of author name -> number of books authored."""
    return library.report_by_author()


def report_active_loans(library: Library) -> list[dict]:
    """Return all borrowing records that have not yet been returned."""
    # Dict comprehension over the history keeps only open loans.
    return [r for r in library.borrowing_history() if r["returned_on"] is None] 

# ======================================================================
# Small presentation helpers
# ======================================================================
def format_book_row(book: Book) -> str:
    """Render one book as a compact table row string."""
    return (
        f"{book.resource_id:<8} | {book.title:<30} | "
        f"{book.author.name:<20} | {book.genre:<12} | "
        f"{book.copies_available}/{book.copies_total}"
    )


def section(title: str) -> None:
    """Print a titled section header for the CLI reports."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
