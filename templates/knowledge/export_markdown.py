"""Write markdown files back out of index.db. Bytes match the indexed files.

python3 export_markdown.py --db /path/to/index.db --out /path/to/dir

This does not accept loose notes. Use import_markdown.py for those.
A bulk import becomes markdown only in the review directory, and only
moves into knowledge/ when import_markdown.py is run with --approve.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


def export_db(db: Path, out: Path) -> int:
    if not db.is_file():
        print(f"index.db is absent: {db}", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    try:
        rows = conn.execute("SELECT path, raw FROM docs ORDER BY path").fetchall()
    finally:
        conn.close()
    count = 0
    for rel, raw in rows:
        if rel.startswith("/") or ".." in Path(rel).parts:
            print(f"refused path: {rel}", file=sys.stderr)
            return 1
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = raw if isinstance(raw, bytes) else bytes(raw)
        dest.write_bytes(data)
        count += 1
    print(f"exported: {count}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export indexed markdown unchanged.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    return export_db(args.db.resolve(), args.out.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
