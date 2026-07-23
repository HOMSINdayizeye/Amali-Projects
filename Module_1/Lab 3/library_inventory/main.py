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
    print("1. Add a book (Book / EBook / AudioBook; author auto-created if new)")
    print("2. Search books")
    print("3. Borrow a book (just enter book id + your borrower id)")
    print("4. Return a book (just enter book id + your borrower id)")
    print("5. Report: available books")
    print("6. Report: borrowed books")
    print("7. Report: books by author")
    print("8. List authors & borrowers")
    print("9. List all books")
    print("0. Exit (data is saved automatically)")
    print("-" * 70)


def do_add_book(library: Library) -> None:
    """Prompt the user and add a (physical) book, creating its author if new."""
    book_id = input("Book ID (e.g. B5): ").strip().upper()
    if not book_id:
        print("Book ID is required.")
        return
    title = input("Title: ").strip()

    author_id = input("Author ID (e.g. A1, or new id): ").strip().upper()
    author = library._authors.get(author_id)
    if author is None:
        # Author does not exist yet: create it from the details entered here.
        name = input("New author name: ").strip()
        nationality = input("Author nationality (blank = Unknown): ").strip() or "Unknown"
        birth_year_str = input("Author birth year (blank = unknown): ").strip()
        birth_year = int(birth_year_str) if birth_year_str else None
        author = Author(author_id, name, nationality, birth_year)
        library.add_author(author)
        print(f"Created author: {author}")

    try:
        year = int(input("Publication year: ").strip())
        copies = int(input("Number of copies: ").strip() or "1")
    except ValueError:
        print("Year and copies must be whole numbers.")
        return
    genre = input("Genre: ").strip() or "General"

    kind = input("Type (1=Book, 2=EBook, 3=AudioBook): ").strip()
    if kind == "2":
        file_format = input("File format (e.g. EPUB, PDF): ").strip() or "PDF"
        try:
            file_size_mb = float(input("File size (MB): ").strip() or "0")
        except ValueError:
            print("File size must be a number.")
            return
        book = EBook(
            book_id, title, author, year, genre,
            file_format=file_format, file_size_mb=file_size_mb,
            copies_total=copies,
        )
    elif kind == "3":
        narrator = input("Narrator: ").strip()
        try:
            duration = int(input("Duration (minutes): ").strip() or "0")
        except ValueError:
            print("Duration must be a whole number.")
            return
        book = AudioBook(
            book_id, title, author, year, genre,
            narrator=narrator, duration_minutes=duration,
            copies_total=copies,
        )
    else:
        book = Book(book_id, title, author, year, genre, copies_total=copies)

    library.add_book(book)
    library.save()
    print(f"Added: {book}")


def do_search(library: Library) -> None:
    """Prompt for filters and print matching books."""
    query = input("Book ID or title contains (blank = any): ").strip() or None

    if query is not None:
        try:
            book = library.get_book(query)
        except KeyError:
            book = None

        if book is not None:
            print(f"\nFound 1 book:")
            print(f"  {book}")
            return

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


def do_list_books(library: Library) -> None:
    """Print every book in the inventory (all types)."""
    books = library.all_books()
    utils.section(f"ALL BOOKS ({len(books)})")
    if not books:
        print("No books in the library yet.")
        return
    for book in books:
        print(f"  {book}")


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
            elif choice == "9":
                do_list_books(library)
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
