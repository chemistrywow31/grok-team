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

Delete the Knowledge Manager row when the human declined that role. In the CEO shape, `reports_to` for that row is Chief of Staff. Leads may ask it. Leads still do not message each other.

Until an id is filled in, do not assume `SendToAgent` can find that bot.

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
The CEO sample, with placeholder offices only, is `templates/roster-ceo-example.md` in the framework repo. Do not copy ids from anywhere. There are none.
