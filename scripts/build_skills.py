#!/usr/bin/env python3
"""Build independently installable skills from canonical authoring files."""
import argparse
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'authoring'
OUTPUT = ROOT / 'skills'
LINK = re.compile(r'(\[[^\]]*\]\()([^)]+)(\))')


def planned_files(source=SOURCE):
    entries = sorted(source.glob('*/entrypoint.md'))
    if not entries:
        raise ValueError('No skill entrypoints found')
    resources = sorted(p for p in source.rglob('*') if p.is_file()
                       and '__pycache__' not in p.parts and p.suffix != '.pyc')
    result = {}
    for entry in entries:
        skill = entry.parent.name
        mapping = {}
        for path in resources:
            relative = path.relative_to(source)
            if relative.parts[1] == 'agents':
                if path.parent.parent == entry.parent:
                    mapping[path] = Path(*relative.parts[1:])
            elif path.name == 'entrypoint.md':
                mapping[path] = (Path('SKILL.md') if path == entry else
                                 Path('references/workflows') / (path.parent.name + '.md'))
            else:
                mapping[path] = Path(*relative.parts[1:])
        if len(set(mapping.values())) != len(mapping):
            raise ValueError(f'Resource destination collision in {skill}')
        for path, dest in mapping.items():
            content = path.read_text(encoding='utf-8')
            if path.name == 'entrypoint.md' and path != entry:
                content = content.split('---', 2)[2].lstrip()
            if path.suffix == '.md':
                def rewrite(match):
                    link = match[2]
                    if '://' in link or link.startswith('#'):
                        return match[0]
                    base, separator, anchor = link.partition('#')
                    target = (path.parent / base).resolve()
                    if target not in mapping:
                        raise ValueError(f'Unbundled link in {path}: {link}')
                    new = Path(os.path.relpath(mapping[target], dest.parent)).as_posix()
                    return match[1] + new + (separator + anchor if separator else '') + match[3]
                content = LINK.sub(rewrite, content)
            if path == entry:
                _, metadata, body = content.split('---', 2)
                content = '---' + metadata + '---\n\n' + (
                    'This skill is independently installable. Supporting workflows and tools are bundled locally; '
                    'follow their links only when needed. Companion skills do not need to be installed. '
                    'Use bundled procedures directly when this workflow calls for them.\n') + '\n' + body.lstrip()
            result[Path(skill) / dest] = content.encode('utf-8')
    return result


def synchronize(output, files, check=False):
    existing = {p.relative_to(output) for p in output.rglob('*') if p.is_file()
                and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    changed = [path for path, content in files.items()
               if not (output / path).is_file() or (output / path).read_bytes() != content]
    obsolete = existing - files.keys()
    if check:
        for path in sorted(set(changed) | obsolete):
            print(f'Out of date: {path}', file=sys.stderr)
        return not (changed or obsolete)
    for path in obsolete:
        (output / path).unlink()
    for path in changed:
        (output / path).parent.mkdir(parents=True, exist_ok=True)
        (output / path).write_bytes(files[path])
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed bundles need regeneration')
    args = parser.parse_args()
    try:
        success = synchronize(OUTPUT, planned_files(), args.check)
    except (ValueError, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    if success:
        print('Five standalone skill bundles are up to date.')
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
