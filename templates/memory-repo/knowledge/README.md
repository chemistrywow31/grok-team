# Knowledge

Shared facts for every bot live in this directory, one topic per markdown file. The markdown is the source of truth. `index.db` is a derived search file. Delete it whenever you want. Rebuild it with `build_index.py`. Do not commit it.

`config.yml` is part of the layout from the start:

```yaml
index: auto
review_after_days:
```

`index` is `auto`, `on`, or `off`. `auto` uses `index.db` when the file is present and otherwise scans the markdown. `on` does the same when the file is missing: the scan is the fallback, and the output is still `path` plus `snippet`. `off` always scans the markdown. Turning the index on later is one command, `python3 build_index.py --knowledge <this directory>`. Front matter, bot prompts, and message formats stay as they are.

Leave `review_after_days` empty until the human names a number. An empty value means there is no schedule.

## Front matter

Each topic file starts with:

```yaml
---
title: Sample topic
topic: sample-topic
owner: Knowledge Manager
scope: all bots
sensitivity: internal
source: placeholder, replace with the real source
updated: YYYY-MM-DD
status: unverified
---
```

`sensitivity` is `public`, `internal`, or `secret-never-store`. Do not use `secret-never-store` as a place to keep a secret. Refuse the text and tell the human in person.

`status` is `active`, `unverified`, or `stale`. `active` means the Knowledge Manager has checked the source. A newer `active` file on the same `topic` wins. The older `active` file is marked `stale`. An `unverified` file does not replace an `active` one.

## Never store

- Secrets, keys, passwords, and credentials.
- Anything the human lists here as employer-confidential. The human names that list. Do not invent an employer.

If a note matches that list, do not write it in this directory, in chat, or in the index. Say that it was refused, and that the human handles it in person.

## Who writes

Only the Knowledge Manager creates or edits topic files after the skeleton exists. Other bots send an add request. They do not edit these files.

The scripts live in the framework at `templates/knowledge/`. Read them by URL and run them with `python3` against this directory. Entry point:

```sh
python3 search.py --knowledge /path/to/knowledge "your query"
```

`README.md` in this folder is the guide. It is not a topic file. The search skips it.

Bots share these facts because they read this same private repo. Bots on the same computer also see the same files on disk, including `index.db` if it exists. The markdown is still the source of truth.
