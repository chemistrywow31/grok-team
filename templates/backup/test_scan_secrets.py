"""Run: python3 templates/backup/test_scan_secrets.py"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import scan_secrets  # noqa: E402


class ScanTests(unittest.TestCase):
    def test_clean_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main-bot.md").write_text(
                "---\nbot: Main bot\nupdated: 2026-01-02\n---\n\n## Journal\n\nnone\n",
                encoding="utf-8",
            )
            self.assertEqual(scan_secrets.scan_root(root), [])
            code = scan_secrets.main(["--root", str(root)])
            self.assertEqual(code, 0)

    def test_password_hit_hides_the_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            secret = "password=" + "hunter2"
            (root / "notes.md").write_text("token\n" + secret + "\n", encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(HERE / "scan_secrets.py"), "--root", str(root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertIn("hit: notes.md rule: password", proc.stdout)
            self.assertNotIn("hunter2", proc.stdout)
            self.assertNotIn("hunter2", proc.stderr)

    def test_email_phone_and_card_rules(self) -> None:
        address = "ada" + "@" + "example.com"
        phone = "Phone: " + "555" + "-0100"
        card = "4242" + "4242" + "4242" + "4242"
        text = "\n".join((address, phone, card))
        found = scan_secrets.hits_in_text(text)
        self.assertIn("email", found)
        self.assertIn("phone", found)
        self.assertIn("card", found)
        rendered = " ".join(found)
        self.assertNotIn(address, rendered)
        self.assertNotIn(card, rendered)


if __name__ == "__main__":
    unittest.main()
