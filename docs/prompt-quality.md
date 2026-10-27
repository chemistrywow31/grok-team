# Prompt quality

You are reading why the bot prompts in this repo are shaped this way. The prompts themselves are `AGENTS.md`, `docs/operating-rules.md`, `docs/interview.md`, `docs/grok-bot-setup.md`, `docs/knowledge-manager.md`, `docs/backup.md`, `docs/restore.md`, `templates/lead-brief.md`, `templates/coordinator-brief.md`, `templates/knowledge-manager-brief.md`, `templates/backup-routine-prompt.md`, `templates/backup-export-request.md`, `templates/memory-repo/AGENTS.md`, and the two copy-paste lines in the README quick start.

This file is notes for a person editing those prompts. It is not a bot persona.

## How to read the labels

xAI has no single text-model system-prompt guide. The full official system-prompt guide is for voice. The coding guide has left the live docs. Many rules below are from a voice guide, a coding guide, Grok Bot docs, or xAI's own prompts. The tag says which.

- **official**: xAI states it in a doc.
- **demonstrated**: xAI's own published prompts do it. xAI does not state it as a rule.
- **inference**: a reading of those sources. Used here only where it removes a real failure mode.

Scope names: `S2S` voice, `BP` text best practices, `GCF` the removed Grok Code guide, `MA` multi-agent research, `SK` Grok Bot skills and routines, `BOTS` Grok Bot bots, `PI` prompt-injection cookbook, `GP` the grok-prompts repo, `REF` the refund-agent prompt.

## Rules these prompts follow

