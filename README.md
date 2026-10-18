# Refactoring Skills

A collection of skills for understanding and refactoring existing projects. The Retrodoc suite produces feature-oriented documentation grounded in executable code and tests, for humans and LLMs preparing to copy behavior or refactor implementations.

## Skills

| Skill | Use it for |
| --- | --- |
| [retrodoc-help](skills/retrodoc-help/SKILL.md) | Choose a workflow and learn how to start |
| [retrodoc](skills/retrodoc/SKILL.md) | Plan source-backed documentation tickets, then execute them in bounded sessions |
| [retrodoc-feature](skills/retrodoc-feature/SKILL.md) | Trace one feature, its source files, contracts and transfer requirements |
| [retrodoc-architecture](skills/retrodoc-architecture/SKILL.md) | Build dependency evidence, draw diagrams and assess separation |
| [retrodoc-check](skills/retrodoc-check/SKILL.md) | Check accuracy, references and coverage; refresh when requested |

These skills describe the implemented system. They do not copy features, refactor application code or publish documentation. Their output provides the context for those later tasks.

## Install and invoke

Install through the [Skills CLI](https://github.com/vercel-labs/skills). Once the repository is published, run this in your documentation workspace:

```sh
npx skills@latest add craftskillz/retrododumentation-skills
```

The CLI provides skill selection, target-agent selection and installation options. Each of the five skills is independently installable: its supporting procedures, references and tools are included. You do not need to select the whole suite or install Matt Pocock's skills.

For example, install just the complete documentation workflow for Codex:

```sh
npx skills@latest add craftskillz/retrododumentation-skills --skill retrodoc --agent codex
```

To install the full suite for Codex and Claude Code:

```sh
npx skills@latest add craftskillz/retrododumentation-skills --skill '*' --agent codex claude-code
```

For a local checkout, use the absolute path to its `skills/` directory instead of the GitHub source. This also avoids discovering third-party skills you may have installed locally while developing this repository:

```sh
npx skills@latest add /path/to/refactoring-skills/skills --list
npx skills@latest add /path/to/refactoring-skills/skills
```

Launch your agent in the documentation workspace after installation; the source project can be elsewhere. The `$skill-name` examples below use Codex syntax; other agents may expose different invocation syntax. Installing a skill configures an agent, not its underlying model.

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

The source is inspected under `/work/my-application`, while documentation is written directly under `/work/project-atlas`. In a new workspace, bare `$retrodoc` asks for the source path. In an existing documentation workspace, it restores valid roots from `retrodoc-context.json` and resumes saved work. Companion skills use the same root recovery when invoked independently; within a full run, they reuse its established roots.

## Start with an unfamiliar project

You do not need to know the feature names. To inspect the inventory before committing to full documentation, use:

```text
$retrodoc Discover features in /work/my-application first and let me choose which ones to document.
```

Discovery writes an index, `coverage.md` and location metadata in the current directory. It lists feature IDs, outcomes, executable entry points and uncertainties, then waits for your selection. It does not generate detailed feature pages or architecture findings yet.

In a new workspace, `$retrodoc` or a project-wide documentation request discovers features and writes a ticket queue, then stops after that planning pass. In a fresh session from the same documentation workspace, run `$retrodoc` again: it resumes the sole `in_progress` ticket, or uses the saved `next_ticket` when ready, falling back to the first ready ticket whose dependencies are satisfied. It completes that one ticket and saves its handoff. You can still pin a ticket with `$retrodoc Execute only tickets/RD-001.md`. The planning session stops before ticket execution. A request to complete the whole project still uses one fresh conversation per ticket, including the architecture and final validation tickets. Use `$retrodoc-feature` to deepen a selected feature; without a selection, it presents the existing inventory or offers discovery if none exists. `$retrodoc-help` explains these choices without starting analysis.

Recovery reads location metadata, queue status and the selected ticket's handoff from disk; it does not need the earlier conversation. Completed queues report their status; blocked queues report missing prerequisites. Multiple unfinished tickets require a selection. Missing or conflicting roots require clarification before writing. Launch from the existing documentation directory so the skill can find these artifacts; a different working directory does not identify the previous run. Request a refresh or replan explicitly when you want to revisit the scope.

## Documentation passes

1. Discover executable entry points and capabilities; clarify only unresolved boundaries; produce the inventory and local ticket queue.
2. Execute one selected ticket per fresh session. Each ticket carries roots, snapshot, scope, source/test leads, dependencies, exact outputs, acceptance criteria and a durable handoff. Re-read source and check drift on every resume.
3. Integrate architecture and indexes, then validate the complete Markdown/HTML atlas. Report unfinished or unresolved tickets explicitly.

Ticket completion is distinct from feature status and from runtime test success. Tickets do not authorize application changes or external issue creation. Each ticket ends with a durable handoff and the next fresh-session prompt. Reusing the same conversation, including after compaction, does not provide a fresh context. Reading only the selected ticket and required evidence bounds context growth; actual cost savings are not guaranteed. See the bundled [ticket workflow](skills/retrodoc/references/ticket-workflow.md).

## Generated documentation

The atlas is written directly into the invocation directory, with `tickets/` first, followed by `features/`, `architecture/`, indexes and checks as tickets are executed. `retrodoc-context.json` records the source and documentation roots. An existing unrelated README is preserved by using `RETRODOC.md` for the index.

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

Project facts come exclusively from executable artifacts: application code, executable tests, scripts, `justfile`, `Dockerfile`, `package.json` scripts/dependencies, CI workflows, schemas, migrations and machine-consumed configuration. README files, ADRs, specifications, glossaries, comments and descriptive docstrings are not factual evidence. Existing documentation is only material to verify/update; source instructions apply only within documentary scope. Development build/test gates, worklogs, commits and release routines do not automatically apply to read-only documentation.

Executable tests provide strong documentary evidence through their actual assertions and setup. Record whether they were run, skipped or mocked. A passing test verifies the exercised cases in its environment; an unexecuted assertion specifies an expectation. Document disagreements between tests and implementation explicitly. Missing executable evidence stays unknown.

## Architecture analysis

The [graph format](skills/retrodoc-architecture/references/graph.md) separates imports, types, calls, events, data and configuration relationships. The analyzer checks supplied evidence locations, computes cyclic strongly connected components, renders a typed Mermaid view, and reports incoming/outgoing dependency and feature-participation counts.

```sh
python3 skills/retrodoc-architecture/scripts/analyze_graph.py \
  /path/to/documentation/architecture/dependencies.json \
  --root /path/to/project --kind import
```

The analyzer requires Python 3.9 or newer and only the standard library. It does **not** extract dependencies from arbitrary source languages or verify the meaning of citations. The agent performs that work, records resolution limitations, and inspects candidates before making architectural claims. Shared files are not automatically god objects; cycles are not automatically defects. Suggested changes remain separate from observed architecture.

## Rendering and ticket tools

Every bundle ships two more standard-library scripts so agents never improvise converters or generators:

```sh
python3 skills/retrodoc/scripts/render_html.py /path/to/documentation           # Markdown -> sibling HTML
python3 skills/retrodoc/scripts/render_html.py /path/to/documentation --check   # hashes, links, fragments, IDs
python3 skills/retrodoc/scripts/scaffold_tickets.py /path/to/documentation plan.json
```

The renderer reads optional `status`/`scope`/`snapshot`/`inspected` front matter, embeds the bundled CSS, rewrites documentation links to HTML, sanitizes inline SVG and skips unchanged pages. The scaffolder turns a disposable planning JSON file into ticket pages and queue rows, validates leads against the source root and never overwrites existing tickets.

## Development and validation

Edit `authoring/`, the canonical source for instructions, UI metadata, references and the analyzer. Generate and commit the installable `skills/` bundles:

```sh
python3 scripts/build_skills.py
python3 scripts/build_skills.py --check
python3 -m unittest discover -s tests -v
```

The generator rewrites links to local bundled resources and removes discovery metadata from supporting workflow documents. Only the five public `SKILL.md` entrypoints are exposed to installers. Shared procedures are maintained once in `authoring/`; generated copies are committed so consumers need no build step. Agents read supporting procedures on demand.

Run the real installer checks locally with:

```sh
RETRODOC_SKILLS_COMMAND="npx --yes skills@latest" python3 -m unittest discover -s tests -v
```

Without that variable, installer integration checks are skipped. CI installs `skills@latest` and runs them automatically. The checks discover exactly five skills, install each separately for Codex and Claude Code in both copy and symlink modes, and verify that installed resources are complete and all local links remain within the selected skill. Other agent targets are handled by the Skills CLI but are not covered by this integration suite.

Commit `authoring/`, generated `skills/`, `scripts/`, `tests/`, `.github/`, `.gitignore` and this README. Keep locally installed third-party skills and their lockfile out of the published repository.

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
