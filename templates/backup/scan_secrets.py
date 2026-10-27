"""Scan backup markdown for secret-shaped text. Python 3 standard library only.

python3 scan_secrets.py --root /path/to/directory

Prints `clean` and exits 0, or `hit: <path> rule: <rule>` and exits 1.
The matched text is never printed.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("pem", re.compile(r"-----BEGIN ")),
    ("api-key", re.compile(r"api[_-]?key\s*[:=]", re.I)),
    ("password", re.compile(r"password\s*[:=]", re.I)),
    ("token", re.compile(r"x-access-token|ghp_[A-Za-z0-9]", re.I)),
    ("secret-key", re.compile(r"sk-[A-Za-z0-9]{8,}")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("phone", re.compile(r"(?im)^.*\b(?:phone|tel)\b\s*[:=].*\d")),
]

_CARD_RE = re.compile(r"\d(?:[\d -]{11,22}\d)")


def _luhn(digits: str) -> bool:
    total = 0
    for index, char in enumerate(reversed(digits)):
        value = int(char)
        if index % 2 == 1:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0


def _card_hit(text: str) -> bool:
    for match in _CARD_RE.finditer(text):
        digits = re.sub(r"\D", "", match.group(0))
        if 13 <= len(digits) <= 19 and _luhn(digits):
            return True
    return False


def hits_in_text(text: str) -> list[str]:
    found: list[str] = []
    for name, pattern in RULES:
        if pattern.search(text):
            found.append(name)
    if _card_hit(text):
        found.append("card")
    return found


def _relative(root: Path, path: Path) -> str:
    if root.is_file():
        return path.name
    return path.relative_to(root).as_posix()


def scan_root(root: Path) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    files = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        relative = _relative(root, path)
        if path.name in {"index.db", "index.db-wal", "index.db-shm"}:
            hits.append((relative, "database"))
            continue
        if path.suffix.lower() not in {".md", ".yml", ".yaml", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            hits.append((relative, "binary"))
            continue
        for rule in hits_in_text(text):
            hits.append((relative, rule))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan markdown for secret-shaped text.")
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args(argv)
    root = args.root
    if not root.exists():
        print("missing root", file=sys.stderr)
        return 2
    found = scan_root(root)
    if not found:
        sys.stdout.write("clean\n")
        return 0
    for path, rule in found:
        sys.stdout.write(f"hit: {path} rule: {rule}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
