"""Library Inventory Application - command line interface.

Run this module to launch an interactive CLI that lets you add books, search
and filter the inventory, borrow/return items, and print reports. All data is
persisted to ``data/library.json`` automatically.

Example:
    python main.py
"""

from __future__ import annotations

from book import Book, EBook, AudioBook
from author import Author
from borrower import Borrower
from library import Library
import utils


def seed_if_empty(library: Library) -> None:
    """Populate a small starter dataset the first time the app runs."""
    if library.all_authors() or library.all_books():
        return  # Data already exists; do not overwrite.

    # --- Authors ---
    adams = Author("A1", "Douglas Adams", "British", 1952)
    tolkien = Author("A2", "J.R.R. Tolkien", "British", 1892)
    rowling = Author("A3", "J.K. Rowling", "British", 1965)
    for author in (adams, tolkien, rowling):
        library.add_author(author)

    # --- Books (incl. EBook and AudioBook subclasses) ---
    library.add_book(Book("B1", "The Hitchhiker's Guide to the Galaxy",
                          adams, 1979, "Sci-Fi", copies_total=3))
    library.add_book(Book("B2", "The Lord of the Rings", tolkien, 1954,
                          "Fantasy", copies_total=2))
    library.add_book(EBook("B3", "Harry Potter and the Philosopher's Stone",
                           rowling, 1997, "Fantasy", file_format="EPUB",
                           file_size_mb=2.4, copies_total=5))
    library.add_book(AudioBook("B4", "The Hobbit", tolkien, 1937, "Fantasy",
                               narrator="Rob Inglis", duration_minutes=660,
                               copies_total=1))

    # --- Borrowers ---
    library.register_borrower(Borrower("U1", "Alice Mensah",
                                       "alice@example.com", "0201234567"))
    library.register_borrower(Borrower("U2", "Kwame Owusu",
                                       "kwame@example.com"))

    # Pre-record one loan so reports have something to show.
    library.borrow_book("B2", "U1")
    library.save()


def show_menu() -> None:
    """Print the main menu options."""
    print("\n" + "-" * 70)
    print("LIBRARY INVENTORY  -  MAIN MENU")
    print("-" * 70)
    print("1. Add a book")
    print("2. Search books")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Report: available books")
    print("6. Report: borrowed books")
    print("7. Report: books by author")
    print("8. List authors & borrowers")
    print("0. Exit (data is saved automatically)")
    print("-" * 70)


def do_add_book(library: Library) -> None:
    """Prompt the user and add a (physical) book to the inventory."""
    book_id = input("Book ID (e.g. B5): ").strip().upper()
    if not book_id:
        print("Book ID is required.")
        return
    title = input("Title: ").strip()
    author_id = input("Author ID (must already exist): ").strip().upper()
    try:
        author = library.get_author(author_id)
    except KeyError:
        print(f"No author '{author_id}'. Add the author first.")
        return
    try:
        year = int(input("Publication year: ").strip())
        copies = int(input("Number of copies: ").strip() or "1")
    except ValueError:
        print("Year and copies must be whole numbers.")
        return
    genre = input("Genre: ").strip() or "General"

    book = Book(book_id, title, author, year, genre, copies_total=copies)
    library.add_book(book)
    library.save()
    print(f"Added: {book}")


def do_search(library: Library) -> None:
    """Prompt for filters and print matching books."""
    query = input("Title contains (blank = any): ").strip() or None
    author_name = input("Author name contains (blank = any): ").strip() or None
    genre = input("Genre (blank = any): ").strip() or None
    avail = input("Available only? (y/N): ").strip().lower() == "y"

    results = utils.search_books(
        library, query=query, author_name=author_name,
        genre=genre, available_only=avail,
    )
    if not results:
        print("No books matched your search.")
        return
    print(f"\nFound {len(results)} book(s):")
    for book in results:
        print(f"  {book}")


def do_borrow(library: Library) -> None:
    book_id = input("Book ID to borrow: ").strip().upper()
    borrower_id = input("Your borrower ID: ").strip().upper()
    try:
        utils.borrow_book(library, book_id, borrower_id)
    except (KeyError, ValueError, RuntimeError) as exc:
        print(f"Cannot borrow: {exc}")
        return
    library.save()
    print(f"Borrowed {book_id} for {borrower_id}.")


def do_return(library: Library) -> None:
    book_id = input("Book ID to return: ").strip().upper()
    borrower_id = input("Your borrower ID: ").strip().upper()
    try:
        utils.return_book(library, book_id, borrower_id)
    except (KeyError, ValueError, RuntimeError) as exc:
        print(f"Cannot return: {exc}")
        return
    library.save()
    print(f"Returned {book_id} from {borrower_id}.")


def do_report_available(library: Library) -> None:
    utils.section("AVAILABLE BOOKS")
    books = utils.report_available_books(library)
    if not books:
        print("No books are currently available.")
        return
    print(utils.format_book_row.__doc__ or "")
    for book in books:
        print(utils.format_book_row(book))


def do_report_borrowed(library: Library) -> None:
    utils.section("BORROWED BOOKS (copies currently out)")
    books = utils.report_borrowed_books(library)
    if not books:
        print("Nothing is currently borrowed.")
        return
    for book in books:
        print(f"  {book}")


def do_report_by_author(library: Library) -> None:
    utils.section("BOOKS BY AUTHOR")
    for name, count in utils.report_books_by_author(library).items():
        print(f"  {name}: {count} book(s)")


def do_list_people(library: Library) -> None:
    utils.section("AUTHORS")
    for author in library.all_authors():
        print(f"  {author}")
    utils.section("BORROWERS")
    for borrower in library.all_borrowers():
        print(f"  {borrower}  [loans: {borrower.borrowed_book_ids}]")


def main() -> None:
    """Entry point: seed data (if needed) and run the CLI loop."""
    library = Library()
    seed_if_empty(library)

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                do_add_book(library)
            elif choice == "2":
                do_search(library)
            elif choice == "3":
                do_borrow(library)
            elif choice == "4":
                do_return(library)
            elif choice == "5":
                do_report_available(library)
            elif choice == "6":
                do_report_borrowed(library)
            elif choice == "7":
                do_report_by_author(library)
            elif choice == "8":
                do_list_people(library)
            elif choice == "0":
                library.save()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as exc:  # noqa: BLE001 - keep the CLI alive
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
