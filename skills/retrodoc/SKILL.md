---
name: retrodoc
description: Document an existing project from source code, organized by features for humans and LLMs. Use for project retrodocumentation or a complete feature atlas with source traceability.
---

# Retrodoc

Produce an evidence-backed description of the project as it exists. Keep the source project separate from the invocation directory where documentation is written. These four sibling skills form one bundle; resolve their links relative to this file. Read [the documentation contract](references/documentation-contract.md), especially its English-language and exclusive executable-evidence policy, before discovery or writing. Executable tests are strong documentary evidence; ADRs, other documentation and explanatory comments are not evidence.

## Establish locations

Follow the documentation contract's source/output root procedure first: capture the invocation directory as `DOCS_ROOT`, ask for the source path unless already supplied, and validate `SOURCE_ROOT`. Pass these roots to every subskill. Output stays directly in `DOCS_ROOT` throughout the run.

## Discover and organize

1. Read applicable project instructions as operating constraints. Discover behavior from implementation, executable tests, manifests, build/task definitions, entry points, route/command/event registrations, schemas and deployment configuration. Use existing documentation only as output to check or update, never as a factual discovery source. Record the inspected revision and local modifications, or a dated snapshot when Git is absent. Scope vendor, generated and build output separately.
2. Identify capabilities by actor, trigger and observable outcome. Trace across layers; a folder, class or endpoint is evidence, not automatically a feature. For libraries, public operations are capabilities; for tools, commands and workflows are capabilities. In monorepos, namespace feature IDs by application/domain when names collide.
3. Create a feature inventory with stable IDs, boundaries, entry points, evidence, status and documentation links. Record shared infrastructure separately. Account for each discovered entry point as a feature, shared concern, excluded item with reason, or unresolved item. State which roots and registration mechanisms were inspected; avoid exhaustive-discovery claims when reflection or unavailable services leave gaps.
4. Show the proposed grouping while continuing unambiguous work. Ask only about domain boundaries or audience preferences that code cannot settle. Write Markdown in English for developers and LLMs. Use the captured `DOCS_ROOT` as the documentation destination. Derive feature groupings from executable evidence; ask about intended scope when necessary, and keep user preferences distinct from observed behavior.

Done when the index gives a bounded inventory, not just a sample of interesting features.

## Document and connect

Read and follow [retrodoc-feature](../retrodoc-feature/SKILL.md) for each in-scope feature. Finish one vertical behavior trace before expanding to the next. Keep inventory statuses accurate. For large projects, save inspected sources, unresolved paths and next steps in `coverage.md` so work can resume without treating unfinished pages as verified.

Read and follow [retrodoc-architecture](../retrodoc-architecture/SKILL.md) to build typed dependency evidence, diagrams and separation findings. Include this phase in a full-project run; a user-limited feature run needs only the relevant dependency slice and its stated limits.

Maintain the index, shared-concern pages, code-derived glossary, reverse source index and coverage record using the documentation contract. Every project claim must trace to executable artifacts. When updating existing pages, verify their claims anew; correct unsupported prose and surface disagreements between executable tests and implementation.

## Verify and deliver

Read and follow [retrodoc-check](../retrodoc-check/SKILL.md). Fix documentation errors within the requested scope. Report pages produced, inspected scope, validation performed, unknowns and unfinished features. Completion means all in-scope inventory items are documented or explicitly unresolved with reasons, and the check report has no unreported failures. Distinguish completed documentation work from unverified runtime behavior.

This workflow writes documentation and analysis artifacts. Copying features, refactoring code, publishing docs and opening issues are separate tasks requiring a user request.
