# CLAUDE.md

This repository uses [AGENTS.md](AGENTS.md) as the canonical, repository-wide agent
instruction source. Read it first, follow its **Task Routing** table into the relevant
[policies/](policies/) file for your task, and then, when operating as a specialized
Agent (e.g. the Backend Agent), read that Agent's `SKILL.md` and its applicable
policies, runbooks, templates, and metadata under `agents/<agent>/`.

This file is a bootstrap only. It does not define, duplicate, or override any
repository-wide rule. If anything here ever conflicts with `AGENTS.md`, `AGENTS.md` wins.
