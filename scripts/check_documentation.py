#!/usr/bin/env python3
"""Check local Markdown navigation and the integrated breast cancer book."""
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / '06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md'
IGNORED_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules',
                'outputs', 'figures', '.cache', '.pytest_cache'}
SOURCE_PATH = re.compile(
    r'(?<![\w/])(?:scripts|0[1-6]_[A-Za-z_]+)/[A-Za-z0-9_./-]+\.(?:py|R|sh|tex|bib)\b')


def source_files(root):
    """Walk source without descending into local environments or outputs."""
    import os
    for directory, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIRS)
        for name in sorted(files):
            yield Path(directory) / name


def anchors(path):
    result = set()
    counts = {}
    fenced = False
    for line in path.read_text().splitlines():
        if line.startswith(('```', '~~~')):
            fenced = not fenced
        if not fenced:
            result.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', line))
        if fenced or not re.match(r'^#{1,6} ', line):
            continue
        title = re.sub(r'^#+ ', '', line).strip()
        title = re.sub(r'<[^>]+>', '', title).lower()
        title = ''.join(c for c in title if c in ' -_' or unicodedata.category(c)[0] in 'LN')
        slug = title.replace(' ', '-')
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f'{slug}-{n}')
    return result


def check_navigation(root):
    errors = []
    pages = sorted(p for p in source_files(root) if p.suffix == '.md')
    for page in pages:
        text = page.read_text(encoding='utf-8')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            if re.match(r'\w+://|mailto:', target):
                continue
            path, _, fragment = target.partition('#')
            dest = (page.parent / unquote(path)).resolve() if path else page
            if not dest.exists():
                errors.append(f'{page.relative_to(root)}: missing {target}')
            elif fragment and dest.suffix == '.md' and unquote(fragment) not in anchors(dest):
                errors.append(f'{page.relative_to(root)}: missing anchor {target}')
        # Repository-qualified commands and source() paths must also resolve.
        # Exclude external URLs; they are not repository-relative references.
        local_text = re.sub(r'https?://[^\s)>]+', '', text)
        for target in sorted(set(SOURCE_PATH.findall(local_text))):
            if not (root / target).is_file():
                errors.append(f'{page.relative_to(root)}: missing source {target}')
    return pages, errors


def main():
    pages, errors = check_navigation(ROOT)
    text = BOOK.read_text()
    genes = re.findall(r'^#### ([A-Z][A-Z0-9]+)$', text, re.M)
    if len(set(genes)) != 60 or len(genes) != 60:
        errors.append('Book must retain exactly 60 integrated gene profiles')
    if len(re.findall(r'^## Chapter \d+:', text, re.M)) != 12:
        errors.append('Book must retain 12 chapters')
    learning = ROOT / '03_learning'
    for name in ('README.md', 'objects-and-meaning.md', 'keys-and-reshaping.md',
                 'missingness-and-comparisons.md', 'models-and-uncertainty.md',
                 'figures-and-features.md', 'probability-and-design.md', 'run-and-package.md',
                 'mastery-checks.md'):
        path = learning / name
        if not path.is_file():
            errors.append(f'Missing learning section: {name}')
    home = (ROOT / 'README.md').read_text()
    if 'Authored by Paul Skeffington · Compiled with OpenAI' not in home:
        errors.append('Missing front-page attribution')
    if re.search(r'dartmouth|university|institution|authentic|independently|copyright clearance|official curriculum', home, re.I):
        errors.append('Unexpected front-page identity or authenticity language')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(pages)} Markdown pages, local links and anchors; 12 chapters; 60 gene profiles')


if __name__ == '__main__':
    main()
