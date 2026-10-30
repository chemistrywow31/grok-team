# Roster

> Guidance: this file lives in the private memory repo. Ids are written here, not in the public framework and not in a shared file. Fill an id as soon as that bot exists, and tell the bot who it reports to. Delete this guidance when you are done.

`preferred_language`: (from the interview)

`backup_repo`: (this private repo, unless the human named another private repo)
`backup_time`: (HH:MM)
`backup_timezone`: (the timezone they named)
`backup_push`: (human or main bot)
`backup_branch`: (pr, or main only when they said so)

| name | role | reports_to | id | channel |
| --- | --- | --- | --- | --- |
| Main bot | main bot | Human | (fill after creation) | |
| Knowledge Manager | knowledge manager | Main bot | (fill after creation) | |
| (name) | (coordinator, exec, or lead) | (name of the layer above) | (fill after creation) | |

Delete the Knowledge Manager row when the human declined that role. In the CEO shape, `reports_to` for that row is Chief of Staff.

## Direct lines

Default route: up one layer, then across. Tasks, decisions, cross-office work, and anything that spends quota use that route.

A bot may message another bot directly only when a row below lists that pair or that layer. Reading this roster does not allow a message.

| who asks | who may be asked | for |
| --- | --- | --- |
| any bot | Knowledge Manager | a shared fact |

Delete the Knowledge Manager row when the human declined that role. Add a row only when the plan named it. If no row remains, write `none`.

A direct line asks a fact or asks advice. It does not assign work, does not touch another office's project, and does not spend money. The message names who is asking. If the answer changes the work, the asker puts it in the next eight-line report. `priority: true` only when a person is waiting. Otherwise `priority: false`. Whether that bot has `SendToAgent` is unknown. If the call is missing, the ask goes up one layer.

Until an id is filled in, do not assume `SendToAgent` can find that bot.

The CEO sample, with placeholder offices only, is `templates/roster-ceo-example.md` in the framework repo. Do not copy ids from anywhere. There are none.
