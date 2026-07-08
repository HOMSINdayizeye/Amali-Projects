"""Borrower domain model.

Represents a library member who can borrow and return books. The list of
currently-borrowed book ids is encapsulated and kept consistent through the
``borrow`` / ``return_book`` helpers.
"""

from __future__ import annotations

from typing import Optional


class Borrower:
    """A library member who borrows books.

    The borrowed items are tracked as a list of book resource ids. Internal
    state is private and exposed through properties.
    """

    def __init__(
        self,
        borrower_id: str,
        name: str,
        email: str,
        phone: str = "",
    ) -> None:
        self._borrower_id = borrower_id.strip().upper()
        self._name = name.strip()
        self._email = email.strip().lower()
        self._phone = phone.strip()
        # Active loans only (returned books are removed).
        self._borrowed_book_ids: list[str] = []

    # ------------------------------------------------------------------
    # Properties (encapsulation)
    # ------------------------------------------------------------------
    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value.strip().lower()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value.strip()

    @property
    def borrowed_book_ids(self) -> list[str]:
        """Return a copy so callers cannot mutate internal state directly."""
        return list(self._borrowed_book_ids)

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------
    def borrow(self, book_id: str) -> None:
        """Record a loan of ``book_id``.

        Raises:
            ValueError: if the borrower already has this book out.
        """
        bid = book_id.strip().upper()
        if bid in self._borrowed_book_ids:
            raise ValueError(f"{self._name} already borrowed {bid}.")
        self._borrowed_book_ids.append(bid)

    def return_book(self, book_id: str) -> None:
        """Remove a loan of ``book_id``.

        Raises:
            ValueError: if the borrower does not currently hold this book.
        """
        bid = book_id.strip().upper()
        if bid not in self._borrowed_book_ids:
            raise ValueError(f"{bid} is not currently borrowed by {self._name}.")
        self._borrowed_book_ids.remove(bid)

    # ------------------------------------------------------------------
    # Special methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"Borrower(id={self._borrower_id!r}, name={self._name!r}, "
            f"active_loans={len(self._borrowed_book_ids)})"
        )

    def __str__(self) -> str:
        return f"{self._name} <{self._email}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Borrower):
            return NotImplemented
        return self._borrower_id == other._borrower_id

    def __hash__(self) -> int:
        return hash(self._borrower_id)

    # ------------------------------------------------------------------
    # (De)serialisation
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "borrower_id": self._borrower_id,
            "name": self._name,
            "email": self._email,
            "phone": self._phone,
            "borrowed_book_ids": list(self._borrowed_book_ids),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Borrower":
        borrower = cls(
            borrower_id=data["borrower_id"],
            name=data["name"],
            email=data["email"],
            phone=data.get("phone", ""),
        )
        # Restore active loans captured at save time.
        borrower._borrowed_book_ids = [
            bid.strip().upper() for bid in data.get("borrowed_book_ids", [])
        ]
        return borrower
