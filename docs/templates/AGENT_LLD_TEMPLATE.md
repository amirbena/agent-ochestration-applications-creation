# &lt;Agent Name&gt; — Low-Level Design

Use this template for `docs/agents/<agent-name>/LLD.md` after the matching HLD's
high-level boundaries are approved. The LLD is for humans first and Agents second. Prefer
tables, bullets, compact diagrams, trees, and short examples. Link
canonical policies rather than copying them. Keep a section brief or write `None` / `N/A`
when it genuinely does not apply.

The LLD owns **implementation design**: enough detail to begin building the Agent Skill
without rediscovering its architecture. It stops before implementation and is not code,
command output, a chronological research log, or a file-by-file execution diary.

## Design Context

- **HLD:** `<relative link to HLD.md>`
- **Approved assumptions used here:** <implementation-relevant assumptions only>
- **Constraints:** <portable-Skill, repository, contract, or compatibility constraints>

Do not repeat the HLD. If this design changes a high-level assumption, update and
re-approve the HLD instead of contradicting it here.

## Proposed Directory Structure

Include only resources this Agent needs; do not create empty directories for symmetry.

```text
agents/<agent-name>/
  README.md
  SKILL.md
  metadata/
  policies/
  runbooks/
  templates/
```

Annotate non-obvious paths and omit irrelevant ones.

## SKILL.md Contract

| Concern | Proposed definition |
| --- | --- |
| Role | <stable responsibility> |
| Primary workflow | <entry, core work, result> |
| Authority | <decisions owned> |
| Boundaries | <decisions owned elsewhere> |
| Stop conditions | <conditions requiring stop/report/escalation> |
| Operational sources | <Agent-local policies, runbooks, and templates loaded> |

Describe the contract; do not draft the full final `SKILL.md` unless a specific passage
is necessary to settle the design.

## Metadata and Capabilities

| Field / capability | Purpose | Required? |
| --- | --- | --- |
| <declarative item> | <why consumers need it> | <Yes / No> |

Keep metadata runtime-neutral. Do not encode a vendor's worker or tool model.

## Assignment Contract

| Input | Required? | Authority / ownership assumption | Validation / blocker behavior |
| --- | --- | --- | --- |
| <input> | <Yes / No> | <source and authority> | <acceptance check or response when missing> |

Cover required and optional inputs, relevant product/architecture context, repository or
scope ownership, validation expectations, and blockers. Add sample YAML/JSON only when
it materially clarifies a non-obvious shape.

## Result Contract

| Result element | Meaning | Consumer requirement |
| --- | --- | --- |
| Status | <statuses and distinctions actually needed> | <how the coordinator acts> |
| Outputs | <artifacts or decisions> | <location or consumption> |
| Changes / evidence | <traceability evidence> | <minimum useful detail> |
| Blockers / findings | <when relevant> | <owner and follow-up> |
| Validation | <executed, failed, not run, or not applicable> | <required evidence/reason> |
| Follow-up | <remaining work> | <routing expectation> |

## Policies

Identify portable, Agent-local normative behavior that belongs under
`agents/<agent-name>/policies/`. Repository-development rules remain canonical under
`/policies/` and should be linked in this design, not copied into the future Skill.

| Proposed policy | Behavior it owns | Why `SKILL.md` alone is insufficient |
| --- | --- | --- |
| <path or None> | <normative behavior> | <reuse or separation rationale> |

## Runbooks

Add a runbook only for a repeated operational workflow, not one-off behavior.

| Proposed runbook | Trigger | Outcome / stop condition |
| --- | --- | --- |
| <path or None> | <repeatable situation> | <result> |

## Templates

Identify reusable assignment, result, or artifact shapes. Avoid a generic abstraction
until real repetition exists.

| Proposed template | Consumer | Reused shape |
| --- | --- | --- |
| <path or None> | <consumer> | <what is standardized> |

## Internal Workers / Subagents

Document workers only where they materially improve execution. Preserve the model:

```text
Agent = stable role
Skill = portable operational definition
Subagent / worker = internal execution mechanism
```

| Candidate worker | Bounded task | Ownership / aggregation rule |
| --- | --- | --- |
| <worker or N/A> | <independent internal work> | <Agent retains external accountability> |

Workers stay hidden from the Team Lead contract unless a compelling, approved contract
reason requires otherwise.

## Workflow / State Model

Use a compact state diagram or transition table only when the Agent has meaningful
states. `N/A` is valid; do not add a state machine for template symmetry.

| State | Entered when | Allowed next state(s) | Required evidence / action |
| --- | --- | --- | --- |
| <state> | <condition> | <state(s)> | <action or output> |

## Validation

Define how correctness of the future Skill will be proven, including structural or
contract validation where appropriate.

| Validation | Proves | Failure behavior |
| --- | --- | --- |
| <check> | <property or contract> | <block, fail, warn, or escalate> |

## Repository Integration

Describe integration with the Team Lead, relevant Agents, repository validator, and
future packaging/distribution only where applicable. Preserve authority and the boundary
between root repository policy and portable Agent behavior.

| Integration point | Contract / dependency | Ownership impact |
| --- | --- | --- |
| <system or role> | <interface> | <owner and coordination requirement> |

## Test Strategy

Describe future tests; do not implement them during research/design.

- **Structural / contract tests:** <required files and stable semantic markers>
- **Behavioral scenarios:** <success, blocker, failure, and boundary cases>
- **Portability checks:** <runtime-neutral and standalone-package properties>
- **Regression protection:** <existing behavior that must remain unchanged>

## Implementation Sequence

Provide roughly 3–8 coherent steps, ordered by dependencies. Describe outcomes, not
shell commands or a chronological diary.

1. <first implementation outcome>
2. <next coherent outcome>
3. <validation and integration outcome>

## Migration / Compatibility

| Existing surface | Impact | Compatibility / migration action |
| --- | --- | --- |
| <surface or None> | <change or N/A> | <action> |

## Remaining Implementation Questions

Only include questions whose answer materially changes implementation.

| Question | Implementation impact | Owner / resolution point |
| --- | --- | --- |
| <question> | <files, contracts, tests, or sequence affected> | <owner> |
