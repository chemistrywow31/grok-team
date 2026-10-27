# Architecture

> Guidance: replace this with the layers the human agreed to. Fill the tables after the interview. A small setup does not need a coordinator layer. Delete this guidance when you are done.

Headings stay English. Cell text may be in the human's language.

## Layers

(Top to bottom. Owner shape: Human → Main bot → Lead. CEO shape: CEO → Chief of Staff → COO and CTO → office leads. A mix is allowed.)

## Reporting lines

Reports go up one layer at a time.

| name | reports_to | does | leaves alone |
| --- | --- | --- | --- |
| Main bot | Human | coordinate, summarize reports, keep this memory repo | does not write a lead's progress page |
| Knowledge Manager | Main bot | answer shared questions from `knowledge/`; only writer of topic files after the skeleton | does not edit project repos or task boards |
| (lead name) | (layer above) | (the named scope) | does not message other leads; may ask the Knowledge Manager |

Delete the Knowledge Manager row when the human declined that role. It reports to the main bot (the chief of staff in the CEO shape). It does not report to the COO or the CTO. Markdown in `knowledge/` is the source of truth. `index.db` is derived. The daily backup commits that markdown and the files under `backup/`. It does not commit a database. The roster holds `backup_repo`.

## Decisions

| date | decision | why |
| --- | --- | --- |
| YYYY-MM-DD | (one sentence) | (one sentence) |

## Sensitivity

| project | repo visibility | data rule |
| --- | --- | --- |
| (name) | private or public | (the human's rule. If they set none, write: repo stays private) |
