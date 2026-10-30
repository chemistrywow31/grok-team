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

Delete the Knowledge Manager row when the human declined that role. It reports to the main bot. It is not a lead. The spec is [../docs/knowledge-manager.md](../docs/knowledge-manager.md).

## Direct lines

Default route: up one layer, then across. Tasks, decisions, cross-office work, and anything that spends quota use that route. You do not connect every bot to every other bot.

A bot may message another bot directly only when a row below lists that pair or that layer. Every bot can read this roster. Reading it does not allow a message.

| who asks | who may be asked | for |
| --- | --- | --- |
| any bot | Knowledge Manager | a shared fact |

Delete the Knowledge Manager row when the human declined that role. Add a row only when the human named it. An example you do not copy unless they said it: a lead asks a named advisor for advice. If no row remains, write `none`.

A direct line asks a fact or asks advice. It does not assign work, does not touch another office's project, and does not spend money. The message names who is asking. If the answer changes the work, the asker puts it in the next eight-line report. `priority: true` only when a person is waiting. Otherwise `priority: false`.

Whether that bot has `SendToAgent` is unknown. If the call is missing, the ask goes up one layer.

The CEO shape has its own sample: [roster-ceo-example.md](roster-ceo-example.md).
