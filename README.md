# Refactoring Skills

A collection of skills for understanding and refactoring existing projects. The Retrodoc suite produces feature-oriented documentation, written from the outside in: features are discovered from what users interact with (UI screens, otherwise APIs or CLI commands), documented functionally first, then enriched from source code, questions to the user and optional Playwright runs. It is meant for humans and LLMs preparing to copy behavior or refactor implementations.

## Skills

| Skill | Use it for |
| --- | --- |
| [retrodoc-help](skills/retrodoc-help/SKILL.md) | Choose a workflow and learn how to start |
| [retrodoc](skills/retrodoc/SKILL.md) | Plan source-backed documentation tickets, then execute them in bounded sessions |
| [retrodoc-feature](skills/retrodoc-feature/SKILL.md) | Document one feature functionally, then enrich it with source files, contracts and transfer requirements |
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

Discovery first inventories the interaction surfaces in `surfaces.md`: UI screens first, then public APIs, CLI commands and system triggers. It then groups them into features using signals visible to users: a shared menu or route prefix, the same business object, a journey from one screen to the next, shared vocabulary and shared permissions. Where signals conflict, it asks you. It writes an index, `surfaces.md`, `coverage.md` and location metadata in the current directory, lists feature IDs, outcomes, surfaces and uncertainties, then waits for your selection.

Discovery reads the source by default. Only when the source cannot list the screens (navigation built from server data, a remote configuration, a minified-only build) does it fall back to a read-only Playwright crawl, and then it asks you to start the application and give its URL rather than starting it itself. It does not generate detailed feature pages or architecture findings yet.

In a new workspace, `$retrodoc` or a project-wide documentation request discovers features and writes a two-wave ticket queue, then stops after that planning pass. In a fresh session from the same documentation workspace, run `$retrodoc` again: it resumes the sole `in_progress` ticket, or uses the saved `next_ticket` when ready, falling back to the first ready ticket whose dependencies are satisfied. It completes that one ticket and saves its handoff. You can still pin a ticket with `$retrodoc Execute only tickets/RD-001.md`. The planning session stops before ticket execution. A request to complete the whole project still uses one fresh conversation per ticket, including the architecture and final validation tickets. Use `$retrodoc-feature` to deepen a selected feature; without a selection, it presents the existing inventory or offers discovery if none exists. `$retrodoc-help` explains these choices without starting analysis.

Recovery reads location metadata, queue status and the selected ticket's handoff from disk; it does not need the earlier conversation. Completed queues report their status; blocked queues report missing prerequisites. Multiple unfinished tickets require a selection. Missing or conflicting roots require clarification before writing. Launch from the existing documentation directory so the skill can find these artifacts; a different working directory does not identify the previous run. Request a refresh or replan explicitly when you want to revisit the scope.

## Documentation passes

1. Inventory the interaction surfaces, group them into features, clarify only unresolved boundaries, and produce the inventory and local ticket queue.
2. Execute one selected ticket per fresh session, in two waves:
   - **Wave 1, functional:** one ticket per feature writes its functional page from the screens, forms, messages and routes, recording open questions without asking them. A **review** ticket then shows you the functional atlas and asks all open questions in one batch.
   - **Wave 2, enrichment:** one ticket per feature traces the source code, corrects the functional page, writes the technical page, asks the questions still open and, when requested, runs Playwright.

   For a functional-only atlas, ask for it at planning (`$retrodoc Plan a functional-only atlas of this project.`); wave 2 can be planned later.

   Every ticket carries roots, snapshot, scope, source/test leads, dependencies, exact outputs, acceptance criteria and a durable handoff. Re-read source and check drift on every resume.
3. Integrate architecture and indexes, then validate the complete Markdown/HTML atlas. Report unfinished or unresolved tickets explicitly.

Ticket completion is distinct from feature status and from runtime test success. Tickets do not authorize application changes or external issue creation. Each ticket ends with a durable handoff and the next fresh-session prompt. Reusing the same conversation, including after compaction, does not provide a fresh context. Reading only the selected ticket and required evidence bounds context growth; actual cost savings are not guaranteed. See the bundled [ticket workflow](skills/retrodoc/references/ticket-workflow.md).

## Generated documentation

The atlas is written directly into the invocation directory, with `tickets/` first, followed by `features/`, `architecture/`, indexes and checks as tickets are executed. `retrodoc-context.json` records the source and documentation roots. An existing unrelated README is preserved by using `RETRODOC.md` for the index.

