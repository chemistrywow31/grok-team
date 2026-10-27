"""Turn loose notes into front-matter files for review.

Nothing is written into the knowledge directory until --approve is set.
That flag is the human's or the Knowledge Manager's yes.

python3 import_markdown.py --src ./loose-notes --review ./knowledge-review
python3 import_markdown.py --approve --review ./knowledge-review --knowledge ./knowledge
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from kmcommon import looks_like_secret, render_markdown, sha256_bytes

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(name: str, raw: bytes) -> str:
    stem = Path(name).stem.lower()
    slug = _SLUG_RE.sub("-", stem).strip("-")
    if slug:
        return slug
    return "topic-" + sha256_bytes(raw)[:8]


def _proposal(name: str, raw: bytes) -> tuple[str, bytes] | str:
    if looks_like_secret(raw.decode("utf-8", errors="replace")):
        return "credential-like text; tell the human in person"
    text = raw.decode("utf-8")
    lines = text.splitlines()
    title = ""
    rest: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() and not title:
            title = line.strip()[:80]
            rest = lines[i + 1 :]
            break
    if not title:
        return "empty note"
    topic = _slug(name, raw)
    fields = {
        "title": title,
        "topic": topic,
        "owner": "Knowledge Manager",
        "scope": "all bots",
        "sensitivity": "internal",
        "source": f"import:{name}",
        "updated": date.today().isoformat(),
        "status": "unverified",
    }
    return topic, render_markdown(fields, "\n".join(rest))


def stage(src: Path, review: Path) -> int:
    if review.name == "knowledge" or (review / "config.yml").is_file():
        print("refusing to write a review into the knowledge directory", file=sys.stderr)
        return 1
    review.mkdir(parents=True, exist_ok=True)
    report: list[str] = []
    notes = sorted(p for p in src.iterdir() if p.is_file() and not p.name.startswith("."))
    if not notes:
        print("no notes", file=sys.stderr)
        return 1
    for path in notes:
        raw = path.read_bytes()
        result = _proposal(path.name, raw)
        if isinstance(result, str):
            report.append(f"refused: {path.name}: {result}")
            continue
        topic, data = result
        dest = review / f"{topic}.md"
        if dest.exists():
            report.append(f"refused: {path.name}: review file already exists")
            continue
        dest.write_bytes(data)
        report.append(f"accepted: {path.name} -> {topic}.md")
    (review / "REPORT.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))
    print("not written to the knowledge directory")
    return 0


def approve(review: Path, knowledge: Path) -> int:
    files = sorted(review.glob("*.md"))
    if not files:
        print("no review files", file=sys.stderr)
        return 1
    knowledge.mkdir(parents=True, exist_ok=True)
    for path in files:
        dest = knowledge / path.name
        if dest.exists():
            print(f"refused overwrite: {path.name}", file=sys.stderr)
            return 1
    for path in files:
        (knowledge / path.name).write_bytes(path.read_bytes())
        print(f"wrote: {path.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Review loose notes before they enter knowledge/.")
    parser.add_argument("--src", type=Path)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--knowledge", type=Path)
    args = parser.parse_args(argv)
    if args.approve:
        if not args.review or not args.knowledge:
            print("--approve needs --review and --knowledge", file=sys.stderr)
            return 1
        return approve(args.review.resolve(), args.knowledge.resolve())
    if not args.src or not args.review:
        print("needs --src and --review", file=sys.stderr)
        return 1
    return stage(args.src.resolve(), args.review.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
