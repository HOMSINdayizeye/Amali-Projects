from pathlib import Path

import pytest

from resilient_importer.exceptions import ImporterError, InvalidUserDataError
from resilient_importer.importer import Importer


class TestImporter:
    def test_import_valid_csv(self, tmp_path: Path):
        csv_file = tmp_path / "users.csv"
        csv_file.write_text("user_id,name,email\n1,Alice,alice@example.com\n")
        db_path = tmp_path / "db.json"

        importer = Importer(csv_path=csv_file, db_path=db_path)
        imported = importer.run()

        assert len(imported) == 1
        assert imported[0].name == "Alice"

    def test_import_skips_invalid_rows(self, tmp_path: Path):
        csv_file = tmp_path / "users.csv"
        csv_file.write_text(
            "user_id,name,email\n" "1,Alice,alice@example.com\n" "2,,bad@example.com\n"
        )
        db_path = tmp_path / "db.json"

        importer = Importer(csv_path=csv_file, db_path=db_path)

        with pytest.raises(InvalidUserDataError):
            importer.run()

    def test_import_unexpected_error_raises_importer_error(
        self, tmp_path: Path, mocker
    ):
        csv_file = tmp_path / "users.csv"
        csv_file.write_text("user_id,name,email\n1,Alice,alice@example.com\n")
        db_path = tmp_path / "db.json"

        importer = Importer(csv_path=csv_file, db_path=db_path)

        mock_repo = mocker.Mock()
        mock_repo.add_user.side_effect = RuntimeError("db down")
        importer.repository = mock_repo

        with pytest.raises(ImporterError):
            importer.run()

        mock_repo.add_user.assert_called_once()
