#!/usr/bin/env python3
"""Check Rust ML review provenance offline; this does not replicate studies."""
import csv
from collections import Counter
from datetime import date
from pathlib import Path
import re
from urllib.parse import urlparse

from check_documentation import anchors

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / '04_machine_learning/evidence/rust-ml-sources.csv'
GUIDE = ROOT / '04_machine_learning/rust-ml-literature.md'
BIBLIOGRAPHY = ROOT / '04_machine_learning/evidence/rust-ml-references.bib'
FIELDS = ['id', 'source_kind', 'year', 'citation', 'identifier', 'source_url',
          'review_url', 'reviewed_version', 'publication_status', 'study_family',
          'rust_role', 'review_scope', 'reviewed_sections', 'source_sha256',
          'artifact_url', 'artifact_revision', 'artifact_review', 'local_execution',
          'breast_cancer_validation', 'finding', 'limitation', 'project_decision',
          'local_application', 'checked_on']
PAPER_STATUSES = {'journal_article', 'conference_paper', 'preprint'}
SOURCE_SCOPES = {'selected_source', 'selected_documentation'}


def read_rows():
    with REGISTER.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('Unexpected Rust ML register header')
        return list(reader)


def inspect(rows, guide, root, bibliography, today=None):
    """Validate metadata relationships, never infer scientific validity from them."""
    today = today or date.today()
    errors, seen_ids, seen_identifiers, paper_keys = [], set(), set(), set()
    card_ids = re.findall(r'^## (RML-[PS]\d{2})$', guide, re.M)
    if len(card_ids) != len(set(card_ids)):
        errors.append('Duplicate Rust ML evidence card')
    # This is the repository's deliberately simple bibliography format, not a
    # general BibTeX parser. Each entry contains only braced scalar fields.
    entries = re.findall(r'^@(\w+)\{(RMLP\d{2}),\n(.*?)^\}', bibliography, re.M | re.S)
    bib = {}
    for entry_type, key, body in entries:
        if key in bib:
            errors.append(f'{key}: duplicate bibliography entry')
        bib[key] = (entry_type, dict(re.findall(r'^\s*(\w+)\s*=\s*\{([^\n]*)\},?$', body, re.M)))
    for number, row in enumerate(rows, start=2):
        if set(row) != set(FIELDS) or any(value is None for value in row.values()):
            errors.append(f'Row {number}: malformed Rust ML fields')
            continue
        label = row['id'] or f'row {number}'
        required = set(FIELDS) - {'artifact_url', 'artifact_revision'}
        if any(not row[key].strip() for key in required):
            errors.append(f'{label}: missing required provenance')
        kind = row['source_kind']
        prefix = {'paper': 'P', 'software': 'S'}.get(kind)
        if prefix is None or not re.fullmatch(rf'RML-{prefix}\d{{2}}', label) or label in seen_ids:
            errors.append(f'{label}: duplicate ID or source-kind mismatch')
        seen_ids.add(label)
        identifier = row['identifier'].lower()
        if identifier in seen_identifiers:
            errors.append(f'{label}: duplicate source identifier')
        seen_identifiers.add(identifier)
        try:
            checked = date.fromisoformat(row['checked_on'])
            if checked > today or not 2021 <= int(row['year']) <= checked.year:
                raise ValueError
        except ValueError:
            errors.append(f'{label}: invalid date or review-window year')
        for key in ('source_url', 'review_url', 'artifact_url'):
            parsed = urlparse(row[key])
            if row[key] and (parsed.scheme != 'https' or not parsed.netloc):
                errors.append(f'{label}: {key} requires HTTPS')
        if not re.fullmatch(r'[a-f0-9]{64}', row['source_sha256']):
            errors.append(f'{label}: invalid reviewed-source SHA256')
        if row['local_execution'] != 'not_run' or row['breast_cancer_validation'] != 'not_established':
            errors.append(f'{label}: execution or clinical-validation claim needs a separate validated contract')
        if kind == 'paper':
            if row['publication_status'] not in PAPER_STATUSES or row['review_scope'] not in {'selected_fulltext', 'abstract_only'}:
                errors.append(f'{label}: invalid paper status or review scope')
            preprint = row['publication_status'] == 'preprint'
            pattern = r'arxiv:\d{4}\.\d{4,5}v\d+' if preprint else r'10\.\d{4,9}/\S+'
            if not re.fullmatch(pattern, identifier):
                errors.append(f'{label}: paper needs a DOI or versioned preprint identifier')
            if row['artifact_revision'] or row['artifact_review'] not in {'pointer_only', 'not_reviewed'}:
                errors.append(f'{label}: paper artifact inspection requires its own evidence contract')
            if (row['artifact_review'] == 'pointer_only') != bool(row['artifact_url']):
                errors.append(f'{label}: artifact pointer and review status disagree')
            key = label.replace('-', '')
            paper_keys.add(key)
            entry_type, fields = bib.get(key, ('', {}))
            expected_type = {'journal_article': 'article', 'conference_paper': 'inproceedings', 'preprint': 'misc'}.get(row['publication_status'])
            if entry_type != expected_type or fields.get('year') != row['year'] or not all(fields.get(k) for k in ('author', 'title', 'url')):
                errors.append(f'{label}: missing or inconsistent bibliography metadata')
            if preprint:
                match = re.fullmatch(r'arxiv:(\d{4}\.\d{4,5})(v\d+)', identifier)
                if not match or fields.get('eprint') != match[1] or fields.get('url', '').lower() != row['source_url'].lower():
                    errors.append(f'{label}: bibliography preprint/version mismatch')
            elif fields.get('doi', '').lower() != identifier:
                errors.append(f'{label}: bibliography DOI mismatch')
        elif kind == 'software':
            pin = re.fullmatch(r'github:([^/]+/[^@]+)@([a-f0-9]{40})', row['identifier'])
            if row['publication_status'] != 'software_documentation' or row['review_scope'] not in SOURCE_SCOPES:
                errors.append(f'{label}: software is not a publication')
            if row['artifact_review'] != row['review_scope']:
                errors.append(f'{label}: software inspection scope mismatch')
            if not pin or row['artifact_revision'] != pin[2]:
                errors.append(f'{label}: inspected software needs an immutable commit')
            else:
                prefix_url = f'https://github.com/{pin[1]}/blob/{pin[2]}/'
                if not row['source_url'].startswith(prefix_url):
                    errors.append(f'{label}: source URL must name the inspected commit and file')
                else:
                    path = row['source_url'][len(prefix_url):]
                    expected_raw = f'https://raw.githubusercontent.com/{pin[1]}/{pin[2]}/{path}'
                    if not path or row['review_url'] != expected_raw:
                        errors.append(f'{label}: reviewed bytes must match the pinned source file')
                if row['artifact_url'] != row['source_url']:
                    errors.append(f'{label}: inspected artifact URL mismatch')
        target, _, fragment = row['local_application'].partition('#')
        destination = (root / target).resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.is_file():
            errors.append(f'{label}: missing repository application')
        elif fragment and (destination.suffix != '.md' or fragment not in anchors(destination)):
            errors.append(f'{label}: missing application anchor')
    if not rows or set(card_ids) != seen_ids:
        errors.append('Rust ML register and cards must cover the same nonempty ID set')
    if set(bib) != paper_keys:
        errors.append('Bibliography must cover exactly the publication records')
    return errors


def summary(rows):
    kinds = Counter(row['source_kind'] for row in rows)
    return f"{kinds['paper']} publications and {kinds['software']} software/documentation inspections"


def main():
    rows = read_rows()
    errors = inspect(rows, GUIDE.read_text(encoding='utf-8'), ROOT,
                     BIBLIOGRAPHY.read_text(encoding='utf-8'))
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: Rust ML {summary(rows)}; provenance, pins, cards and bibliography')


if __name__ == '__main__':
    main()
