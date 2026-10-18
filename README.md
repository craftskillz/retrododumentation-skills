# Refactoring Skills

A collection of skills for understanding and refactoring existing projects. The Retrodoc suite produces feature-oriented documentation grounded in executable code and tests, for humans and LLMs preparing to copy behavior or refactor implementations.

## Skills

| Skill | Use it for |
| --- | --- |
| [retrodoc-help](skills/retrodoc-help/SKILL.md) | Choose a workflow and learn how to start |
| [retrodoc](skills/retrodoc/SKILL.md) | Discover features first, or produce the complete documentation atlas |
| [retrodoc-feature](skills/retrodoc-feature/SKILL.md) | Trace one feature, its source files, contracts and transfer requirements |
| [retrodoc-architecture](skills/retrodoc-architecture/SKILL.md) | Build dependency evidence, draw diagrams and assess separation |
| [retrodoc-check](skills/retrodoc-check/SKILL.md) | Check accuracy, references and coverage; refresh when requested |

These skills describe the implemented system. They do not copy features, refactor application code or publish documentation. Their output provides the context for those later tasks.

## Install and invoke

Copy all five `skills/retrodoc*` directories together into the documentation workspace's `.agents/skills/` directory, retaining their sibling layout. Launch the agent in that workspace; the source project can be elsewhere. Inspect existing destinations before copying so you preserve any local customizations. They share a contract in `retrodoc/references/`; installing an individual companion without that folder leaves a missing dependency. Matt Pocock's collection is not a runtime dependency.

Example Codex prompts after installation:

```text
$retrodoc-help I do not know this project. Where should I start?
$retrodoc Document this project from source, organized by feature.
$retrodoc-feature Document checkout, including the source needed to copy its behavior.
$retrodoc-architecture Analyze the documented features for cycles and concentrated responsibilities.
$retrodoc-check Refresh the documentation against the current source.
```

You can also direct an agent to read `skills/retrodoc/SKILL.md` and follow it without installing. It must have access to the target source and permission to write the current invocation directory.

For example, launch Codex in `/work/project-atlas` and enter:

```text
$retrodoc Document the source code at /work/my-application.
```

The source is inspected under `/work/my-application`, while documentation is written directly under `/work/project-atlas`. With just `$retrodoc`, the skill asks for the source path first. Companion skills follow the same rule when invoked independently; within a full run, they reuse its established roots.

## Start with an unfamiliar project

You do not need to know the feature names. To inspect the inventory before committing to full documentation, use:

```text
$retrodoc Discover features in /work/my-application first and let me choose which ones to document.
```

Discovery writes an index, `coverage.md` and location metadata in the current directory. It lists feature IDs, outcomes, executable entry points and uncertainties, then waits for your selection. It does not generate detailed feature pages or architecture findings yet.

For complete documentation, `$retrodoc Document the entire project` discovers features and continues automatically. Use `$retrodoc-feature` to deepen a selected feature; without a selection, it presents the existing inventory or offers discovery if none exists. `$retrodoc-help` explains these choices without starting analysis.

## Generated documentation

The atlas is written directly into the invocation directory, with `features/`, `architecture/`, indexes and checks. `retrodoc-context.json` records the source and documentation roots. An existing unrelated README is preserved by using `RETRODOC.md` for the index.

Documentation is in English, using Markdown, Mermaid diagrams and a JSON dependency graph. The skills work across programming languages, using the agent and available stack-specific tools to inspect source.

Each feature page contains:

1. Purpose and boundaries.
2. Current behavior, including failures and edge cases.
3. Implementation flow.
4. Interfaces, data and dependency contracts.
5. **Participating source files**, with linked paths, symbols, roles and evidence.
6. Copying guidance: required source/resources, integration points, shared dependencies and blockers.
7. Refactoring guidance: invariants, consumers, affected features and verification.
8. Evidence, execution status and open questions.

Source tables retain source-root-relative file identities and compute clickable links from the actual documentation location. Moving either tree requires refreshing those links. A feature index provides navigation. A reverse source index maps files back to every feature they participate in. Coverage records disclose uninspected areas and support continuing large projects across sessions. Domain terminology is derived from implementation and executable tests, not from existing glossaries or decision documents.

## Evidence policy

All skills and generated documentation are in English. Preserve literal source identifiers, paths and configuration keys.

Project facts come exclusively from executable artifacts: application code, executable tests, scripts, `justfile`, `Dockerfile`, `package.json` scripts/dependencies, CI workflows, schemas, migrations and machine-consumed configuration. README files, ADRs, specifications, glossaries, comments and descriptive docstrings are not factual evidence. Existing documentation is only material to verify/update; applicable agent instructions remain operating constraints.

Executable tests provide strong documentary evidence through their actual assertions and setup. Record whether they were run, skipped or mocked. A passing test verifies the exercised cases in its environment; an unexecuted assertion specifies an expectation. Document disagreements between tests and implementation explicitly. Missing executable evidence stays unknown.

## Architecture analysis

The [graph format](skills/retrodoc-architecture/references/graph.md) separates imports, types, calls, events, data and configuration relationships. The analyzer checks supplied evidence locations, computes cyclic strongly connected components, renders a typed Mermaid view, and reports incoming/outgoing dependency and feature-participation counts.

```sh
python3 skills/retrodoc-architecture/scripts/analyze_graph.py \
  /path/to/documentation/architecture/dependencies.json \
  --root /path/to/project --kind import
```

It requires Python 3.9 or newer and only the standard library. It does **not** extract dependencies from arbitrary source languages or verify the meaning of citations. The agent performs that work, records resolution limitations, and inspects candidates before making architectural claims. Shared files are not automatically god objects; cycles are not automatically defects. Suggested changes remain separate from observed architecture.

## Validation

```sh
python3 -m unittest discover -s tests -v
```

Tests exercise cyclic groups, self-loops, non-cyclic tails, typed-edge isolation, shared participation, invalid evidence, CLI behavior, label escaping and long graphs.

These tests validate the analyzer, not the completeness or accuracy of LLM-generated documentation. Evaluate the workflow on a familiar feature before applying it across a large project.

## Design origins

Retrodoc draws on concepts from Matt Pocock’s `mattpocock/skills` collection:

- `writing-for-agents`: progressive disclosure, clear completion criteria and one authoritative home for each fact.
- `domain-modeling`: consistent domain vocabulary and explicit contexts, adapted here to derive meanings exclusively from executable artifacts.
- `codebase-design` and `improve-codebase-architecture`: interfaces, responsibility placement and testable seams.
- `research` and `diagnosing-bugs`: primary evidence and separation of hypotheses from observed results.
- `tdd`, `to-tickets` and `handoff`: observable behavior, vertical traces and resumable context.
- `code-review`: separate structural compliance from behavioral accuracy.

OpenAI's bundled `skill-creator` informed packaging, metadata, scope and validation. Retrodoc adapts these ideas to retrospective documentation, with explicit source references, snapshot tracking and refresh checks. Neither collection is required at runtime. No issue tracker, external service or multi-agent execution is required.
