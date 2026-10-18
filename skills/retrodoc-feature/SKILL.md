---
name: retrodoc-feature
description: Document an existing feature from source, including participating files, behavior contracts, and copying or refactoring guidance. Use for a focused feature dossier, not implementing the copy or refactor.
---

# Document a feature

Read [the documentation contract](../retrodoc/references/documentation-contract.md), including its English-language and exclusive executable-evidence policy, before tracing the feature. This skill requires the sibling `retrodoc` folder; it can run without an existing atlas by creating a minimal index for the requested scope.


Before discovery, follow the contract's source/output root procedure: capture the invocation directory as `DOCS_ROOT` and ask for the source path unless supplied in the request. In a parent Retrodoc workflow, inherit its validated roots without asking again. All documentation is written directly under `DOCS_ROOT`; source inspection uses `SOURCE_ROOT`.

1. Locate the capability using implemented operations, registration points, callers and executable test assertions. Derive domain terms from those artifacts; exclude glossaries, ADRs, documentation, comments and descriptive docstrings as evidence. If unrelated capabilities match, show concrete candidates and ask which one; continue collecting facts common to them.
2. Follow implementation from trigger through decisions, state and side effects to outcome. Inspect failure branches, authorization and configuration gates. Trace registrations and dependency injection as well as direct calls. Follow important indirect dependencies until reaching an inspected local implementation, an external interaction established by local executable code/tests, or a recorded unknown.
3. Build the participating-files table as you trace. Include shared symbols, schema/migration, assets, registration and tests; explain each role. Filenames and imports alone do not prove participation in a particular behavior.
4. Write the page using all eight contract sections. Separate behavior from implementation so a refactoring agent knows what must remain stable. Derive the copy brief from dependency closure, including resources and environment requirements. Trace inbound consumers for refactoring impact. Record uncertainty where source access ends.
5. Update the feature index and reverse source index, preserving other feature rows. Add observed dependencies to an existing architecture dataset when its schema is available; otherwise retain evidence in the page for later analysis. Check every source link and material behavioral assertion against inspected files.

Done when all sections are substantive, every listed file has a role and evidence, and readers can distinguish verified behavior from transfer assumptions. Report inspected scope and test execution status. Do not implement suggested changes during documentation.
