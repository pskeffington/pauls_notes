#!/usr/bin/env python3
"""Offline integrity checks for the breast cancer ML evidence register."""
import csv
from datetime import date
from pathlib import Path
import re
from urllib.parse import urlparse

from check_documentation import anchors

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / '04_machine_learning/evidence/breast-cancer-studies.csv'
GUIDE = ROOT / '04_machine_learning/breast-cancer-evidence.md'
GUIDES = (GUIDE, ROOT / '04_machine_learning/recent-tuning-evidence.md')

FIELDS = ['id', 'year', 'citation', 'identifier', 'source_url', 'evidence_type', 'task',
          'study_family', 'review_level', 'artifact_status', 'artifact_url', 'artifact_version',
          'local_reproduction', 'local_application', 'checked_on']
REVIEWS = {'abstract', 'abstract_artifact_docs', 'selected_methods_availability',
           'selected_source', 'selected_methods', 'abstract_guidance'}
ARTIFACTS = {'archive_docs_read', 'commercial_not_reviewed', 'not_reviewed',
             'proprietary_statement_read', 'selected_source_read', 'partial_readme_read', 'not_applicable'}
DESIGNS = {'prospective_observational', 'randomized_secondary_report', 'randomized_primary_report',
           'external_validation', 'retrospective_external_validation', 'preprint_external_report',
           'methodological', 'methodological_review', 'reporting_guidance', 'appraisal_guidance'}


def read_guides():
    return '\n'.join(path.read_text(encoding='utf-8') for path in GUIDES)


def inspect(rows, guide, root, today=None):
    today = today or date.today()
    errors, seen_ids, seen_citations = [], set(), set()
    card_ids = re.findall(r'^## (BC-(?:\d{2}|M\d{2}))$', guide, re.M)
    if len(card_ids) != len(set(card_ids)):
        errors.append('Duplicate evidence card heading')
    for number, row in enumerate(rows, start=2):
        if set(row) != set(FIELDS) or any(value is None for value in row.values()):
            errors.append(f'Row {number}: malformed register fields')
            continue
        label = row['id'] or f'row {number}'
        required = set(FIELDS) - {'artifact_url', 'artifact_version'}
        if any(not row[key].strip() for key in required):
            errors.append(f'{label}: missing required metadata')
        if not re.fullmatch(r'BC-(?:\d{2}|M\d{2})', row['id']) or row['id'] in seen_ids:
            errors.append(f'{label}: invalid or duplicate ID')
        seen_ids.add(row['id'])
        identifier = row['identifier'].lower()
        if identifier in seen_citations or not re.fullmatch(r'(?:10\.\d{4,9}/\S+|arxiv:\d{4}\.\d{4,5}v\d+|(?:jmlr|pmlr):\d+/[a-z0-9-]+)', identifier):
            errors.append(f'{label}: invalid or duplicate publication identifier')
        seen_citations.add(identifier)
        try:
            checked = date.fromisoformat(row['checked_on'])
            if checked > today or not 1900 <= int(row['year']) <= checked.year:
                raise ValueError
        except ValueError:
            errors.append(f'{label}: invalid review date or publication year')
        for key in ('source_url', 'artifact_url'):
            if row[key] and (urlparse(row[key]).scheme != 'https' or not urlparse(row[key]).netloc):
                errors.append(f'{label}: {key} requires an HTTPS URL')
        if row['review_level'] not in REVIEWS or row['artifact_status'] not in ARTIFACTS:
            errors.append(f'{label}: undeclared review or artifact status')
        if row['evidence_type'] not in DESIGNS:
            errors.append(f'{label}: undeclared study design')
        if row['artifact_status'].endswith('_read') and not all(row[k] for k in ('artifact_url', 'artifact_version')):
            errors.append(f'{label}: inspected artifact needs a URL and version')
        if row['evidence_type'] == 'preprint_external_report' and not identifier.startswith('arxiv:'):
            errors.append(f'{label}: preprint needs a versioned identifier')
        if row['local_reproduction'] != 'not_run':
            errors.append(f'{label}: reproduction claim needs a separately implemented evidence contract')
        target, _, fragment = row['local_application'].partition('#')
        destination = (root / target).resolve()
        if not destination.is_relative_to(root.resolve()) or not destination.is_file():
            errors.append(f'{label}: missing repository application')
        elif fragment and (destination.suffix != '.md' or fragment not in anchors(destination)):
            errors.append(f'{label}: missing application anchor')
        if row['id'] not in card_ids:
            errors.append(f'{label}: missing evidence card')
    if not rows or set(card_ids) != seen_ids:
        errors.append('Register and evidence cards must cover the same nonempty ID set')
    return errors


def main():
    with REGISTER.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise SystemExit('Unexpected evidence register header')
        rows = list(reader)
    errors = inspect(rows, read_guides(), ROOT)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {len(rows)} ML evidence records; citation IDs, review states, dates, cards and local applications')


if __name__ == '__main__':
    main()