Documentation is in English, using Markdown, Mermaid diagrams and a JSON dependency graph. The skills work across programming languages, using the agent and available stack-specific tools to inspect source.

A feature is a menu area or business object, for example "Orders" with its list, detail, creation and cancellation screens; the outcomes it offers are user journeys inside it. Each feature has two pages, plus extra pages (for example one per screen) when that keeps it readable.

The **functional page** (`features/<id>.md`) is written from the user's or caller's perspective, without implementation terms, so it can serve as a rebuild specification on any stack:

1. Summary: who uses the feature and the outcomes it offers.
2. Access: menu path, route, endpoint or command, and required roles.
3. Interface: screens with their regions, data, actions, forms, validation and states; or API operations; or CLI commands.
4. User journeys: normal, alternative and failure scenarios.
5. Business rules as the user experiences them.
6. User-facing messages, verbatim with their keys.
7. Open functional questions.

The **technical page** (`features/<id>/technical.md`) enriches it:

1. Implementation flow.
2. Interfaces, data and dependency contracts.
3. **Participating source files**, with linked paths, symbols, roles and evidence.
4. Copying guidance: required source/resources, integration points, shared dependencies and blockers, known defects not to replicate and, for user-facing features, the resolved presentation values.
5. Refactoring guidance: invariants, consumers, affected features and verification.
6. Evidence, execution status, user answers used and open questions.

Every question raised for you is logged in `questions.md` with an ID (`Q-NNN`) that pages cite, and a status (`open` or `answered`). You can also answer open questions by editing that file between sessions.

Source tables retain source-root-relative file identities and compute clickable links from the actual documentation location. Moving either tree requires refreshing those links. A feature index provides navigation. A reverse source index maps files back to every feature they participate in. Coverage records disclose uninspected areas and support continuing large projects across sessions. Domain terminology is derived from visible labels, implementation, executable tests and user answers, not from existing glossaries or decision documents.

## Evidence policy

All skills and generated documentation are in English. Preserve literal source identifiers, paths and configuration keys.

Project facts come from executable artifacts, which are the definitive source of truth: application code, executable tests, scripts, `justfile`, `Dockerfile`, `package.json` scripts/dependencies, CI workflows, schemas, migrations and machine-consumed configuration. README files, ADRs, specifications, glossaries, comments and descriptive docstrings are not factual evidence. Existing documentation is only material to verify/update; source instructions apply only within documentary scope.

Answers you give to the agent's questions are strong evidence, labeled `User-stated`. They settle what code cannot: feature boundaries, business meaning, intent, and whether a behavior is deliberate or a defect. When an answer contradicts the source code, the code wins: the page documents the implemented behavior and keeps your statement as an unresolved discrepancy. Development build/test gates, worklogs, commits and release routines do not automatically apply to read-only documentation.

Executable tests provide strong documentary evidence through their actual assertions and setup. Record whether they were run, skipped or mocked. A passing test verifies the exercised cases in its environment; an unexecuted assertion specifies an expectation. Document disagreements between tests and implementation explicitly. Missing executable evidence stays unknown.

Running the application is opt-in. When requested (for example `$retrodoc-feature Document checkout for copying, with the runtime evidence pass.`), the feature workflow runs an isolated copy of the inspected revision with synthetic data and neutralized side effects, then drives it with a scripted browser test. It records `Executed` results for open questions and writes screenshots and an executable acceptance spec under `features/<feature-id>/`, so the copy can be verified against the same spec. Scripted runs keep token cost low: logs and screenshots stay on disk and only failures are read. See the bundled [runtime evidence pass](skills/retrodoc/references/runtime-evidence.md).

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
- `domain-modeling`: consistent domain vocabulary and explicit contexts, adapted here to derive meanings from executable artifacts and user answers.
- `codebase-design` and `improve-codebase-architecture`: interfaces, responsibility placement and testable seams.
- `research` and `diagnosing-bugs`: primary evidence and separation of hypotheses from observed results.
- `tdd`, `to-tickets` and `handoff`: observable behavior, vertical traces and resumable context.
- `code-review`: separate structural compliance from behavioral accuracy.

OpenAI's bundled `skill-creator` informed packaging, metadata, scope and validation. Retrodoc adapts these ideas to retrospective documentation, with explicit source references, snapshot tracking and refresh checks. Neither collection is required at runtime. No issue tracker, external service or multi-agent execution is required.
