"""Behavior checks for the bundled HTML renderer and ticket scaffolder."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/retrodoc/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


render = load('render_html')
scaffold = load('scaffold_tickets')


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name).resolve()
        self.docs, self.source = base / 'docs', base / 'app'
        (self.docs / 'features').mkdir(parents=True)
        (self.source / 'src').mkdir(parents=True)
        (self.source / 'src/orders.py').write_text('pass\n')
        (self.docs / 'features/orders.md').write_text('# Orders\n\nLead.\n\n## Behavior\n\nA.\n\n## Behavior\n\nB.\n')

    def page(self, text, name='README.md'):
        (self.docs / name).write_text(text)
        return render.main([str(self.docs)])

    def html(self, name='index.html'):
        return (self.docs / name).read_text()

    def test_front_matter_lead_links_and_hash(self):
        self.assertEqual(self.page('---\nstatus: planning\nscope: whole project\n---\n# Atlas\n\nLead **text**.\n\n'
                                   '## Key reading\n\n- See [orders](features/orders.md#behavior) and [`src/orders.py`](../app/src/orders.py).\n'), 0)
        out = self.html()
        self.assertIn('<span class="badge">planning</span>', out)
        self.assertIn('<p>Lead <strong>text</strong>.</p>', out)
        self.assertIn('class="card callout"', out)
        self.assertIn('href="features/orders.html#behavior"', out)
        self.assertIn('href="../app/src/orders.py"', out)
        self.assertEqual(render.main([str(self.docs), '--check']), 0)

    def test_escapes_html_and_drops_unsafe_links_and_svg_scripts(self):
        self.page('# A\n\n<script>x()</script> [bad](javascript:alert(1))\n\n'
                  '```svg\n<svg viewBox="0 0 1 1" onload="x()"><script>x()</script><path d="M0 0"/></svg>\n```\n')
        out = self.html().split('<body>')[1]
        self.assertNotIn('<script', out)
        self.assertNotIn('javascript:', out)
        self.assertNotIn('onload', out)
        self.assertIn('&lt;script&gt;', out)
        self.assertIn('<path d="M0 0" />', out)

    def test_tables_with_pipes_nested_lists_and_unique_ids(self):
        self.page('# A\n\n## T\n\n| a | b |\n|---|---|\n| `x|y` | c \\| d |\n\n1. one\n   - two\n2. three\n')
        out = self.html()
        self.assertIn('<td><code>x|y</code></td><td>c | d</td>', out)
        self.assertIn('<ol><li>one<ul><li>two</li></ul></li><li>three</li></ol>', out)
        feature = self.html('features/orders.html')
        self.assertIn('id="behavior"', feature)
        self.assertIn('id="behavior-1"', feature)

    def test_unpaired_mermaid_is_flagged_and_paired_mermaid_is_not(self):
        self.page('# A\n\n```mermaid\ngraph LR; a-->b\n```\n')
        self.assertIn('data-retrodoc-incomplete', self.html())
        self.assertEqual(render.main([str(self.docs), '--check']), 1)
        self.page('# A\n\n```mermaid\ngraph LR; a-->b\n```\n\n```svg\n<svg viewBox="0 0 1 1"><title>a to b</title></svg>\n```\n')
        self.assertNotIn('data-retrodoc-incomplete', self.html())
        self.assertEqual(render.main([str(self.docs), '--check']), 0)

    def test_check_detects_stale_render_and_broken_link(self):
        self.page('# A\n\n[missing](nothere.md)\n')
        (self.docs / 'README.md').write_text('# A\n\nchanged\n')
        problems = render.check(render.Workspace(self.docs), render.Workspace(self.docs).pages())
        self.assertTrue(any('stale' in p for p in problems))
        self.assertTrue(any('broken link nothere.html' in p for p in problems))

    def test_unchanged_pages_are_not_rewritten_and_unrelated_html_is_preserved(self):
        self.page('# A\n')
        before = self.html()
        report = render.render(render.Workspace(self.docs), render.Workspace(self.docs).pages(), today='2099-01-01')
        self.assertIn('index.html', report['unchanged'])
        self.assertEqual(self.html(), before)
        (self.docs / 'index.html').write_text('<p>someone else</p>')
        (self.docs / 'retrodoc-context.json').write_text(json.dumps(dict(version=1, index='README.md')))
        ws = render.Workspace(self.docs)
        self.assertEqual(ws.html_index.name, 'retrodoc-index.html')
        render.render(ws, ws.pages())
        self.assertEqual(self.html(), '<p>someone else</p>')
        self.assertIn('href="../retrodoc-index.html"', self.html('features/orders.html'))
        self.assertEqual(json.loads((self.docs / 'retrodoc-context.json').read_text())['html_index'], 'retrodoc-index.html')


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name).resolve()
        self.docs, self.source = base / 'docs', base / 'app'
        self.docs.mkdir()
        (self.source / 'src').mkdir(parents=True)
        (self.source / 'src/orders.py').write_text('pass\n')
        self.plan = base / 'plan.json'
        self.tickets = [
            dict(id='RD-001', type='shared', title='Order model', objective='Document the order model.', features=['order-model'],
                 leads=[dict(path='src/orders.py', note='`Order`')], first_step='Read `Order` in src/orders.py.'),
            dict(id='RD-002', type='feature', title='Place order', objective='Document placing an order.', features=['orders'],
                 leads=[dict(path='src/orders.py', note='`place`')], deps=[dict(id='RD-001', provides='model contract')],
                 first_step='Read `place`.')]
        self.write_plan()

    def write_plan(self):
        self.plan.write_text(json.dumps(dict(version=1, source_root=str(self.source), tickets=self.tickets,
                                             snapshot=dict(revision='abc1234def', dirty='clean', inspected='2026-10-18'))))

    def test_creates_tickets_queue_and_renderable_pages(self):
        self.assertEqual(scaffold.main([str(self.docs), str(self.plan)]), 0)
        first = (self.docs / 'tickets/RD-001.md').read_text()
        self.assertIn('status: ready', first)
        self.assertIn('[`src/orders.py`](../../app/src/orders.py)', first)
        self.assertIn('status: blocked', (self.docs / 'tickets/RD-002.md').read_text())
        queue = (self.docs / 'tickets/index.md').read_text()
        self.assertIn('| [RD-002](RD-002.md) | feature | Place order | `orders` | `blocked` | [RD-001](RD-001.md) |', queue)
        (self.docs / 'README.md').write_text('# Atlas\n\n[Queue](tickets/index.md)\n')
        self.assertEqual(render.main([str(self.docs)]), 0)
        self.assertEqual(render.main([str(self.docs), '--check']), 0)

    def test_two_wave_tickets_split_functional_and_technical_pages(self):
        self.tickets = [
            dict(id='RD-001', type='functional', title='Orders', objective='Document orders functionally.', features=['orders'],
                 surfaces=[dict(kind='screen', name='Checkout', access='Cart › Checkout | /checkout')],
                 leads=[dict(path='src/orders.py')], first_step='Read the checkout screen.'),
            dict(id='RD-002', type='review', title='Functional review', objective='Ask open questions.',
                 deps=[dict(id='RD-001')], first_step='Read `questions.md`.'),
            dict(id='RD-003', type='enrichment', title='Orders internals', objective='Enrich orders.', features=['orders'],
                 leads=[dict(path='src/orders.py')], deps=[dict(id='RD-001'), dict(id='RD-002')], first_step='Read `place`.')]
        self.write_plan()
        self.assertEqual(scaffold.main([str(self.docs), str(self.plan)]), 0)
        functional, review, enrichment = ((self.docs / f'tickets/RD-00{n}.md').read_text() for n in (1, 2, 3))
        self.assertIn('| screen | Checkout | Cart › Checkout \\| /checkout |', functional)
        self.assertIn('`features/orders.md` (functional page)', functional)
        self.assertNotIn('technical.md', functional)
        self.assertIn('not asked', functional)
        self.assertIn('status: blocked', review)
        self.assertIn('one batch', review)
        self.assertIn('`features/orders/technical.md` (technical page)', enrichment)
        self.assertNotIn('## Interaction surfaces', enrichment)

    def test_rejects_surfaces_without_kind_or_name(self):
        self.tickets[1]['surfaces'] = [dict(name='Checkout')]
        self.write_plan()
        self.assertEqual(scaffold.main([str(self.docs), str(self.plan)]), 1)
        self.assertFalse((self.docs / 'tickets').exists())

    def test_never_overwrites_existing_tickets_and_appends_new_rows(self):
        scaffold.main([str(self.docs), str(self.plan)])
        done = (self.docs / 'tickets/RD-001.md')
        done.write_text(done.read_text().replace('status: ready', 'status: done') + '\nHandoff kept.\n')
        self.tickets.append(dict(id='RD-003', type='check', title='Final check', objective='Validate.',
                                 deps=[dict(id='RD-001')], first_step='Rescan registrations.'))
        self.write_plan()
        created, kept, _ = scaffold.scaffold(self.docs, self.plan)
        self.assertEqual(created, ['RD-003'])
        self.assertEqual(kept, ['RD-001', 'RD-002'])
        self.assertIn('Handoff kept.', done.read_text())
        self.assertIn('status: ready', (self.docs / 'tickets/RD-003.md').read_text())
        queue = (self.docs / 'tickets/index.md').read_text()
        self.assertEqual(queue.count('| [RD-001](RD-001.md) | shared'), 1)
        self.assertIn('| [RD-003](RD-003.md) | check |', queue)

    def test_rejects_missing_leads_and_unknown_dependencies_without_writing(self):
        self.tickets[0]['leads'] = [dict(path='src/missing.py')]
        self.write_plan()
        self.assertEqual(scaffold.main([str(self.docs), str(self.plan)]), 1)
        self.assertFalse((self.docs / 'tickets').exists())
        self.tickets[0]['leads'] = [dict(path='src/orders.py')]
        self.tickets[1]['deps'] = [dict(id='RD-999')]
        self.write_plan()
        self.assertEqual(scaffold.main([str(self.docs), str(self.plan)]), 1)
        self.assertFalse((self.docs / 'tickets').exists())


if __name__ == '__main__':
    unittest.main()
