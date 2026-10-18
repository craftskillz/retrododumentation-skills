# Document a feature

Read [the documentation contract](../documentation-contract.md), including its English-language and exclusive executable-evidence policy, before tracing the feature. It can run without an existing atlas by creating a minimal index for the requested scope.

When invoked for a Retrodoc ticket, inherit its selected scope and validated roots, follow [the ticket execution and handoff rules](../ticket-workflow.md), use a fresh conversation for that ticket, and stop after its handoff. Additional tickets require additional fresh contexts. A ticket is not evidence: re-read its executable source leads before accepting claims.

Before discovery, follow the contract's source/output root procedure: capture the invocation directory as `DOCS_ROOT` and ask for the source path unless supplied in the request. In a parent Retrodoc workflow, inherit its validated roots without asking again. All documentation is written directly under `DOCS_ROOT`; source inspection uses `SOURCE_ROOT`.

## Select the feature

Accept a feature ID/name, an observable behavior, or an entry-point reference; an exact internal name is not required. A feature selected by the parent workflow already satisfies this step.

If the user supplies no feature, inspect the inventory in `DOCS_ROOT` after establishing the source root. Use it as a navigation aid only: verify its source identity and candidate entry points against current executable artifacts before presenting choices. Show stable IDs, short outcomes and statuses, then ask which feature or subset to document. Wait for the selection; do not choose an arbitrary feature or ask the user to invent names.

If no usable inventory exists, explain that discovery identifies features from code and offer to run [retrodoc in discovery-only mode](retrodoc.md). If the user already requested discovery, proceed; otherwise wait for acceptance. Reuse the established roots, produce the inventory, and let the user select from it before returning here. If discovery finds no supported candidates, report the inspected scope and gaps rather than inventing a feature list.

For an ambiguous feature request, present concrete executable-backed matches and ask the user to choose. Once selected, continue with the trace below.

## Trace and document

1. Locate the capability using implemented operations, registration points, callers and executable test assertions. Derive domain terms from those artifacts; exclude glossaries, ADRs, documentation, comments and descriptive docstrings as evidence. If unrelated capabilities match, show concrete candidates and ask which one; continue collecting facts common to them.
2. Follow implementation from trigger through decisions, state and side effects to outcome. Inspect failure branches, authorization and configuration gates. Trace registrations and dependency injection as well as direct calls. Follow important indirect dependencies until reaching an inspected local implementation, an external interaction established by local executable code/tests, or a recorded unknown.
3. Build the participating-files table as you trace. Include shared symbols, schema/migration, assets, registration and tests; explain each role. Filenames and imports alone do not prove participation in a particular behavior.
4. Write the page using all eight contract sections. Separate behavior from implementation so a refactoring agent knows what must remain stable. Derive the copy brief from dependency closure, including resources and environment requirements. Trace inbound consumers for refactoring impact. Record uncertainty where source access ends.
5. Update the feature index and reverse source index, preserving other feature rows. Add observed dependencies to an existing architecture dataset when its schema is available; otherwise retain evidence in the page for later analysis. Check every source link and material behavioral assertion against inspected files.

Done when all sections are substantive, every listed file has a role and evidence, and readers can distinguish verified behavior from transfer assumptions. Report inspected scope and test execution status. Do not implement suggested changes during documentation.

## Publish the local reading edition

Follow [the HTML publication contract](../html-format.md) and its bundled CSS for canonical Markdown plus sibling HTML pages. Refresh the HTML atlas navigation for pages actually produced. Preserve all evidence and unknowns; label future-state diagrams as proposals. Validate the reading edition and return both entry points. Discovery-only scope remains an inventory and coverage, without feature placeholders.
