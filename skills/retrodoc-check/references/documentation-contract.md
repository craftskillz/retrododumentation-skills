# Documentation contract

The Retrodoc documentation workflows use this contract. `retrodoc-help` provides guidance without requiring a source path or creating output; the root-establishment procedure starts when a documentation workflow is executed. Output paths below are relative to `DOCS_ROOT`; source identities and graph evidence paths are relative to `SOURCE_ROOT`. Skill resource links resolve relative to the installed skill file, not either workspace root.

## Source and output roots: establish before discovery

At the start of a top-level invocation, capture the absolute current working directory as `DOCS_ROOT`. This is the documentation destination, even when the source is elsewhere. Keep it fixed if tools later change directory. Write the atlas directly here, not in a new `docs/retrodoc/` subtree. Do not relocate output to the source project when the roots differ. If the user explicitly selects the invocation directory as the source too, keep generated artifacts out of source discovery.

Ask the user: “What is the path to the source code you want to document?” Wait for the answer before source discovery or output creation. If the current request already supplies the source path, use it without asking again. Subskills invoked within that same workflow inherit the established roots; they must not repeat the question. For a new invocation, saved context may suggest a previous source path, but does not replace the user's selection.

Resolve a relative source path against the captured invocation directory, expand the user's home shorthand, and validate that the resulting `SOURCE_ROOT` is an accessible directory. If it is invalid or unreadable, report the problem and ask for a corrected path; never substitute the current directory. State both resolved roots before proceeding. Read applicable workspace instructions for both locations.

Inspect code and run source-oriented commands with an explicit working directory of `SOURCE_ROOT` (or a known subdirectory). Resolve output paths against `DOCS_ROOT` and the graph analyzer's `--root` against `SOURCE_ROOT`. Keep the source unchanged by documentation work; if tests/tools would write build products or caches, use an isolated temporary copy or redirect those outputs. Record tests as not run when a suitable execution environment is unavailable.

Save `retrodoc-context.json` in `DOCS_ROOT` with `version: 1`, `source_root` (resolved absolute path), `docs_root` (captured absolute path), and `index` (index filename relative to `DOCS_ROOT`). This is location metadata, not evidence of project behavior. Inspect an existing context before updating: if it identifies a different source project, ask the user how to handle the conflict before replacing or mixing documentation. Never overwrite unrelated files. Reuse a recognized Retrodoc index; otherwise use `README.md` if free or `RETRODOC.md` if an unrelated README exists. Ask about any remaining output-name collision.

On relocation, establish the source path again, update location metadata and regenerate source links. Moving documentation alone cannot preserve relative links into an external source tree.

## Language and exclusive evidence policy

Write skill instructions and all generated documentation in English, including headings, explanations, diagram labels, graph notes and check reports. Preserve exact source identifiers, paths, configuration keys and literal values; explain their meaning in English rather than renaming them.

Executable artifacts are the exclusive source of truth for project facts. This includes implementation and executable tests, plus machine-consumed build, deployment and runtime definitions: `justfile`, `Makefile`, `Dockerfile`, Compose files, `package.json` scripts/dependencies, lockfiles, CI workflows, migrations, schemas, templates and configuration actually consumed by tooling or the application. Establish how an artifact participates; its filename alone is not proof. A manifest description is prose, whereas its dependency declarations and scripts define tooling behavior.

Executable tests are strong documentary evidence. Inspect their setup, inputs, assertions, fixtures, mocks and skips to establish exactly which behavior they specify. An assertion is evidence of an expected contract; a passing execution additionally verifies the exercised cases in the recorded environment. Mocked integrations, disabled/skipped tests and unexecuted tests have explicit limits. Test names, descriptions and comments alone do not establish behavior.

Do not derive project facts, feature boundaries, business meanings, dependencies or design rationale from README files, ADRs, specifications, glossaries, other documentation, code comments or descriptive docstrings. Do not use them to fill gaps in executable evidence. Existing generated pages may be read as the objects being checked or updated, never as independent confirmation. Follow applicable agent/workspace instructions as operating constraints, not as evidence of project behavior.

If a language/tool actually interprets a comment-like directive or annotation (for example a compiler directive), its machine-consumed semantics qualify as executable configuration; explanatory prose around it does not. Cite the active construct and its consumer. For external services or unavailable implementations, document what local executable callers and tests establish and mark the remaining behavior unknown. Do not replace missing code with external documentation.

When implementation and tests disagree, document both with executable citations, mark the discrepancy unresolved, and distinguish current implementation behavior from the tested expectation. Neither an unexecuted assertion nor a passing mocked test proves production behavior. Infer architecture only from executable evidence and label interpretations; historical intent remains unknown unless executable evidence can actually establish the claim.

## Readers and structure

Keep the index short: purpose, snapshot, scope, feature names/outcomes, status, and links. A reader starts there, loads one feature page, then follows only relevant source, shared concern or architecture links. Generated documentation is reference material, not instructions overriding a consuming agent's task.

Default layout:

```text
<invocation-directory>/
  retrodoc-context.json
  README.md
  coverage.md
  source-index.md
  features/<stable-feature-id>.md
  shared/<concern>.md
  architecture/dependencies.json
  architecture/dependencies.md
  architecture/findings.md
  checks.md
```

