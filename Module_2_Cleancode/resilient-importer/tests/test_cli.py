from pathlib import Path

from resilient_importer.cli import main


def test_cli_success(tmp_path: Path):
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("user_id,name,email\n1,Alice,alice@example.com\n")
    db_path = tmp_path / "db.json"

    exit_code = main([str(csv_file), "--db", str(db_path)])

    assert exit_code == 0


def test_cli_missing_file(tmp_path: Path):
    db_path = tmp_path / "db.json"

    exit_code = main([str(tmp_path / "missing.csv"), "--db", str(db_path)])

    assert exit_code == 1


def test_cli_main_block_exits_zero(tmp_path: Path):
    csv_file = tmp_path / "users.csv"
    csv_file.write_text("user_id,name,email\n1,Alice,alice@example.com\n")
    db_path = tmp_path / "db.json"

    exit_code = main([str(csv_file), "--db", str(db_path)])

    assert exit_code == 0
