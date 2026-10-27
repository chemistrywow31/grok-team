# Roster: CEO example

> Guidance: this is a sample shape, not a real roster. Copy the rows you need into the private memory repo. Ids stay blank until each bot exists, and they are written only in that private file. Delete this guidance when you copy.

`preferred_language`: (set in the interview)

The human is the CEO. The main bot is the Chief of Staff. Do not create a second chief of staff. The COO and the CTO coordinate. Office leads do the work.

Reporting, one layer at a time:

- Project office lead → CTO → Chief of Staff → CEO
- Team office lead → COO → Chief of Staff → CEO

Project offices are software projects. Team offices are operations or content teams. Delete any row that has no work. Leads do not message each other. They may ask the Knowledge Manager. Delete that row when the human declined the role. It reports to the Chief of Staff, beside the COO and the CTO, not under them.

| name | role | reports_to | id | channel |
| --- | --- | --- | --- | --- |
| Chief of Staff | main bot | CEO | (fill after creation) | (exec room, or blank) |
| COO | exec | Chief of Staff | (fill after creation) | |
| CTO | exec | Chief of Staff | (fill after creation) | |
| Knowledge Manager | knowledge manager | Chief of Staff | (fill after creation) | |
| Project Office A lead | lead | CTO | (fill after creation) | |
| Project Office B lead | lead | CTO | (fill after creation) | |
| Project Office C lead | lead | CTO | (fill after creation) | |
| Team Office X lead | lead | COO | (fill after creation) | |
| Team Office Y lead | lead | COO | (fill after creation) | |
| Team Office Z lead | lead | COO | (fill after creation) | |

An exec room, if you open one, is the Chief of Staff, the COO, and the CTO. The CEO joins only if they want to. Office leads stay out until someone names them. A room holds at most 6 members, including the main bot.

See [../docs/architecture.md](../docs/architecture.md#example-ceo) and [../docs/interview.md](../docs/interview.md).
