"""JSON-backed user repository.

Simulates a database by persisting user records to a JSON file.
Tracks known user IDs in memory for fast duplicate detection and
writes the full dataset back to disk after each mutation.
"""

import json
from pathlib import Path
from typing import Set

from .exceptions import DuplicateUserError
from .models import User


class UserRepository:
    """Simulated database storage using a JSON file."""

    def __init__(self, db_path: Path):
        """Initialise the repository and load existing data.

        Args:
            db_path: Path to the JSON file used as the backing store.
        """
        self.db_path = db_path
        self._user_ids: Set[str] = set()
        self._cache: dict[str, tuple[str, str]] = {}
        self._load()

    def _load(self) -> None:
        """Load existing users from the JSON database."""
        if not self.db_path.exists():
            self.db_path.write_text("[]", encoding="utf-8")
            return

        with open(self.db_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for item in data:
                    self._user_ids.add(item["user_id"])
            except (json.JSONDecodeError, KeyError):
                self._user_ids = set()

    def _save(self) -> None:
        """Persist users to the JSON database."""
        data = [
            {"user_id": uid, "name": name, "email": email}
            for uid, (name, email) in self._cache.items()
        ]
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def add_user(self, user: User) -> None:
        """Add a user to the repository.

        Args:
            user: The User instance to persist.

        Raises:
            DuplicateUserError: If a user with the same ``user_id``
                already exists in the repository.
        """
        if user.user_id in self._user_ids:
            raise DuplicateUserError(f"Duplicate user_id: {user.user_id}")
        self._user_ids.add(user.user_id)
        self._cache[user.user_id] = (user.name, user.email)
        self._save()
