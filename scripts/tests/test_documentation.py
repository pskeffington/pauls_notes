"""Regression checks for documentation navigation and executable paths."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_documentation import check_navigation, unsupported_front_page_claims


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

    def test_git_sign_in_terms_not_blocked_on_front_page(self):
        language = ('Sign in to GitHub; configure authentication; '
                    'the authenticated client uses a credential helper. '
                    'Authenticate without including a password.')
        self.assertEqual(unsupported_front_page_claims(language), [])

    def test_prohibited_identity_claims_remain_blocked(self):
        cases = (
            'college affiliation',
            'a university class',
            'institutional endorsement',
            'authentic research curriculum',
            'authenticity guarantee',
            'independently approved',
            'copyright clearance',
            'official curriculum',
        )
        for case in cases:
            with self.subTest(case=case):
                self.assertTrue(unsupported_front_page_claims(case))

    def test_fragments_and_duplicate_headings(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            page = root / 'README.md'
            page.write_text('<a id="start"></a>\n# Topic\n# Topic\n'
                            '[first](#start) [second](#topic-1) [bad](#absent)\n')
            self.assertEqual(check_navigation(root)[1], ['README.md: missing anchor #absent'])


if __name__ == '__main__':
    unittest.main()
