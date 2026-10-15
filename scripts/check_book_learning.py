#!/usr/bin/env python3
"""Offline learning-book completeness and evidence-boundary checks."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '06_RESOURCES/Genomics'


def inspect_book(book: str, register: str, evidence: str) -> list[str]:
    errors = []
    chapters = re.findall(r'^## Chapter (\d+):', book, re.M)
    if chapters != [str(n) for n in range(1, 13)]:
        errors.append('Expected twelve chapters in numerical order')
    profiles = re.findall(r'^#### ([A-Z][A-Z0-9]+)\n(.*?)(?=^#{1,4} |\Z)', book, re.M | re.S)
    symbols = [symbol for symbol, _ in profiles]
    if len(symbols) != 60 or len(set(symbols)) != 60:
        errors.append('Expected sixty distinct integrated profiles')
    for symbol, body in profiles:
        if len(body.strip()) < 500 or any(token not in body for token in
                ('Research focus:', 'Study context:', '**Evidence:**', '`ABSTRACT_ONLY`')):
            errors.append(f'Incomplete profile or changed review scope: {symbol}')
    lookup = re.search(r'^### Alphabetical gene lookup\n(.*?)(?=^### |\Z)', book, re.M | re.S)
    jumps = re.findall(r'\[([A-Z][A-Z0-9]+)\]\(#([a-z0-9]+)\)', lookup.group(1) if lookup else '')
    if jumps != [(s, s.lower()) for s in sorted(set(symbols))]:
        errors.append('Alphabetical lookup does not cover every profile exactly once')
    identities = re.findall(r'^\| \[([A-Z][A-Z0-9]+)\][^|]*\| HGNC:(\d+) \| \[(\d+)\][^|]*\| \[(ENSG\d+)\][^|]*\| ANNOTATION_VERIFIED \|', register, re.M)
    if len(identities) != 60 or {row[0] for row in identities} != set(symbols):
        errors.append('Annotation identity rows do not match the integrated catalog')
    for field in range(4):
        if len({row[field] for row in identities}) != len(identities):
            errors.append('Duplicate primary identity in annotation table')
    studies = re.findall(r'^## ([A-Z][A-Z0-9]+)\n(.*?)(?=^## |\Z)', evidence, re.M | re.S)
    if len(studies) != 60 or {symbol for symbol, _ in studies} != set(symbols):
        errors.append('Evidence entries do not match the integrated catalog')
    for symbol, body in studies:
        if '- State: `ABSTRACT_ONLY`' not in body or 'PRIMARY_EVIDENCE_VERIFIED' in body:
            errors.append(f'Changed literature review boundary: {symbol}')
        if not re.search(r'https://pubmed[.]ncbi[.]nlm[.]nih[.]gov/\d+/', body) or '- Limit:' not in body:
            errors.append(f'Missing primary reference or interpretation limit: {symbol}')
    if book.count('```mermaid') != 7:
        errors.append('Expected seven integrated conceptual or synthetic diagrams')
    for number in range(1, 8):
        caption = re.search(rf'\*\*Figure {number} caption\.\*\*(.*?)(?:\n\n|\Z)', book, re.S)
        if not caption or any(token not in caption.group(1) for token in ('**Inputs:**', '**Sources:**')):
            errors.append(f'Incomplete figure caption: {number}')
    if book.count('**Text equivalent:**') != 7:
        errors.append('Expected a text equivalent for each figure')
    for label in ('**Beginner:**', '**Biology-focused reader:**', '**Research-focused reader:**'):
        if label not in book:
            errors.append('Missing learning route: ' + label)
    for block in re.split(r'^## Chapter \d+:', book, flags=re.M)[1:]:
        if '[Return to contents](#contents)' not in block:
            errors.append('Chapter lacks a contents return link')
    return errors


def main() -> None:
    errors = inspect_book(
        (BASE / 'BREAST_CANCER_60_GENE_COMPANION.md').read_text(),
        (BASE / 'REFERENCES/ANNOTATION_SOURCE_REGISTER.md').read_text(),
        (BASE / 'REFERENCES/GENE_EVIDENCE_MATRIX.md').read_text())
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: book chapters, sixty profiles and identities, evidence scope, lookup, seven figures and learning routes')


if __name__ == '__main__':
    main()
