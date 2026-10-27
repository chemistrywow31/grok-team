"""Rebuild knowledge/index.db from markdown. The markdown stays the source of truth.

python3 build_index.py --knowledge /path/to/knowledge
python3 build_index.py --knowledge /path/to/knowledge --backup-to /path/to/copy.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from kmcommon import (
    backup_database,
    connect,
    iter_topic_files,
    looks_like_secret,
    needs_trigram,
    rel_path,
    sha256_bytes,
    split_front_matter,
)


def _create_schema(conn, tokenizer: str) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS docs_fts;
        DROP TABLE IF EXISTS docs;
        DROP TABLE IF EXISTS meta;
        """
    )
    conn.execute(
        """
        CREATE TABLE docs (
            path TEXT PRIMARY KEY,
            sha256 TEXT NOT NULL,
            raw BLOB NOT NULL,
            title TEXT NOT NULL,
            topic TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )
    conn.execute(
        f"""
        CREATE VIRTUAL TABLE docs_fts USING fts5(
            path UNINDEXED,
            title,
            topic,
            body,
            tokenize = '{tokenizer}'
        )
        """
    )
    conn.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    conn.execute("INSERT INTO meta (key, value) VALUES ('tokenizer', ?)", (tokenizer,))


def _upsert(conn, path: str, digest: str, raw: bytes, title: str, topic: str, body: str) -> None:
    conn.execute("DELETE FROM docs_fts WHERE path = ?", (path,))
    conn.execute("DELETE FROM docs WHERE path = ?", (path,))
    conn.execute(
        """
        INSERT INTO docs (path, sha256, raw, title, topic, body)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (path, digest, raw, title, topic, body),
    )
    conn.execute(
        "INSERT INTO docs_fts (path, title, topic, body) VALUES (?, ?, ?, ?)",
        (path, title, topic, body),
    )


def build(knowledge: Path, db: Path) -> int:
    loaded: list[tuple[str, bytes, str]] = []
    problems: list[str] = []
    texts: list[str] = []
    for path in iter_topic_files(knowledge):
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
            fields, body = split_front_matter(text)
        except (UnicodeDecodeError, ValueError) as exc:
            problems.append(f"{rel_path(knowledge, path)}: {exc}")
            continue
        if fields["sensitivity"] == "secret-never-store" or looks_like_secret(text):
            problems.append(
                f"{rel_path(knowledge, path)}: refused, secret-like content is not indexed"
            )
            continue
        rel = rel_path(knowledge, path)
        loaded.append((rel, raw, text))
        texts.append(text)

    tokenizer = "trigram" if needs_trigram(texts) else "unicode61"
    updated = 0
    deleted = 0
    unchanged = 0
    conn = connect(db)
    try:
        row = None
        exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'meta'"
        ).fetchone()
        if exists:
            row = conn.execute("SELECT value FROM meta WHERE key = 'tokenizer'").fetchone()
        if row is None or row[0] != tokenizer:
            _create_schema(conn, tokenizer)
            current: dict[str, str] = {}
        else:
            current = dict(conn.execute("SELECT path, sha256 FROM docs"))

        seen: set[str] = set()
        updated = 0
        unchanged = 0
        for rel, raw, text in loaded:
            seen.add(rel)
            digest = sha256_bytes(raw)
            if current.get(rel) == digest:
                unchanged += 1
                continue
            fields, body = split_front_matter(text)
            _upsert(conn, rel, digest, raw, fields["title"], fields["topic"], body)
            updated += 1

        deleted = 0
        for old in list(current):
            if old in seen:
                continue
            conn.execute("DELETE FROM docs_fts WHERE path = ?", (old,))
            conn.execute("DELETE FROM docs WHERE path = ?", (old,))
            deleted += 1
        # A refused file must not stay in the index from an older run.
        for line in problems:
            rel = line.split(":", 1)[0]
            if conn.execute("SELECT 1 FROM docs WHERE path = ?", (rel,)).fetchone():
                conn.execute("DELETE FROM docs_fts WHERE path = ?", (rel,))
                conn.execute("DELETE FROM docs WHERE path = ?", (rel,))
                deleted += 1
        conn.commit()
    finally:
        conn.close()

    print(f"tokenizer: {tokenizer}")
    print(f"updated: {updated}")
    print(f"deleted: {deleted}")
    print(f"unchanged: {unchanged}")
    for line in problems:
        print(line, file=sys.stderr)
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build knowledge/index.db from markdown.")
    parser.add_argument("--knowledge", required=True, type=Path)
    parser.add_argument("--db", type=Path)
    parser.add_argument("--backup-to", type=Path)
    args = parser.parse_args(argv)
    knowledge = args.knowledge.resolve()
    db = (args.db or (knowledge / "index.db")).resolve()
    code = build(knowledge, db)
    if args.backup_to:
        backup_database(db, args.backup_to.resolve())
        print(f"backup: {args.backup_to}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
