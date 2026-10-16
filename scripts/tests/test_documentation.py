"""Regression checks for documentation navigation and executable paths."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_documentation import check_navigation


class NavigationTests(unittest.TestCase):
    def test_commands_and_ignored_environments(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '.venv').mkdir()
            (root / '.venv/README.md').write_text('[broken](absent.md)')
            (root / 'README.md').write_text(
                '```bash\npython3 scripts/missing.py\n```\n'
                '[upstream](https://example.org/scripts/upstream.py)\n')
            pages, errors = check_navigation(root)
            self.assertEqual(len(pages), 1)
            self.assertEqual(errors, ['README.md: missing source scripts/missing.py'])
            (root / 'scripts').mkdir()
            (root / 'scripts/missing.py').write_text('pass\n')
            self.assertEqual(check_navigation(root)[1], [])

    def test_fragments_and_duplicate_headings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'README.md'
            page.write_text('<a id="start"></a>\n# Topic\n# Topic\n'
                            '[first](#start) [second](#topic-1) [bad](#absent)\n')
            self.assertEqual(check_navigation(root)[1], ['README.md: missing anchor #absent'])


if __name__ == '__main__':
    unittest.main()