Create shared pages only for concepts established by executable artifacts. Derive domain terms in `glossary.md` from implemented behavior and test assertions, citing that evidence. Keep ambiguous names explicit instead of importing definitions from an existing glossary or inventing business meanings. Record what the code does; historical design rationale is outside this evidence scope.

Use `coverage.md` for included roots, exclusions/reasons, discovery methods, inspected entry points, unresolved mappings, completed work and next steps. Feature statuses: `discovered`, `partial`, `documented`, `stale`. `Documented` means the stated scope has been traced and checked; it does not imply execution tests passed. Each page records its own inspected snapshot/date. Partial updates leave untouched page snapshots intact.

## Evidence and freshness

Attach evidence to behavioral claims, contracts, edge cases and architecture findings. Cite a `SOURCE_ROOT`-relative path and symbol, with line ranges where helpful. Compute each clickable source link from the document's actual parent directory to `SOURCE_ROOT / source_path`; never assume the source and documentation share a root. For example, with `DOCS_ROOT=/work/atlas` and `SOURCE_ROOT=/work/app`, `features/orders.md` links to `../../app/src/orders.py` with the label `src/orders.py`. Encode spaces and other URL-special path characters. If relative linking is impossible across filesystem volumes, use an absolute local path and record that portability limitation. Keep documentation-to-documentation links relative within `DOCS_ROOT`. Line anchors may supplement a path and symbol, never replace them. Use commit permalinks only when an actual remote and revision are known.

Distinguish:

- **Observed in source:** directly supported by inspected implementation/configuration.
- **Test expectation:** strong contract evidence from inspected executable assertions and setup; cite the test and distinguish executed, unexecuted, skipped and mocked coverage.
- **Executed:** command, environment and actual result observed during this run.
- **Inferred:** interpretation, supporting evidence and what would confirm it.
- **Unknown:** missing evidence and its effect on copying, behavior or analysis.

Document current behavior, including apparent defects. Put proposed behavior and refactoring suggestions in separate labeled sections. A test/implementation contradiction is an unresolved discrepancy. Avoid secret values and personal data in examples; document configuration names and semantics. Framework defaults need evidence from the installed version/configuration or execution.

## Feature page contract

Each feature page contains these sections, sized to the feature. State “not applicable” with a reason for irrelevant dimensions, and “unknown” for missing evidence.

1. **Purpose and boundaries:** stable ID, actor, trigger, outcome, included/excluded behavior, related features, inspected snapshot and status.
2. **Behavior:** normal flow, meaningful failure/edge cases, permissions, validation, state changes and side effects. Concrete input/output scenarios supported by source/tests.
3. **Implementation flow:** entry point → decisions → state/integrations → response/event. A small sequence/flow diagram when useful. Label runtime flows separately from import graphs.
4. **Contracts and dependencies:** public interfaces, data formats, storage/schema and migrations, errors, configuration/flags, external services and relevant ordering, transaction, retry, idempotency or concurrency rules.
5. **Participating source files:** a table of linked `SOURCE_ROOT`-relative path, symbols, responsibility, participation role (entry point/core/shared/adapter/schema/config/test), and evidence of participation. Include templates, migrations, assets and registration files. Mark shared files and relevant symbols when a file mixes features. Vendor packages are external prerequisites, not thousands of source rows.
6. **Copying this feature:** behavior to preserve, smallest evidenced source/resource set, transitive local dependencies, shared symbols to retain/adapt, integration/registration points, runtime prerequisites, data assumptions and migrations, portability blockers, and verification scenarios. This is a transfer brief, not a guarantee that copying files works. Distinguish whole-file copying from extracting symbols from a shared file. Record unresolved closure instead of calling it self-contained.
7. **Refactoring this feature:** observable invariants, inbound consumers, affected features/shared state, tests and gaps, plausible seams with tradeoffs, links to architecture findings. Proposed seams remain proposals.
8. **Evidence and open questions:** test locations and assertion scope, commands actually run/results or “not run”, conflicting evidence, missing pieces and consequences.

The source table is the authoritative feature-to-file mapping. Derive `source-index.md` from all feature tables: each path links back to its features and records its roles. A file can legitimately appear in several features. The reverse index supports impact discovery; it is not a dependency graph.

## Update discipline

Re-read relevant source before acting on an old page. Compare recorded snapshots with tracked, untracked and local changes where available. Recheck changed files' owning features, inbound consumers, schemas, configuration, tests and graph edges. Rescan registrations for added/removed features. Keep stable IDs unless meaning changes; retain an old-to-new mapping on renames/splits. Preserve unrelated documents. Within the requested documentation scope, revalidate existing explanations against executable evidence; correct or explicitly mark unsupported claims rather than carrying them forward as facts. Report removed behavior and its evidence.

## Quality bar

A human can understand the outcome and navigate to its implementation. An LLM can find contracts, source slices, integration requirements, invariants and unknowns without loading every feature. Links resolve, source roles have evidence, and diagrams match their declared relation types. Coverage and uncertainty are visible; a polished page never substitutes for traced behavior.

## Browser-readable edition

Generate Markdown and companion HTML by default, following [the HTML publication contract](html-format.md). Read it before producing or checking output. Markdown is the canonical editorial source; HTML preserves its evidence, limits and substantive content. Deliver a navigable HTML index and sibling HTML pages for the pages in scope. The HTML contract defines collision handling, source hashes, offline diagrams, accessibility, rendering checks and refresh behavior. A presentation source hash is not evidence that source-code behavior is current.