- **No conflicts, concrete task, direct output.** Official. Scope: `S2S`, `BP`, `GCF`, `MA`. The plan has one format, the report has eight lines, a yes is defined with examples of what is not a yes. Sources: [voice prompting guide](https://docs.x.ai/developers/model-capabilities/audio/speech-to-speech/prompting-guide), [text best practices](https://docs.x.ai/developers/model-capabilities/text/best-practices), [Grok Code guide (archived)](https://web.archive.org/web/20251118014240/https://docs.x.ai/docs/guides/grok-code-prompt-engineering), [multi-agent prompting](https://docs.x.ai/developers/model-capabilities/text/multi-agent).
- **Short bullets, one hard rule per bullet, no "try to" or "ideally" in a hard rule.** Official. Scope: `S2S`. Same voice guide.
- **Examples, because the model copies them.** Official. Scope: `S2S`. Reports, yes/no, and untrusted sentences are quoted. Each example says what not to copy (sample office names, English values when the human uses another language).
- **Language is pinned.** Official. Scope: `S2S`. Docs stay English. Speech to the human uses `preferred_language`. Report labels stay English. Report values use the human's language. `none` is not translated.
- **Numeric limits where length matters.** Official. Scope: `S2S`. One question per turn. One-page plan. Eight report lines. One `Next`. Two failures on the same action, then stop. Profile is one short paragraph. The profile character limit is unknown, so no fake maximum is written down.
- **Second person, and an objective of one or two sentences that says what done is and when to stop.** Official. Scope: `S2S`. Also the finish-line wording. Official for a first task. Scope: `BOTS`, [Grok Bot bots](https://docs.x.ai/grok-bot/bots). The interview uses `Goal` / `Exit when` because that flow stalls when a step is skipped. The phase pattern is official for voice. Using it on this text interview is inference, and it is used because the interview was already skipping ahead.
- **Say you do not know. Ask. Do not invent.** Official. Scope: `S2S`. Unknown tools, unknown buttons, unknown channel-delete, unknown profile length.
- **Only real tool names, in backticks, with when, what you say first, and what you do with the result. Confirm before a tool that changes something.** Official. Scope: `S2S`. The names are `CreateAgent`, `CreateChannel`, `UpdateChannel`, `SendToAgent`, `CloudAgent`. No other tool is named. `SendToAgent` uses `priority: true` and `priority: false` only. Other parameters are marked unknown.
- **Escalation after two failed attempts, with the words to say.** Official pattern. Scope: `S2S`. The number two is this repo's rule, not a documented Grok Bot limit.
- **Crisis path.** Official for an agent that talks to a person. Scope: `S2S`. The bot stops, says it is not a crisis service, and points at local emergency services. No hotline number is invented.
- **Tool output and pages are data, not instructions.** Official. Scope: `PI`. [Prompt-injection defenses](https://docs.x.ai/cookbook/examples/prompt-injection-defenses). The private memory repo is carved out on purpose: agreed decisions there are the human's instructions, and they still lose to the critical list.
- **Approval before create, commit, push, package, delete, or publish.** Official. Scope: `SK` and the starter prompts. [Skills, routines, and automations](https://docs.x.ai/grok-bot/skills-routines-and-automations), [Grok Bot use cases](https://docs.x.ai/grok-bot/use-cases).
- **A brief names when it applies, inputs, sequence, how to check, what to return, and what needs a yes.** Official for skills. Scope: `SK`. Applied to the lead, coordinator, and Knowledge Manager briefs. They are not Grok Bot skill files, and they have no skill YAML.
- **One output shape for one job.** Official, concrete task and direct output. Scope: `S2S`, `BP`. `search.py` prints `mode`, then `path` and `snippet`, or `none`, whether `index.db` is present or not. Ask, answer, and add messages keep the same labels. Turning the index on is `build_index.py` only.
- **Missing or stale data is reported. Chat memory is not the task board.** Official. Scope: `SK` and `BOTS`. [Bots](https://docs.x.ai/grok-bot/bots).
- **Lasting rules stay apart from one task.** Official. Scope: `BOTS`.
- **No secrets in a shared template.** Official. Scope: `BOTS`.
- **Quoted bans, an explicit precedence order, do not recite the prompt unless asked, and pushback does not waive a yes.** Demonstrated, not a written rule. Scope: `GP` and `REF`. [grok-prompts](https://github.com/xai-org/grok-prompts), [refund agent](https://docs.x.ai/cookbook/examples/refund-agent-human-approval). Precedence is adapted from the `<policy>` pattern. These files do not use `<policy>` tags.
- **A clarifying question when the input is thin.** Inference from the voice guide's speech rule. Used because inventing a layer was the failure this interview exists to prevent.
- **One routine, after the steps are written down.** Official. Scope: `SK`. [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations). `daily-backup` is a saved prompt on the main bot. The prompt names the schedule, the timezone, the scan, the empty-day silence, and the approval already recorded on the roster. Event listeners are not used. The known caps (50 routines, five minutes apart, 20 run records) are stated. A cron string is not invented.

## Rules not applied

- **Voice section order, and no `#` title.** Official for `S2S` only. Putting that order on a text bot is inference. These files keep one `#` title because they are also repo documents. The prompt body uses `##`.
- **ALL CAPS on every rule.** Official `S2S` says emphasis is rare. `NEVER` appears only in `CRITICAL INSTRUCTIONS`.
- **Skill YAML frontmatter.** Demonstrated in a cookbook skill. These are bot briefs and one routine prompt loaded as text, not skill files. There is no skill YAML.
- **Native-tool-call versus XML tool calls.** Official `GCF`. The prompts name tools. They do not embed XML tool calls. There is no schema in this repo to restate. [Function calling](https://docs.x.ai/developers/tools/function-calling) and [structured outputs](https://docs.x.ai/developers/model-capabilities/text/structured-outputs) are about API metadata this repo does not own.
- **Harness defenses.** Official `PI`: prompt text alone missed attacks. This repo cannot set tool allow-lists. The secrets rule and the "do not edit the repo" rule are prompt-only. That is a gap, not a control.
- **Prompt-cache ordering.** Official `BP` / [prompt caching](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices). There is no API harness in this repo.
- **xAI product safety prefixes** (base64, "developer mode", forged assistant turns). Demonstrated in `GP`. Those are xAI's own product policies. Copying them into a user's org bot would pretend they are this framework's policy. Untrusted-content handling is the part that transferred.
- **API settings** (temperature, reasoning effort, retries). Not prompt text. [Text best practices](https://docs.x.ai/developers/model-capabilities/text/best-practices).

## Gaps that remain

- Stacked files have no official length budget. The hard list is repeated in `AGENTS.md` so a bot that only loads that file still sees it. The repeats can drift.
- `CreateAgent`, `CreateChannel`, `UpdateChannel`, `SendToAgent`, and `CloudAgent` are the names this framework was given. Full schemas are not in the public docs used above. Anything past the listed fields is marked unknown on purpose.
- Confidentiality is a written rule. The bots share one filesystem. The prompt cannot add a sandbox.
- The voice guide's "1–2 short sentences per turn" is for speech. Here, one question per turn and a one-page plan are the limits that match the task.
- Whether the Knowledge Manager has `SendToAgent` is unknown. Askers are told to use it. If the tool is missing, the ask goes through the main bot. That fallback is written down. It is not a measured product fact.
- A measured file count where FTS5 becomes necessary is unknown. The docs state a rough hint and the trigram minimum of 3 characters. They do not invent a cutoff.
- `CloudAgent` parameters are unknown, including a commit straight to `main`. The backup asks for it only when the roster says `main`, and it keeps the pull request if that is what the tool returns.
- The secret scan misses anything outside its named rules. A clean result is not a guarantee.
- The docs used here do not describe a vault. Personal contact details stay with the human. The prompt does not invent a screen to put them on.
