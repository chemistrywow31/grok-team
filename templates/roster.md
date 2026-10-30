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

<!-- roster-meta:start -->
## Roster meta

> Guidance: keep this section only when interview question 5c said yes to C-level direct asks, named a special role, or said yes to peer leads. If all three were no, delete everything from the start marker to the end marker, markers included. Delete this guidance after you fill it.

This is looser than the default rule that leads do not message each other. The human chose it.

| name | meta |
| --- | --- |
| (a name from the table above) | (`layer: c-level`, `kind: special`, `peer: lead`, or more than one, joined by `; `) |

- `layer: c-level`: a C-level exec directly under the Chief of Staff. Bots with this value may ask each other directly.
- `kind: special`: any bot may ask this bot directly.
- `peer: lead`: a lead opened for peer asks. Two leads that both have this value may ask each other directly, whoever they report to. This is a limited exception to the rule that leads do not message each other.
- Allowed values are only these three, each at most once per row, joined by `; `. `layer: c-level` goes only on an `exec` row under the Chief of Staff. `peer: lead` goes only on a `lead` row. Each of the two needs at least two rows, or it is left out.
- A direct ask is consult or read-only. Consult means asking questions and looking up information. Read-only means reading what the other bot allows you to see. It changes nothing: the asker does not ask the other bot to do work (no executing, forwarding, writing, or running on its behalf), and does not change anything of the other bot's (files, settings, memory, or project). Assigning work, touching another bot's project, and spending quota go up the org line. The asker still sends its own eight-line report up.
- A bot that gets a direct ask only answers. It does not take the ask as an assignment. If the ask is really a task, it replies that the task must go up the org line.
- Only the human sets or changes meta, after a new yes. A bot never adds or removes meta.

<!-- roster-meta:end -->
The CEO shape has its own sample: [roster-ceo-example.md](roster-ceo-example.md).
