# Retrodoc help

Help the user choose a workflow without requiring prior knowledge of the project's features. This skill provides guidance; it does not start source analysis, create documentation or require a source path merely to explain usage. Keep skill instructions and copyable prompts in English; conversational guidance can follow the user's language.

## Understand the need

Use the stated goal if clear. Otherwise ask one short question: whether the user wants to discover an unfamiliar project, document everything, deepen one feature, inspect architecture, or check existing documentation. Recommend discovery first when they want to understand the available features before choosing work.

Read the relevant linked procedure before explaining its detailed behavior. These bundled procedures are the authoritative workflow instructions, not evidence about any target project's behavior.

| User need | Workflow | Result |
| --- | --- | --- |
| Identify features before choosing | [retrodoc](retrodoc.md), discovery only | Evidence-backed inventory, coverage and a selection of features |
| Plan documentation of the whole project | [retrodoc](retrodoc.md), default planning pass | Feature inventory and self-contained tickets for fresh sessions |
| Execute one planned ticket | [retrodoc](retrodoc.md), ticket execution | One checked slice and a durable handoff |
| Continue a previous run in a new session | [retrodoc](retrodoc.md), workspace recovery | Saved roots and unfinished/next ready ticket, recovered from the documentation directory |
| Complete the whole atlas across sessions | [retrodoc](retrodoc.md), ticket workflow | Planning, one ticket per fresh context, then separate integration/check tickets |
| Document a selected behavior | [retrodoc-feature](retrodoc-feature.md) | Behavior, participating files, copy prerequisites and refactoring invariants |
| Prepare a feature for copying, with runtime evidence | [retrodoc-feature](retrodoc-feature.md) plus the opt-in [runtime evidence pass](../runtime-evidence.md) | The dossier plus screenshots, executed checks and an acceptance spec, produced in an isolated copy of the application |
| Inspect dependencies and separation | [retrodoc-architecture](../../SKILL.md) | Typed graphs, evidenced cycles and qualified responsibility findings |
| Verify or refresh documentation | [retrodoc-check](retrodoc-check.md) | Accuracy/coverage report; documentation updates when requested |

Explain that project-wide planning discovers features automatically; each resulting ticket runs in a fresh conversation, separate from planning and other tickets. A whole-project request keeps that session boundary. Explain that the agent provides a durable handoff and next-session prompt instead of silently continuing the queue. Read [the ticket workflow](../ticket-workflow.md) for phase and handoff details. A feature request can use an observable behavior or entry point instead of an internal feature name. With no feature specified, `retrodoc-feature` offers inventory choices; without an inventory, it offers discovery first.

## Give the next prompt

Provide one recommended prompt matched to the goal, not every possible command. Recommend a named companion invocation only when that companion is installed. When only this skill is available, give a prompt such as `$retrodoc-help Run the bundled discovery-only workflow and let me choose features`; execute the linked local procedure after that request. Do not require installing a companion to use its bundled procedure. The following examples apply when the named skill is installed:

```text
$retrodoc Discover the features first and let me choose which ones to document.
$retrodoc Plan the documentation tickets for this project.
$retrodoc Execute only tickets/RD-001.md.
$retrodoc Continue the existing documentation.
$retrodoc Plan the complete atlas; I will execute each ticket in a fresh conversation.
$retrodoc-feature Help me select a feature from the inventory to document.
$retrodoc-feature Document checkout for copying, with the runtime evidence pass.
$retrodoc-architecture Analyze dependencies and responsibility concentration.
$retrodoc-check Check the documentation against current executable artifacts.
$retrodoc-check Refresh the documentation against current executable artifacts.
```

Mention the two-location model: execution restores valid saved roots, uses an explicitly supplied source path, or asks for one when neither is available. It writes documentation directly into the invocation directory; the source can be elsewhere. In a fresh conversation from an existing documentation directory, bare `$retrodoc` resumes an unfinished ticket or selects the next ready ticket, then stops after that ticket. Output is English; factual evidence comes exclusively from executable artifacts and tests, not ADRs, prose documentation or explanatory comments. Read [the contract](../documentation-contract.md) if the user needs details about evidence, paths or output structure.

Conclude guidance once the user has a recommended workflow, an explanation of its result and a usable prompt. If they ask to execute that workflow, read and follow the selected bundled procedure, establish its roots once and honor the chosen mode. A request for help alone does not authorize a full documentation run.

## Browser reading

Explain that executed documentation workflows produce both canonical Markdown and a navigable, offline HTML edition. Read [the HTML publication contract](../html-format.md) when explaining presentation or refresh behavior. Help alone still creates no files.
