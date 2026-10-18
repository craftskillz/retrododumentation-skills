#!/usr/bin/env python3
"""Create missing Retrodoc ticket pages and queue rows from a planning file; never overwrite tickets."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote

TYPES = {'feature', 'shared', 'investigation', 'architecture', 'check'}
STATUS = re.compile(r'^status:\s*(\S+)', re.M)
ID = re.compile(r'^RD-\d{3,}$')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strings(value, field, ident):
    require(isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value), f'{ident}: {field} must be a list of strings')
    return value


def entries(value, field, ident):
    require(isinstance(value, list), f'{ident}: {field} must be a list')
    for entry in value:
        require(isinstance(entry, dict) and isinstance(entry.get('path'), str) and entry['path'].strip(),
                f'{ident}: each {field} entry needs a path')
    return value


def load_plan(path, docs_root):
    plan = json.loads(Path(path).read_text(encoding='utf-8'))
    require(isinstance(plan, dict) and plan.get('version') == 1, 'plan must be an object with version 1')
    source = Path(plan.get('source_root', '')).expanduser()
    require(source.is_absolute() and source.is_dir(), 'source_root must be an existing absolute directory')
    snapshot = plan.get('snapshot')
    require(isinstance(snapshot, dict) and all(isinstance(snapshot.get(k), str) and snapshot[k].strip()
                                               for k in ('revision', 'dirty', 'inspected')),
            'snapshot needs revision, dirty and inspected')
    context = docs_root / 'retrodoc-context.json'
    if context.is_file():
        saved = json.loads(context.read_text(encoding='utf-8')).get('source_root')
        require(not saved or Path(saved).resolve() == source.resolve(), f'plan source_root differs from retrodoc-context.json ({saved})')
    tickets = plan.get('tickets')
    require(isinstance(tickets, list) and tickets, 'tickets must be a nonempty list')
    seen = set()
    for t in tickets:
        require(isinstance(t, dict), 'ticket must be an object')
        ident = t.get('id', '?')
        require(isinstance(ident, str) and ID.match(ident) and ident not in seen, f'missing, malformed or duplicate ticket ID: {ident}')
        seen.add(ident)
        require(t.get('type') in TYPES, f'{ident}: type must be one of {sorted(TYPES)}')
        for key in ('title', 'objective', 'first_step'):
            require(isinstance(t.get(key), str) and t[key].strip(), f'{ident}: missing {key}')
        for key in ('features', 'include', 'exclude', 'unknowns', 'acceptance', 'outputs'):
            t[key] = strings(t.get(key, []), key, ident)
        for key in ('leads', 'tests'):
            t[key] = entries(t.get(key, []), key, ident)
        require(t['type'] not in ('feature', 'shared') or t['features'], f'{ident}: {t["type"]} tickets need features')
        require(t['type'] not in ('feature', 'shared', 'investigation') or t['leads'], f'{ident}: needs executable leads')
        deps = t.get('deps', [])
        require(isinstance(deps, list) and all(isinstance(d, dict) and isinstance(d.get('id'), str) for d in deps),
                f'{ident}: deps must be a list of {{"id", "provides"}} objects')
        t['deps'] = deps
    return plan, source.resolve(), tickets


def source_link(source, rel, page_dir):
    if any(ch in rel for ch in '*?['):
        return f'`{rel}`'
    target = source / rel.rstrip('/')
    require(target.exists(), f'missing source lead: {rel}')
    href = '/'.join(quote(part) for part in Path(os.path.relpath(target, page_dir)).parts)
    return f'[`{rel}`]({href}{"/" if rel.endswith("/") else ""})'


def default_outputs(t):
    kinds = {'feature': 'features', 'shared': 'shared'}
    if t['type'] in kinds:
        outputs = [f'`{kinds[t["type"]]}/{f}.md`' for f in t['features']]
    elif t['type'] == 'investigation':
        outputs = ['Findings in `coverage.md` and this ticket\'s handoff']
    elif t['type'] == 'architecture':
        outputs = ['`architecture/dependencies.json`', '`architecture/dependencies.md`', '`architecture/findings.md`',
                   '`source-index.md`', '`glossary.md`']
    else:
        outputs = ['`checks.md`']
    return outputs + ['Updates to the index, `coverage.md`, the queue and this ticket', '`retrodoc-context.json` (`next_ticket`)',
                      'Re-rendered HTML siblings for every changed page']


def default_acceptance(t):
    if t['type'] == 'feature':
        items = [f'`features/{f}.md` contains all eight feature page contract sections.' for f in t['features']]
        items += ['Normal flow, meaningful failures, validation, state changes and side effects cite implementation or test assertions with evidence labels.',
                  'The participating-file table lists every traced file with symbols, role and evidence; shared files are marked.',
                  'Copying and refactoring sections state transitive local dependencies, registration points and unresolved closure.',
                  'Test assertion scope is described per test file; tests are reported as run with results or "not run".']
    elif t['type'] == 'shared':
        items = [f'`shared/{f}.md` documents the reusable contract, its cited consumers and invariants.' for f in t['features']]
        items += ['Listed consumers match an actual import/call search.']
    elif t['type'] == 'investigation':
        items = ['The question is answered with executable citations, or the evidence gap is recorded and the ticket marked `unresolved`.']
    elif t['type'] == 'architecture':
        items = ['`architecture/dependencies.json` validates with the bundled analyzer against SOURCE_ROOT.',
                 'Findings carry evidence, confidence, impact and counterevidence; unfinished feature tickets are listed as limits.']
    else:
        items = ['`checks.md` separates structural, semantic and execution results.',
                 'A registration rescan is compared with `coverage.md`; done/unresolved/blocked counts are reported.']
    return items + ['Source links resolve from each page\'s directory to SOURCE_ROOT.',
                    '`render_html.py --check` reports no problems for the changed pages.']


def ticket_page(t, status, plan, source, docs_root, queue):
    page_dir = queue.parent
    snap = plan['snapshot']
    features = ', '.join(f'`{f}`' for f in t['features']) or '— (cross-cutting)'
    lines = ['---', f'status: {status}', f'scope: {", ".join(t["features"]) or t["type"]}',
             f'snapshot: Git `{snap["revision"][:12]}` ({snap["dirty"]})', f'inspected: {snap["inspected"]}', '---',
             f'# {t["id"]} — {t["title"]}', '', t['objective'], '',
             '## Key reading', '',
             '- Established: executable starting points located during planning.',
             '- Main limit: no behavior traced yet; every lead must be re-read against the current source.',
             '- Look next: the inspection plan below.', '',
             '## Ticket', '', '| Field | Value |', '|---|---|',
             f'| ID | `{t["id"]}` |', f'| Type | {t["type"]} |', f'| Owning feature IDs | {features} |',
             f'| Created | {snap["inspected"]} (Pass 1) |', '',
             '## Roots and snapshot', '',
             f'- **SOURCE_ROOT:** `{source}`', f'- **DOCS_ROOT:** `{docs_root}`',
             f'- **Planned against:** Git `{snap["revision"]}`; working tree {snap["dirty"]}.',
             f'- **Context:** `retrodoc-context.json`; **queue:** `{queue.relative_to(docs_root).as_posix()}` (relative to DOCS_ROOT).', '',
             '## Objective and scope', '']
    for key, label in (('actor', 'Actor / trigger'), ('outcome', 'Observed outcome to verify')):
        if t.get(key):
            lines.append(f'- **{label}:** {t[key]}')
    lines += ['', '**Included:**', ''] + [f'- {x}' for x in t['include'] or ['The objective above.']] + ['']
    if t['exclude']:
        lines += ['**Excluded:**', ''] + [f'- {x}' for x in t['exclude']] + ['']
    lines += ['Outcomes were located during planning and are not yet verified behavior.', '',
              '## Output files', ''] + [f'- {x}' for x in t['outputs'] or default_outputs(t)] + ['', '## Executable starting points', '']
    if t['leads']:
        lines += ['| Source | Lead |', '|---|---|'] + [f'| {source_link(source, x["path"], page_dir)} | {x.get("note") or "—"} |' for x in t['leads']]
    else:
        lines.append('- Completed dossiers, `coverage.md` and the workflow for this ticket type.')
    lines.append('')
    if t['tests']:
        lines += ['**Tests located (assertion scope as noted):**', '', '| Test | Note |', '|---|---|']
        lines += [f'| {source_link(source, x["path"], page_dir)} | {x.get("note") or "assertions not yet inspected"} |' for x in t['tests']] + ['']
    elif t['type'] in ('feature', 'shared'):
        lines += ['**Tests located:** none during planning; search again before concluding there is no coverage.', '']
    lines += ['## Dependencies', '']
    if t['deps']:
        lines += [f'- [{d["id"]}]({d["id"]}.md) — {d.get("provides") or "deliverable required as input"}' for d in t['deps']]
        lines.append('- Status stays `blocked` until these tickets are `done`.')
    else:
        lines.append('- None. Independently ready.')
    lines += ['', '## Acceptance criteria', ''] + [f'- {x}' for x in default_acceptance(t) + t['acceptance']]
    lines += ['', '## Known unknowns and inspection plan', ''] + [f'- {x}' for x in t['unknowns'] or ['None recorded at planning time.']]
    lines += ['', '**Inspection plan:**', '', f'1. {t["first_step"]}',
              '2. Trace one vertical path end to end before widening.',
              '3. Read the listed tests\' setup and assertions; record mocks and skips.',
              '4. Write the Markdown outputs, run the bundled HTML renderer, then validate links, citations and parity.', '',
              'Runtime checks are optional; if skipped, record "not run". Do not modify the source project.', '',
              '## Handoff', '',
              f'- **{snap["inspected"]} — Pass 1 planning:** ticket created from registration scans; no behavior traced and no outputs exist yet.',
              '- **Next action:** step 1 of the inspection plan.', '',
              '## Fresh-session prompt', '', '```text',
              f'Work from {docs_root}. Use $retrodoc to execute only {queue.parent.relative_to(docs_root).as_posix()}/{t["id"]}.md.',
              'The ticket supplies SOURCE_ROOT and the inspected snapshot. Validate both roots,',
              'recheck source freshness, finish the ticket\'s documentation and checks, update',
              'its handoff and queue, then stop. Do not modify the source application.', '```', '']
    return '\n'.join(lines)


def queue_row(t, status):
    deps = ', '.join(f'[{d["id"]}]({d["id"]}.md)' for d in t['deps']) or '—'
    features = ', '.join(f'`{f}`' for f in t['features']) or '—'
    return f'| [{t["id"]}]({t["id"]}.md) | {t["type"]} | {t["title"]} | {features} | `{status}` | {deps} |'


def new_queue(rows, plan):
    return '\n'.join(['---', 'status: planning', 'scope: ticket queue', f'inspected: {plan["snapshot"]["inspected"]}', '---',
                      '# Ticket queue', '', 'Bounded Retrodoc tickets; each ticket runs in its own fresh session.', '',
                      '## Queue', '', '| ID | Type | Objective | Features | Status | Depends on |', '|---|---|---|---|---|---|',
                      *rows, '', '## How to run the next ticket', '',
                      'Start a new conversation in DOCS_ROOT and invoke `$retrodoc`; it resumes the unfinished ticket or selects the next ready one.', ''])


def append_rows(text, rows):
    lines = text.split('\n')
    header = next((n for n, l in enumerate(lines) if l.startswith('|') and re.search(r'\|\s*ID\s*\|', l)), None)
    require(header is not None, 'existing queue has no table with an ID column; add the new rows by hand')
    end = header
    while end + 1 < len(lines) and lines[end + 1].startswith('|'):
        end += 1
    return '\n'.join(lines[:end + 1] + rows + lines[end + 1:])


def scaffold(docs_root, plan_path, dry_run=False):
    docs_root = Path(docs_root).resolve()
    require(docs_root.is_dir(), f'not a directory: {docs_root}')
    plan, source, tickets = load_plan(plan_path, docs_root)
    context = docs_root / 'retrodoc-context.json'
    queue_rel = json.loads(context.read_text(encoding='utf-8')).get('ticket_queue') if context.is_file() else None
    queue = docs_root / (queue_rel or 'tickets/index.md')
    known = {p.stem: p for p in queue.parent.glob('RD-*.md')}
    planned = {t['id'] for t in tickets}
    statuses = {}
    for ident, path in known.items():
        match = STATUS.search(path.read_text(encoding='utf-8'))
        statuses[ident] = match[1] if match else 'unknown'
    created, kept, pages = [], [], {}
    for t in tickets:
        if t['id'] in known:
            kept.append(t['id'])
            continue
        for d in t['deps']:
            require(d['id'] in planned or d['id'] in known, f'{t["id"]}: unknown dependency {d["id"]}')
        status = 'ready' if all(statuses.get(d['id']) == 'done' for d in t['deps']) else 'blocked'
        pages[queue.parent / f'{t["id"]}.md'] = ticket_page(t, status, plan, source, docs_root, queue)
        created.append((t, status))
    rows = [queue_row(t, status) for t, status in created]
    queue_text = None
    if rows:
        queue_text = append_rows(queue.read_text(encoding='utf-8'), rows) if queue.is_file() else new_queue(rows, plan)
    if not dry_run:
        queue.parent.mkdir(parents=True, exist_ok=True)
        for path, text in pages.items():
            path.write_text(text, encoding='utf-8')
        if queue_text is not None:
            queue.write_text(queue_text, encoding='utf-8')
    return [t['id'] for t, _ in created], kept, queue


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docs_root', help='Retrodoc output root (DOCS_ROOT)')
    parser.add_argument('plan', help='Planning JSON file (keep it outside DOCS_ROOT; ticket pages are authoritative)')
    parser.add_argument('--dry-run', action='store_true', help='Validate the plan and report without writing')
    args = parser.parse_args(argv)
    try:
        created, kept, queue = scaffold(args.docs_root, args.plan, args.dry_run)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(exc, file=sys.stderr)
        return 1
    verb = 'Would create' if args.dry_run else 'Created'
    print(f'{verb} {len(created)} ticket(s): {", ".join(created) or "none"}')
    if kept:
        print(f'Kept {len(kept)} existing ticket(s) unchanged: {", ".join(kept)}')
    print(f'Queue: {queue}')
    if created and not args.dry_run:
        print('Next: run render_html.py on DOCS_ROOT to publish the HTML siblings.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
