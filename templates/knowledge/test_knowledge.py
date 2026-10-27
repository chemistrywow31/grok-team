"""Run: python3 templates/knowledge/test_knowledge.py"""

from __future__ import annotations

import filecmp
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_index  # noqa: E402
import export_markdown  # noqa: E402
import import_markdown  # noqa: E402
import search  # noqa: E402
from kmcommon import render_markdown  # noqa: E402


def _write(path: Path, fields: dict[str, str], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_markdown(fields, body))


class KnowledgeTests(unittest.TestCase):
    def _sample(self, root: Path) -> None:
        (root / "config.yml").write_text("index: auto\nreview_after_days:\n", encoding="utf-8")
        (root / "README.md").write_text("Guide only. Token GUIDE-ONLY-WORD.\n", encoding="utf-8")
        _write(
            root / "hours.md",
            {
                "title": "Sample hours",
                "topic": "sample-hours",
                "owner": "Knowledge Manager",
                "scope": "all bots",
                "sensitivity": "internal",
                "source": "placeholder",
                "updated": "2026-01-02",
                "status": "active",
            },
            "Office hours are posted on the shared board.",
        )
        _write(
            root / "notes.md",
            {
                "title": "共享範例",
                "topic": "shared-example",
                "owner": "Knowledge Manager",
                "scope": "all bots",
                "sensitivity": "public",
                "source": "placeholder",
                "updated": "2026-01-03",
                "status": "active",
            },
            "共享知識放在記憶庫的 markdown 檔，不是索引。",
        )

    def test_round_trip_delete_and_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            root.mkdir()
            self._sample(root)
            code = build_index.build(root, root / "index.db")
            self.assertEqual(code, 0)
            from io import StringIO
            from contextlib import redirect_stdout

            second = StringIO()
            with redirect_stdout(second):
                self.assertEqual(build_index.build(root, root / "index.db"), 0)
            self.assertIn("unchanged: 2", second.getvalue())
            self.assertIn("updated: 0", second.getvalue())
            out = Path(tmp) / "exported"
            self.assertEqual(export_markdown.export_db(root / "index.db", out), 0)
            for name in ("hours.md", "notes.md"):
                self.assertTrue(filecmp.cmp(root / name, out / name, shallow=False))

            mode, hits = search.search(root, "共享知識")
            self.assertEqual(mode, "index")
            self.assertEqual([path for path, _ in hits], ["notes.md"])

            (root / "config.yml").write_text("index: off\n", encoding="utf-8")
            mode, hits = search.search(root, "共享知識")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["notes.md"])

            (root / "config.yml").write_text("index: auto\n", encoding="utf-8")
            (root / "notes.md").unlink()
            code = build_index.build(root, root / "index.db")
            self.assertEqual(code, 0)
            mode, hits = search.search(root, "共享知識")
            self.assertEqual(hits, [])
            out2 = Path(tmp) / "exported-after-delete"
            self.assertEqual(export_markdown.export_db(root / "index.db", out2), 0)
            self.assertFalse((out2 / "notes.md").exists())
            self.assertTrue((out2 / "hours.md").is_file())

    def test_fallback_when_index_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            root.mkdir()
            self._sample(root)
            mode, hits = search.search(root, "Office hours")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["hours.md"])
            mode, hits = search.search(root, "GUIDE-ONLY-WORD")
            self.assertEqual(hits, [])

    def test_import_review_then_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            src = base / "loose"
            src.mkdir()
            (src / "desk.txt").write_text("Desk note\n\nThe shared desk is on floor 2.\n", encoding="utf-8")
            (src / "secret.txt").write_text("token\npassword=hunter2\n", encoding="utf-8")
            review = base / "review"
            self.assertEqual(import_markdown.stage(src, review), 0)
            report = (review / "REPORT.txt").read_text(encoding="utf-8")
            self.assertIn("accepted: desk.txt", report)
            self.assertIn("refused: secret.txt", report)
            self.assertNotIn("hunter2", report)
            self.assertFalse((review / "secret.txt").exists())
            knowledge = base / "knowledge"
            knowledge.mkdir()
            (knowledge / "config.yml").write_text("index: on\n", encoding="utf-8")
            self.assertEqual(import_markdown.approve(review, knowledge), 0)
            self.assertTrue((knowledge / "desk.md").is_file())
            build_index.build(knowledge, knowledge / "index.db")
            out = base / "out"
            export_markdown.export_db(knowledge / "index.db", out)
            self.assertTrue(filecmp.cmp(knowledge / "desk.md", out / "desk.md", shallow=False))

    def test_backup_api_not_byte_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            root.mkdir()
            self._sample(root)
            dest = Path(tmp) / "copy.db"
            code = build_index.main(["--knowledge", str(root), "--backup-to", str(dest)])
            self.assertEqual(code, 0)
            self.assertTrue(dest.is_file())
            # The backup is a consistent database, not a requirement that sizes match a cp.
            mode_db = root / "index.db"
            self.assertGreater(dest.stat().st_size, 0)
            self.assertNotEqual(dest.resolve(), mode_db.resolve())

    def test_config_modes_keep_the_same_hits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            root.mkdir()
            self._sample(root)
            (root / "config.yml").unlink()
            mode, hits = search.search(root, "Office hours")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["hours.md"])

            (root / "config.yml").write_text("index: on\n", encoding="utf-8")
            mode, hits = search.search(root, "Office hours")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["hours.md"])

            self.assertEqual(build_index.build(root, root / "index.db"), 0)
            mode, hits = search.search(root, "Office hours")
            self.assertEqual(mode, "index")
            self.assertEqual([path for path, _ in hits], ["hours.md"])

            (root / "config.yml").write_text("index: off\n", encoding="utf-8")
            mode, hits = search.search(root, "Office hours")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["hours.md"])

            (root / "config.yml").write_text("index: auto\n", encoding="utf-8")
            mode, hits = search.search(root, "共")
            self.assertEqual(mode, "plain")
            self.assertEqual([path for path, _ in hits], ["notes.md"])

            (root / "config.yml").write_text("index: maybe\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                search.search(root, "Office hours")

    def test_cli_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "knowledge"
            root.mkdir()
            self._sample(root)
            proc = subprocess.run(
                [sys.executable, str(HERE / "search.py"), "--knowledge", str(root), "Office hours"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0)
            self.assertIn("mode: plain", proc.stdout)
            self.assertIn("path: hours.md", proc.stdout)
            self.assertIn("index.db is absent", proc.stderr)


if __name__ == "__main__":
    unittest.main()
