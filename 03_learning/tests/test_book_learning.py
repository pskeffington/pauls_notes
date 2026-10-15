"""Negative cases for learning-book completeness; mutations stay in memory."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('book_check', ROOT / 'scripts/check_book_learning.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BASE = ROOT / '06_RESOURCES/Genomics'
BOOK = (BASE / 'BREAST_CANCER_60_GENE_COMPANION.md').read_text()
REGISTER = (BASE / 'REFERENCES/ANNOTATION_SOURCE_REGISTER.md').read_text()
EVIDENCE = (BASE / 'REFERENCES/GENE_EVIDENCE_MATRIX.md').read_text()


class BookLearningChecks(unittest.TestCase):
    def inspect(self, book=BOOK, register=REGISTER, evidence=EVIDENCE):
        return MODULE.inspect_book(book, register, evidence)

    def test_current_book(self):
        self.assertEqual(self.inspect(), [])

    def test_missing_chapter(self):
        self.assertTrue(self.inspect(book=BOOK.replace('## Chapter 3:', '## Removed 3:', 1)))

    def test_duplicate_gene(self):
        self.assertTrue(self.inspect(book=BOOK.replace('#### ATM\n', '#### AKT1\n', 1)))

    def test_missing_lookup(self):
        self.assertTrue(self.inspect(book=re.sub(r'^\| \[AKT1\]\(#akt1\)', '| AKT1', BOOK, count=1, flags=re.M)))

    def test_short_profile(self):
        shortened = re.sub(r'^#### AKT1\n.*?(?=^#### )', '#### AKT1\nShort.\n', BOOK, count=1, flags=re.M | re.S)
        self.assertTrue(self.inspect(book=shortened))

    def test_missing_identity(self):
        self.assertTrue(self.inspect(register=re.sub(r'^\| \[AKT1\].*\n', '', REGISTER, flags=re.M)))

    def test_duplicate_identity(self):
        ids = re.findall(r'HGNC:(\d+)', REGISTER)
        self.assertTrue(self.inspect(register=REGISTER.replace('HGNC:' + ids[1], 'HGNC:' + ids[0], 1)))

    def test_evidence_promotion(self):
        self.assertTrue(self.inspect(evidence=EVIDENCE.replace('- State: `ABSTRACT_ONLY`', '- State: `PRIMARY_EVIDENCE_VERIFIED`', 1)))

    def test_caption_and_accessibility(self):
        self.assertTrue(self.inspect(book=BOOK.replace('**Inputs:**', '**Omitted:**', 1)))
        self.assertTrue(self.inspect(book=BOOK.replace('**Text equivalent:**', '**Omitted:**', 1)))

    def test_route(self):
        self.assertTrue(self.inspect(book=BOOK.replace('**Beginner:**', '**Omitted:**', 1)))


if __name__ == '__main__':
    unittest.main()
