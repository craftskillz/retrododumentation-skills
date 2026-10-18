"""Check isolated bundles and optionally exercise the real Skills CLI."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('builder', ROOT / 'scripts/build_skills.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
NAMES = {'retrodoc', 'retrodoc-help', 'retrodoc-feature', 'retrodoc-architecture', 'retrodoc-check'}


def assert_bundle(test, folder):
    test.assertTrue((folder / 'SKILL.md').is_file())
    test.assertEqual(len(list(folder.rglob('SKILL.md'))), 1)
    for document in folder.rglob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text()):
            if '://' in link or link.startswith('#'):
                continue
            target = (document.parent / link.split('#')[0]).resolve()
            test.assertTrue(target.is_relative_to(folder.resolve()), f'External dependency: {document}: {link}')
            test.assertTrue(target.is_file(), f'Missing resource: {document}: {link}')


class PackagingTests(unittest.TestCase):
    def test_committed_bundles_match_sources(self):
        self.assertTrue(builder.synchronize(ROOT / 'skills', builder.planned_files(), check=True))
        self.assertEqual({p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}, NAMES)

    def test_each_skill_works_without_sibling_files(self):
        with tempfile.TemporaryDirectory() as temp:
            for name in sorted(NAMES):
                target = Path(temp) / name
                shutil.copytree(ROOT / 'skills' / name, target)
                assert_bundle(self, target)

    def test_check_detects_missing_or_changed_bundled_resource(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            files = {Path('demo/references/contract.md'): b'canonical'}
            builder.synchronize(target, files)
            (target / 'demo/references/contract.md').write_text('drift')
            self.assertFalse(builder.synchronize(target, files, check=True))
            builder.synchronize(target, files)
            (target / 'demo/references/contract.md').unlink()
            self.assertFalse(builder.synchronize(target, files, check=True))

    def test_installed_analyzer_accepts_separate_source_root(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, docs = root / 'application', root / 'documentation'
            source.mkdir()
            docs.mkdir()
            (source / 'a.py').write_text('import b\n')
            (source / 'b.py').write_text('import a\n')
            data = dict(version=1, snapshot='fixture', granularity='file', scope='fixture', limitations=[], features=['demo'],
                        nodes=[dict(id=n, label=n, path=n+'.py', features=['demo']) for n in 'ab'],
                        edges=[{'from': a, 'to': b, 'kind': 'import', 'evidence': [dict(path=a+'.py', line=1, note='Local import')]} for a,b in [('a','b'),('b','a')]])
            graph = docs / 'graph.json'
            graph.write_text(json.dumps(data))
            for name in sorted(NAMES):
                target = docs / name
                shutil.copytree(ROOT / 'skills' / name, target)
                result = subprocess.run([sys.executable, str(target / 'scripts/analyze_graph.py'), str(graph), '--root', str(source)], cwd=docs, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('- n0 (a), n1 (b)', result.stdout)

    def test_installed_renderer_works_from_each_bundle(self):
        with tempfile.TemporaryDirectory() as temp:
            docs = Path(temp) / 'documentation'
            docs.mkdir()
            (docs / 'README.md').write_text('# Atlas\n\nLead.\n')
            for name in sorted(NAMES):
                target = Path(temp) / name
                shutil.copytree(ROOT / 'skills' / name, target)
                script = target / 'scripts/render_html.py'
                for args in ([], ['--force'], ['--check']):
                    result = subprocess.run([sys.executable, str(script), str(docs), *args], text=True, capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                self.assertIn('--accent', (docs / 'index.html').read_text())


@unittest.skipUnless(os.environ.get('RETRODOC_SKILLS_COMMAND'), 'Set RETRODOC_SKILLS_COMMAND to run real installer checks')
class SkillsCliTests(unittest.TestCase):
    def test_discovery_and_individual_installs(self):
        command = shlex.split(os.environ['RETRODOC_SKILLS_COMMAND'])
        environment = dict(os.environ, DO_NOT_TRACK='1', DISABLE_TELEMETRY='1')
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            # Reproduce the publishable layout, excluding locally installed third-party skills.
            exported = temp / 'repository'
            shutil.copytree(ROOT / 'skills', exported / 'skills')
            shutil.copytree(ROOT / 'authoring', exported / 'authoring')
            listed = subprocess.run(command + ['add', str(exported), '--list'], cwd=temp, env=environment, text=True, capture_output=True, timeout=60)
            self.assertEqual(listed.returncode, 0, listed.stderr + listed.stdout)
            self.assertIn('Found 5 skills', listed.stdout)
            for name in NAMES:
                self.assertIn(name, listed.stdout)
            for mode in ('symlink', 'copy'):
                for name in sorted(NAMES):
                    with self.subTest(mode=mode, skill=name):
                        project = temp / (name + '-' + mode)
                        project.mkdir()
                        # Both agents get their own paths in the same otherwise-empty project.
                        (project / '.claude').mkdir()
                        args = command + ['add', str(exported), '--skill', name, '--agent', 'codex', 'claude-code', '--yes']
                        if mode == 'copy':
                            args.append('--copy')
                        installed = subprocess.run(args, cwd=project, env=environment, text=True, capture_output=True, timeout=60)
                        self.assertEqual(installed.returncode, 0, installed.stderr + installed.stdout)
                        for agent_dir in ('.agents', '.claude'):
                            parent = project / agent_dir / 'skills'
                            self.assertEqual({p.name for p in parent.iterdir()}, {name})
                            folder = parent / name
                            assert_bundle(self, folder)
                            for original in (exported / 'skills' / name).rglob('*'):
                                if original.is_file() and '__pycache__' not in original.parts:
                                    self.assertEqual((folder / original.relative_to(exported / 'skills' / name)).read_bytes(), original.read_bytes())
                        if mode == 'symlink':
                            self.assertTrue((project / '.claude/skills' / name).is_symlink())


if __name__ == '__main__':
    unittest.main()
