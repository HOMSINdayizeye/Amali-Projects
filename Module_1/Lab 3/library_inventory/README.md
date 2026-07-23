# Lab 3 — Inventory Management: Library Inventory System

A small object-oriented **inventory management** application for a library, written in Python. It tracks authors, books (including e‑books and audio books), and borrowers, supports searching/filtering the catalogue, lends and returns copies, and persists everything to a JSON file.

> Module 1 · Lab 3. Focus: OOP (classes, inheritance, encapsulation), file I/O (JSON), and comprehensions.

---

## Features

- **Inventory of resources** — physical books plus `EBook` and `AudioBook` subclasses (inheritance via a `LibraryResource` base class).
- **Copy tracking** — each book tracks `copies_total` / `copies_available`; encapsulated so availability can never exceed stock.
- **Author & borrower management** — fully encapsulated value objects with id-based equality/hashing.
- **Search & filter** — by title, author name, genre, and/or availability (list comprehensions).
- **Borrow / return** — lends a copy, records the borrower, and keeps a borrowing history with borrowed/returned dates.
- **Reports** — available books, borrowed books, books grouped by author, and active loans.
- **JSON persistence** — all data is loaded from and saved to `data/library.json` automatically.
- **Interactive CLI** — menu-driven terminal app, plus reusable module-level functions and a pytest suite.

---

## Project Structure

```
library_inventory/
├── main.py              # CLI entry point (menu loop, seeding)
├── library.py           # Library manager: collections, JSON load/save, operations
├── book.py              # Book, EBook, AudioBook + LibraryResource (ABC)
├── author.py            # Author value object
├── borrower.py          # Borrower value object
├── utils.py             # Reusable functions: add_book, search_books, borrow_book, return_book + reporting helpers
├── data/
│   └── library.json     # Persisted state (created/updated automatically)
└── tests/
    └── test_library.py  # pytest suite
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (uses `from __future__ import annotations` and `list[...]` type hints).

### Run the application

From the `library_inventory/` directory:

```bash
python main.py
```

On first run the library is seeded with sample authors, books (incl. an e‑book and an audio book), borrowers, and one pre-recorded loan. Subsequent runs load the saved `data/library.json`.

The menu:

```
1. Add a book
2. Search books
3. Borrow a book
4. Return a book
5. Report: available books
6. Report: borrowed books
7. Report: books by author
8. List authors & borrowers
0. Exit (data is saved automatically)
```

> Note: `do_add_book` in `main.py` currently creates physical `Book` objects. Use the classes in `book.py` (`EBook`, `AudioBook`) directly if you want to add those types.

---

## Running the Tests

The tests use `pytest` and write to a temporary file, so the committed `data/library.json` is never touched.

```bash
pip install pytest
pytest tests/
```

---

## Core API (reusable functions)

These live in `utils.py` and wrap `Library` operations so the CLI and tests share one code path:

| Function | Purpose |
| --- | --- |
| `add_book(library, book)` | Add a `Book` / `EBook` / `AudioBook` to the inventory. |
| `search_books(library, query, author_name, genre, available_only)` | Filter the catalogue by title/author/genre/availability. |
| `borrow_book(library, book_id, borrower_id)` | Lend a copy (raises if unavailable). |
| `return_book(library, book_id, borrower_id)` | Return a copy (raises if not held). |

Reporting helpers: `report_available_books`, `report_borrowed_books`, `report_books_by_author`, `report_active_loans`.

### Example

```python
from library import Library
from book import EBook
from author import Author
import utils

lib = Library()
author = Author("A1", "Douglas Adams", "British", 1952)
lib.add_author(author)
utils.add_book(lib, EBook("B1", "Dirk Gently", author, 1987, "Sci-Fi", "EPUB", 1.5, 2))
lib.register_borrower(Borrower("U1", "Alice", "alice@example.com"))
utils.borrow_book(lib, "B1", "U1")
lib.save()
```

---

## How It Works

- **Inheritance** — `Book` extends the abstract `LibraryResource`; `EBook` and `AudioBook` extend `Book` and reuse its constructor via `super()`, adding type-specific fields and `to_dict()` overrides. A factory `book_from_dict()` rebuilds the correct subclass on load.
- **Encapsulation** — attributes are private; access goes through properties. `Book.copies_total`/`copies_available` setters keep availability valid; `Borrower.borrowed_book_ids` returns a copy to prevent external mutation.
- **Persistence** — `Library.save()` writes authors, books, borrowers, and borrowing history to JSON; `Library.load()` rebuilds objects (authors first, since books reference them by id).
- **Comprehensions** — searching, filtering, and the by-author report are all implemented with list/dict comprehensions.

---

## Data Model (`data/library.json`)

```json
{
  "authors":   [ { "author_id", "name", "nationality", "birth_year" } ],
  "books":     [ { "kind", "book_id", "title", "author_id", "year",
                   "genre", "copies_total", "copies_available", ... } ],
  "borrowers": [ { "borrower_id", "name", "email", "phone",
                   "borrowed_book_ids": [] } ],
  "borrowings":[ { "borrower_id", "book_id", "borrowed_on", "returned_on" } ]
}
```

`kind` is `"book"`, `"ebook"`, or `"audiobook"` and drives deserialisation back to the right class.
