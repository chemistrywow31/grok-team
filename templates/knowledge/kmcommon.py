"""Shared helpers for the knowledge scripts. Python 3 standard library only."""

from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path

FIELDS = (
    "title",
    "topic",
    "owner",
    "scope",
    "sensitivity",
    "source",
    "updated",
    "status",
)
SENSITIVITY = {"public", "internal", "secret-never-store"}
STATUS = {"active", "unverified", "stale"}
INDEX_MODES = {"auto", "on", "off"}

_SECRET_RE = re.compile(
    r"(-----BEGIN |api[_-]?key\s*[:=]|password\s*[:=]|x-access-token|ghp_[A-Za-z0-9]|sk-[A-Za-z0-9]{8,})",
    re.I,
)


def looks_like_secret(text: str) -> bool:
    return _SECRET_RE.search(text) is not None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_config(text: str) -> dict[str, str | None]:
    """Read the small config.yml subset: `key: value` lines. Blank value is None."""
    out: dict[str, str | None] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"bad config line: {raw}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        out[key] = value or None
    return out


def load_config(knowledge: Path) -> dict[str, str | None]:
    path = knowledge / "config.yml"
    if not path.is_file():
        return {"index": "auto", "review_after_days": None}
    data = parse_config(path.read_text(encoding="utf-8"))
    data.setdefault("index", "auto")
    data.setdefault("review_after_days", None)
    mode = data["index"]
    if mode not in INDEX_MODES:
        raise ValueError(f"index must be auto, on, or off; got {mode}")
    return data


def split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter is not closed")
    header = text[4:end]
    body = text[end + len("\n---\n") :]
    fields: dict[str, str] = {}
    for raw in header.splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"bad front matter line: {raw}")
        key, value = raw.split(":", 1)
        fields[key.strip()] = value.strip()
    missing = [name for name in FIELDS if name not in fields]
    if missing:
        raise ValueError("missing " + ", ".join(missing))
    if fields["sensitivity"] not in SENSITIVITY:
        raise ValueError("bad sensitivity")
    if fields["status"] not in STATUS:
        raise ValueError("bad status")
    return fields, body


def render_markdown(fields: dict[str, str], body: str) -> bytes:
    lines = ["---"]
    for name in FIELDS:
        lines.append(f"{name}: {fields[name]}")
    lines.append("---")
    lines.append("")
    text = "\n".join(lines) + body.strip() + "\n"
    return text.encode("utf-8")


def needs_trigram(texts: list[str]) -> bool:
    for text in texts:
        for char in text:
            code = ord(char)
            if (
                0x3040 <= code <= 0x30FF
                or 0x3400 <= code <= 0x4DBF
                or 0x4E00 <= code <= 0x9FFF
            ):
                return True
    return False


def iter_topic_files(knowledge: Path) -> list[Path]:
    files = []
    for path in sorted(knowledge.rglob("*.md")):
        if not path.is_file():
            continue
        if path.name == "README.md":
            continue
        if "bin" in path.relative_to(knowledge).parts:
            continue
        files.append(path)
    return files


def rel_path(knowledge: Path, path: Path) -> str:
    return path.relative_to(knowledge).as_posix()


def connect(db: Path) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def backup_database(src: Path, dest: Path) -> None:
    """Copy a database with the sqlite3 backup API. Do not use a plain file copy."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    source = sqlite3.connect(src)
    target = sqlite3.connect(dest)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
