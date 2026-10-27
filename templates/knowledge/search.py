"""One search interface for both modes.

python3 search.py --knowledge /path/to/knowledge "shared hours"

index: auto  use index.db when it is present, otherwise scan the markdown
index: on    use index.db when it is present, otherwise scan the markdown
index: off   scan the markdown even if index.db is present

Stdout is the same shape in every mode: a mode line, then path and snippet,
or the word none. A missing index does not change that shape.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

from kmcommon import iter_topic_files, load_config, rel_path, split_front_matter


def _snippet(text: str, query: str, limit: int = 160) -> str:
    haystack = text.replace("\n", " ")
    folded = haystack.casefold()
    needle = query.casefold()
    at = folded.find(needle)
    if at < 0:
        at = 0
    start = max(0, at - 40)
    piece = haystack[start : start + limit].strip()
    return piece


def plain_search(knowledge: Path, query: str) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    needle = query.casefold()
    for path in iter_topic_files(knowledge):
        try:
            text = path.read_text(encoding="utf-8")
            fields, body = split_front_matter(text)
        except (UnicodeDecodeError, ValueError):
            continue
        if fields["sensitivity"] == "secret-never-store":
            continue
        blob = "\n".join((fields["title"], fields["topic"], body))
        if needle in blob.casefold():
            hits.append((rel_path(knowledge, path), _snippet(blob, query)))
    return hits


def _fts_query(query: str) -> str:
    return '"' + query.replace('"', '""') + '"'


def index_search(db: Path, query: str) -> list[tuple[str, str]] | None:
    if not db.is_file():
        return None
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        tokenizer = conn.execute("SELECT value FROM meta WHERE key = 'tokenizer'").fetchone()
        if tokenizer and tokenizer[0] == "trigram" and len(query) < 3:
            print(
                "query shorter than 3 characters; trigram cannot search it; searched the markdown",
                file=sys.stderr,
            )
            return None
        rows = conn.execute(
            """
            SELECT path, snippet(docs_fts, 3, '', '', ' … ', 8)
            FROM docs_fts
            WHERE docs_fts MATCH ?
            ORDER BY path
            """,
            (_fts_query(query),),
        ).fetchall()
    finally:
        conn.close()
    return [(path, snippet.strip()) for path, snippet in rows]


def search(knowledge: Path, query: str) -> tuple[str, list[tuple[str, str]]]:
    config = load_config(knowledge)
    mode = config["index"] or "auto"
    db = knowledge / "index.db"
    if mode == "off":
        return "plain", plain_search(knowledge, query)
    found = index_search(db, query)
    if found is None:
        if mode in {"auto", "on"} and not db.is_file():
            print("index.db is absent; searched the markdown", file=sys.stderr)
        return "plain", plain_search(knowledge, query)
    return "index", found


def render(mode: str, hits: list[tuple[str, str]]) -> str:
    lines = [f"mode: {mode}"]
    if not hits:
        lines.append("none")
        return "\n".join(lines) + "\n"
    blocks = []
    for path, snippet in hits:
        blocks.append(f"path: {path}\nsnippet: {snippet}")
    lines.append("\n\n".join(blocks))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Search knowledge markdown or the index.")
    parser.add_argument("--knowledge", required=True, type=Path)
    parser.add_argument("query", nargs="+")
    args = parser.parse_args(argv)
    query = " ".join(args.query).strip()
    if not query:
        print("empty query", file=sys.stderr)
        return 1
    try:
        mode, hits = search(args.knowledge.resolve(), query)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    sys.stdout.write(render(mode, hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
