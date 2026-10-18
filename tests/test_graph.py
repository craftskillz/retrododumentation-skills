"""Behavior checks for typed dependency analysis and evidence validation."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/retrodoc-architecture/scripts/analyze_graph.py'
spec = importlib.util.spec_from_file_location('graph', SCRIPT)
graph = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graph)


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for name in ('a.py', 'b.py', 'c.py'):
            (self.root / name).write_text('# fixture\npass\n')
        self.data = dict(version=1, snapshot='test snapshot', granularity='file', scope='fixture',
                         limitations=[], features=['checkout', 'refund'],
                         nodes=[dict(id=n, label=n, path=n+'.py', features=['checkout', 'refund']) for n in 'abc'], edges=[])

    def edge(self, a, b, kind='import'):
        return dict(**{'from': a, 'to': b}, kind=kind,
                    evidence=[dict(path=a+'.py', line=1, note='fixture relationship')])

    def test_scc_separates_cycle_tail_and_self_loop(self):
        self.assertEqual(graph.components({'a': {'b'}, 'b': {'a', 'c'}, 'c': set(), 'd': {'d'}}),
                         [['a', 'b'], ['c'], ['d']])

    def test_type_edges_do_not_create_runtime_import_cycle(self):
        self.data['edges'] = [self.edge('a', 'b'), self.edge('b', 'a', 'type')]
        nodes = graph.validate(self.data, self.root)
        self.assertIn('No cycles found', graph.render(self.data, nodes, 'import'))
        self.assertIn('No cycles found', graph.render(self.data, nodes, 'type'))

    def test_shared_participation_is_not_a_cycle(self):
        output = graph.render(self.data, graph.validate(self.data, self.root), 'import')
        self.assertIn('No cycles found', output)
        self.assertIn('Counts are not god-object diagnoses.', output)

    def test_invalid_evidence_and_endpoints_rejected(self):
        for change in ('endpoint', 'line', 'path', 'feature', 'duplicate'):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                data['edges'] = [self.edge('a', 'b')]
                if change == 'endpoint': data['edges'][0]['to'] = 'missing'
                if change == 'line': data['edges'][0]['evidence'][0]['line'] = 30
                if change == 'path': data['edges'][0]['evidence'][0]['path'] = '../outside.py'
                if change == 'feature': data['nodes'][0]['features'] = ['undeclared']
                if change == 'duplicate': data['edges'] *= 2
                with self.assertRaises(ValueError):
                    graph.validate(data, self.root)

    def test_cli_cycle_and_bad_json(self):
        self.data['edges'] = [self.edge('a', 'b'), self.edge('b', 'a')]
        path = self.root / 'graph.json'
        path.write_text(json.dumps(self.data))
        command = [sys.executable, str(SCRIPT), str(path), '--root', str(self.root)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('- n0 (a), n1 (b)', result.stdout)
        self.assertIn('n0 -->|import| n1', result.stdout)
        path.write_text('{')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('Invalid graph:', result.stderr)

    def test_large_chain_avoids_recursion_limit(self):
        adjacency = {str(i): {str(i+1)} for i in range(3000)}
        adjacency['3000'] = set()
        self.assertEqual(len(graph.components(adjacency)), 3001)

    def test_labels_cannot_break_out_of_diagram(self):
        self.data['nodes'][0]['label'] = 'a"]\n evil --> injected'
        output = graph.render(self.data, graph.validate(self.data, self.root), 'import')
        self.assertNotIn('\n evil --> injected', output)
        self.assertIn('&#34;', output)


if __name__ == '__main__':
    unittest.main()
