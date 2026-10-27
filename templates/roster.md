# Roster

> Guidance: copy this into the human's private memory repo before you fill it in. Ids go only in that private file. This public template has no real ids. Delete this guidance after you copy it.

`preferred_language`: (set in the interview, for example `en` or `zh-TW`)

`backup_repo`: (the private repo the human named in the interview)
`backup_time`: (HH:MM)
`backup_timezone`: (the timezone they named)
`backup_push`: (human or main bot)
`backup_branch`: (pr, or main only when they said so)

You do not invent a repo URL. The daily backup spec is [../docs/backup.md](../docs/backup.md).

A bot does not know the others' ids until it is told. After you create a bot, write the id here and tell that bot who it reports to.

| name | role | reports_to | id | channel |
| --- | --- | --- | --- | --- |
| Main bot | main bot | Human | (fill after creation) | (war room name, or blank) |
| Dev coordinator | coordinator | Main bot | (fill after creation) | |
| Knowledge Manager | knowledge manager | Main bot | (fill after creation) | |
| Project A lead | lead | Dev coordinator | (fill after creation) | |

`role` is `main bot`, `coordinator`, `exec`, `knowledge manager`, or `lead`, or a name the human chose. `reports_to` is the name of the layer above. With no coordinator layer, a lead's `reports_to` is the main bot.

Delete the Knowledge Manager row when the human declined that role. It reports to the main bot. It is not a lead. Leads may ask it. Leads still do not message each other. The spec is [../docs/knowledge-manager.md](../docs/knowledge-manager.md).

The CEO shape has its own sample: [roster-ceo-example.md](roster-ceo-example.md).
