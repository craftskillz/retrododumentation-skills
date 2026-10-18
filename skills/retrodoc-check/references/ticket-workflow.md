# Ticket-based documentation passes

Use this workflow for project-wide documentation. A first pass creates an evidence-backed plan in its own session; each execution ticket then uses a separate fresh conversation. The ticket and its durable handoff replace reliance on the planning conversation. The purpose is to bound context growth and repeated reading; actual cost depends on the project and model and is not guaranteed. Tickets are local Markdown artifacts, not external issues. Do not create issues or send messages without a separate request.

## Pass 1: discover and plan

Establish SOURCE_ROOT and DOCS_ROOT using the documentation contract. Inspect executable registrations and representative vertical traces deeply enough to identify capabilities, boundaries and dependencies. Clarify only domain/audience questions that code cannot settle; do not require users to name features. Do not deeply document every feature in this pass.

Write location metadata, the bounded feature inventory, coverage and `tickets/index.md`. Create one stable `RD-NNN` ticket per coherent documentary outcome. Split oversized features by observable behavior; avoid one ticket per file or a ticket that requires understanding the entire product. Add shared-concern tickets only when evidence shows a reusable contract, plus architecture-integration and final-validation tickets. Record actual dependencies; do not impose an arbitrary serial chain. Architecture tickets depend on the source mappings they use; final validation depends on the pages/graphs in scope.

Check every discovered entry point is attributed and every planned deliverable has an owner. Each ticket needs a runnable first inspection step and bounded acceptance criteria. If discovery cannot settle a boundary, create an investigation ticket with a question and completion criterion rather than inventing behavior. Existing partial dossiers may seed tickets but are unverified outputs to recheck, not factual evidence.

Publish paired Markdown/HTML inventory, coverage and ticket pages. Link only existing dossiers. Stop after planning and present the recommended ready ticket with a copyable fresh-session prompt. This is completion of Pass 1, not completion of the atlas. Do not start the first execution ticket in the planning context, even when the eventual request covers the whole project. Save the plan and give the next fresh-session prompt.

## Ticket contract

Each ticket contains enough context to execute without the planning conversation:

- Stable ID, title, type (feature/shared/investigation/architecture/check), status and owning feature IDs.
- Absolute source root, output root, inspected revision and dirty state (or dated non-Git snapshot), plus index/context paths relative to the output root.
- Observable documentary objective, actor/trigger/outcome where known, included/excluded scope and exact output files. Keep intended behavior separate from observed behavior.
- Executable starting points: source-root-relative paths, symbols/registrations and tests with the assertion scope already inspected. These are leads to re-read, not proof carried across sessions. Never use repository prose as evidence.
- Dependencies by ticket ID and what evidence/deliverable they provide; independent work remains independently ready.
- Concrete acceptance criteria: relevant behavior/failures/state contracts, participating-file table, copy/refactor limits, source citations, index/coverage updates and HTML parity. Architecture/check tickets use their respective contracts instead of feature-only sections.
- Known unknowns and a short inspection plan, including the next exact file/symbol to inspect. Record runtime checks separately from documentary checks; application execution is optional unless the user requests it.
- Handoff: inspected files/ranges and findings with citations, outputs changed, validations actually run, unresolved paths, remaining work and the next action. Do not dump raw conversation or sensitive values.
- A fresh-session invocation that names this ticket and tells the agent to work from DOCS_ROOT.

Keep `tickets/index.md` as the queue with ID, objective, status, dependencies and links. Ticket states are `ready`, `in_progress`, `blocked`, `done`, `unresolved`; these are distinct from feature statuses. A ticket is ready only when its required dependencies are satisfied. Blocked means a named missing prerequisite prevents progress; unresolved means a bounded investigation concluded with an explicit evidence gap accepted by the relevant scope. Neither state silently counts as verified behavior. A ticket is done only after its acceptance criteria and documentary validation are satisfied.

## Session boundaries and efficient context loading

Use a genuinely fresh conversation for each ticket. A summary, compaction or rereading the ticket in the same conversation is not a fresh context. A single context may work on at most one execution ticket; a large unfinished ticket may resume in another fresh session with its updated handoff. If the current conversation already performed discovery/planning or a different ticket, preserve the handoff and direct the user to start a new conversation instead of executing the next ticket here.

Load the selected ticket, location metadata, relevant queue rows and required dependency outputs. Read only the applicable workflow references and executable source needed for that bounded trace. Follow local dependencies when necessary, but do not reload every dossier, the whole queue's handoff history, the entire source tree or the planning transcript. Use the revision/local-change comparison to decide which additional evidence needs reinspection. Reserve full registration rescanning and atlas-wide reconciliation for their integration/check tickets unless local drift requires them sooner.

The default handoff is a copyable prompt for a new conversation. Do not claim to reset this conversation or silently launch subagents. If the user explicitly requests orchestration and a tool can create independent fresh contexts, that orchestrator may run the queue with one ticket per context and durable handoffs; otherwise stop at the boundary. Independent contexts must receive the ticket and required artifacts, not the parent conversation history.

## Pass 2: execute one ticket

An explicit ticket selection supplies the source/output context in that ticket; validate and state the paths rather than asking for the same source selection again. Capture the invocation directory as DOCS_ROOT. If it differs from the ticket's output root, stop to resolve the destination instead of writing into two atlases. Check existing context for source identity conflicts.

Read the selected ticket, queue dependencies, applicable documentation contract and only the relevant bundled feature/architecture/check workflow. Compare HEAD and local changes with the ticket snapshot; re-read executable evidence before accepting claims. If drift changes scope or prerequisites, update the ticket/coverage and investigate affected boundaries before continuing. Prior-session prose and hashes do not establish current correctness.

Mark the ticket in_progress, complete its bounded vertical trace and outputs, and validate that slice in Markdown and HTML. Update the atlas, source mappings, coverage and ticket handoff. Mark done only when its acceptance criteria hold; otherwise record the specific remaining gap and accurate status. Do not implement application changes.

End the session after the selected ticket with its status, outputs, checks, unresolved work and the next ready ticket's fresh-session prompt. Stop after that handoff. A request covering several tickets or the whole project still requires a separate fresh context for each ticket; it does not authorize a same-conversation loop. If the ticket remains unfinished, the next prompt resumes that same ticket. Splitting work into tickets does not itself authorize delegation.

## Pass 3: integrate and verify

Execute each architecture/integration ticket in its own fresh context to reconcile typed dependencies, diagrams, shared concepts, glossary and reverse source index across completed feature mappings. Then execute the final validation ticket in another fresh context: rescan registrations for coverage changes, check source freshness, reconcile unresolved items and validate both reading editions. Avoid claiming the full project is documented while tickets remain incomplete. Report done/unresolved/blocked counts and the exact remaining scope.

## Fresh-session prompt

Start a new conversation from DOCS_ROOT, then paste this prompt adapted with actual established paths and an existing ticket. Do not paste the planning transcript:

```text
Work from <DOCS_ROOT>. Use $retrodoc to execute only tickets/RD-NNN.md.
The ticket supplies SOURCE_ROOT and the inspected snapshot. Validate both roots,
recheck source freshness, finish the ticket's documentation and checks, update
its handoff and queue, then stop. Do not modify the source application.
```

If the named skill is not installed, ask the agent to read the available standalone Retrodoc SKILL.md and follow its bundled ticket workflow. Do not require companion installation.
