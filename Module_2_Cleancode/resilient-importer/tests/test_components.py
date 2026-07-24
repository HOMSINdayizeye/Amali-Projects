from pathlib import Path

import pytest

from resilient_importer.exceptions import FileFormatError
from resilient_importer.models import User
from resilient_importer.parser import CSVParser
from resilient_importer.validator import UserValidator
from tests.factories import make_user


class TestCSVParser:
    def test_parse_valid_csv(self, tmp_path: Path):
        csv_file = tmp_path / "users.csv"
        csv_file.write_text("user_id,name,email\n1,Alice,alice@example.com\n")

        parser = CSVParser(csv_file)
        users = list(parser.parse())

        assert len(users) == 1
        assert users[0].user_id == "1"
        assert users[0].name == "Alice"
        assert users[0].email == "alice@example.com"

    def test_parse_missing_file_raises(self, tmp_path: Path):
        parser = CSVParser(tmp_path / "missing.csv")
        with pytest.raises(FileFormatError):
            list(parser.parse())

    def test_parse_missing_columns_raises(self, tmp_path: Path):
        csv_file = tmp_path / "bad.csv"
        csv_file.write_text("id,name\n1,Alice\n")

        parser = CSVParser(csv_file)
        with pytest.raises(FileFormatError):
            list(parser.parse())

    def test_parse_missing_column_in_row_raises(self, tmp_path: Path):
        csv_file = tmp_path / "bad_row.csv"
        csv_file.write_text("user_id,name,email\n1,Alice\n")

        parser = CSVParser(csv_file)
        with pytest.raises(FileFormatError):
            list(parser.parse())


class TestUserValidator:
    @pytest.mark.parametrize(
        "user,expected_errors",
        [
            (make_user(email="test@example.com"), []),
            (make_user(email="invalid-email"), ["Invalid email address"]),
            (make_user(name=""), ["name must not be empty"]),
            (
                User(user_id="", name="Alice", email="a@example.com"),
                ["user_id must not be empty"],
            ),
        ],
    )
    def test_validation_cases(self, user, expected_errors):
        result = UserValidator().validate(user)
        assert result.is_valid is (len(expected_errors) == 0)
        for expected in expected_errors:
            assert any(expected in e for e in result.errors)
