"""
Inspect SQLite database vs SQLAlchemy models and Alembic revision.

Run from the backend root (same directory as alembic.ini):

    python scripts/check_db.py

Use this before applying migrations to see the current revision and any
missing tables or columns.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

# Backend root (parent of scripts/)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

load_dotenv(ROOT / ".env")

from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402


def _sqlite_file_path(url: str) -> Path | None:
    """Return path for a sqlite file URL, or None if not a file-based sqlite URL."""
    if not url.startswith("sqlite"):
        return None
    # sqlite:///relative  or  sqlite:////absolute
    rest = url.split("sqlite:///", 1)[-1]
    if rest.startswith("/") or re.match(r"^[A-Za-z]:", rest):
        return Path(rest)
    return (ROOT / rest).resolve()


def _alembic_from_db(engine) -> str | None:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='alembic_version'"
            )
        ).fetchone()
        if not row:
            return None
        v = conn.execute(text("SELECT version_num FROM alembic_version")).fetchone()
        return v[0] if v else None


def _alembic_cli(*args: str) -> tuple[int, str]:
    try:
        p = subprocess.run(
            [sys.executable, "-m", "alembic", *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        raw = ((p.stdout or "") + "\n" + (p.stderr or "")).strip()
        # Drop Alembic logging noise on stderr
        lines = [ln for ln in raw.splitlines() if "INFO  [alembic" not in ln]
        combined = "\n".join(lines).strip()
        return p.returncode, combined
    except FileNotFoundError:
        return -1, "python -m alembic failed (install requirements.txt)"


def _schema_drift(engine) -> list[str]:
    messages: list[str] = []
    insp = inspect(engine)
    for table_name, table in Base.metadata.tables.items():
        if not insp.has_table(table_name):
            messages.append(f"Missing table (expected by models): {table_name}")
            continue
        db_cols = {c["name"] for c in insp.get_columns(table_name)}
        model_cols = {c.name for c in table.columns}
        missing = sorted(model_cols - db_cols)
        if missing:
            messages.append(
                f"Table {table_name!r} missing column(s): {', '.join(missing)}"
            )
    return messages


def main() -> int:
    print("UC Cookbook - database check")
    print("=" * 50)

    url = settings.DATABASE_URL
    db_path = _sqlite_file_path(url)
    if db_path is not None:
        print(f"Database file: {db_path}")
        print(f"File exists: {db_path.is_file()}")
    else:
        print(f"Database URL: {url}")

    engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
    )

    if db_path is not None and not db_path.is_file():
        print("\nNo database file yet. Create it with: alembic upgrade head")
        return 0

    rev = _alembic_from_db(engine)
    print(f"\nAlembic version in DB: {rev if rev is not None else '(no alembic_version table)'}")

    code, out = _alembic_cli("current")
    print(f"\n`alembic current` (exit {code}):\n{out or '(no output)'}")

    code_h, heads_out = _alembic_cli("heads")
    print(f"\n`alembic heads` (exit {code_h}):\n{heads_out or '(no output)'}")

    drift = _schema_drift(engine)
    print("\nModel vs database columns:")
    if drift:
        for line in drift:
            print(f"  - {line}")
        print("\nNext step: alembic upgrade head")
    else:
        print("  (no missing tables or columns)")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Ensure .env exists (copy from .env.example) and dependencies are installed.", file=sys.stderr)
        raise SystemExit(1)
