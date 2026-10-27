updated: YYYY-MM-DD
topics: none
refused: none
knowledge check: missing
index_copied: no

This is a placeholder. The Knowledge Manager replaces it after a backup export. Until then the main bot keeps the rebuild lines and does not copy a database.

```sh
python3 build_index.py --knowledge <path to knowledge>
```

`index.db`, `index.db-wal`, and `index.db-shm` are not part of the backup. Rebuild from the markdown. Do not copy a live database with `cp`.
