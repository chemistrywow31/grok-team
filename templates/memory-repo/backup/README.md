# Backup

This directory is the daily export inside the private repo named on the roster as `backup_repo`. Markdown is the copy you keep. `index.db` is not copied here.

The main bot owns the routine `daily-backup`. Other bots write only their own `backup/<slug>.md` when asked. The Knowledge Manager also writes `knowledge-check.md`. The main bot commits. A day with no change stays quiet.

Full rules: https://github.com/chemistrywow31/grok-team/blob/main/docs/backup.md

Restore: https://github.com/chemistrywow31/grok-team/blob/main/docs/restore.md

Do not put a secret, a token, a card number, or a personal contact in this directory. Those stay with the human. This framework does not invent a vault screen.
