from pathlib import Path

import pytest

from resilient_importer.exceptions import DuplicateUserError
from resilient_importer.repository import UserRepository
from tests.factories import make_user


class TestUserRepository:
    def test_add_user_creates_file(self, tmp_path: Path):
        db_path = tmp_path / "db.json"
        repo = UserRepository(db_path)
        user = make_user(user_id="1", name="Alice", email="alice@example.com")

        repo.add_user(user)

        assert db_path.exists()
        content = db_path.read_text(encoding="utf-8")
        assert "Alice" in content

    def test_add_duplicate_user_raises(self, tmp_path: Path):
        db_path = tmp_path / "db.json"
        repo = UserRepository(db_path)
        user = make_user(user_id="1")

        repo.add_user(user)

        with pytest.raises(DuplicateUserError):
            repo.add_user(user)

    def test_load_existing_data(self, tmp_path: Path):
        db_path = tmp_path / "db.json"
        db_path.write_text(
            '[{"user_id": "1", "name": "Alice", "email": "a@example.com"}]',
            encoding="utf-8",
        )

        repo = UserRepository(db_path)

        user = make_user(user_id="1", name="Alice", email="a@example.com")
        with pytest.raises(DuplicateUserError):
            repo.add_user(user)

    def test_load_corrupted_json(self, tmp_path: Path):
        db_path = tmp_path / "db.json"
        db_path.write_text("not valid json", encoding="utf-8")

        repo = UserRepository(db_path)

        user = make_user(user_id="1", name="Alice", email="a@example.com")
        repo.add_user(user)
        assert db_path.exists()
