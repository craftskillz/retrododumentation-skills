---
name: retrodoc-help
description: Guide users through Retrodoc skill selection and explain discovery, feature documentation, architecture analysis and checks. Use when users do not know where to start or how the skills fit together.
---

# Retrodoc help

Help the user choose a workflow without requiring prior knowledge of the project's features. This skill provides guidance; it does not start source analysis, create documentation or require a source path merely to explain usage. Keep skill instructions and copyable prompts in English; conversational guidance can follow the user's language.

## Understand the need

Use the stated goal if clear. Otherwise ask one short question: whether the user wants to discover an unfamiliar project, document everything, deepen one feature, inspect architecture, or check existing documentation. Recommend discovery first when they want to understand the available features before choosing work.

Read the relevant linked skill before explaining its detailed behavior. These sibling skills are the authoritative workflow instructions, not evidence about any target project's behavior.

| User need | Workflow | Result |
| --- | --- | --- |
| Identify features before choosing | [retrodoc](../retrodoc/SKILL.md), discovery only | Evidence-backed inventory, coverage and a selection of features |
| Document the whole project | [retrodoc](../retrodoc/SKILL.md), full documentation | Discovery followed by feature dossiers, architecture analysis and checks |
| Document a selected behavior | [retrodoc-feature](../retrodoc-feature/SKILL.md) | Behavior, participating files, copy prerequisites and refactoring invariants |
| Inspect dependencies and separation | [retrodoc-architecture](../retrodoc-architecture/SKILL.md) | Typed graphs, evidenced cycles and qualified responsibility findings |
| Verify or refresh documentation | [retrodoc-check](../retrodoc-check/SKILL.md) | Accuracy/coverage report; documentation updates when requested |

Explain that full documentation discovers features automatically. A feature request can use an observable behavior or entry point instead of an internal feature name. With no feature specified, `retrodoc-feature` offers inventory choices; without an inventory, it offers discovery first.

## Give the next prompt

Provide one recommended prompt matched to the goal, not every possible command. Examples:

```text
$retrodoc Discover the features first and let me choose which ones to document.
$retrodoc Document the entire project, starting with feature discovery.
$retrodoc-feature Help me select a feature from the inventory to document.
$retrodoc-architecture Analyze dependencies and responsibility concentration.
$retrodoc-check Check the documentation against current executable artifacts.
$retrodoc-check Refresh the documentation against current executable artifacts.
```

Mention the two-location model: execution asks for the source path unless supplied, and writes documentation directly into the invocation directory. The source can be elsewhere. Output is English; factual evidence comes exclusively from executable artifacts and tests, not ADRs, prose documentation or explanatory comments. Read [the contract](../retrodoc/references/documentation-contract.md) if the user needs details about evidence, paths or output structure.

Conclude guidance once the user has a recommended workflow, an explanation of its result and a usable prompt. If they ask to execute that workflow, read and follow the selected skill, establish its roots once and honor the chosen mode. A request for help alone does not authorize a full documentation run.
