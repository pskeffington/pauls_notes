#!/usr/bin/env python3
"""Parse retained Python and Bash source without running examples."""
import ast
import subprocess
from check_documentation import ROOT, source_files


def main():
    errors = []
    count = 0
    for path in source_files(ROOT):
        if path.suffix == '.py':
            try:
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            except SyntaxError as exc:
                errors.append(str(exc))
            count += 1
        elif path.suffix == '.sh':
            result = subprocess.run(['bash', '-n', str(path)], capture_output=True, text=True)
            if result.returncode:
                errors.append(result.stderr.strip())
            count += 1
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: Python and Bash syntax in {count} source files')


if __name__ == '__main__':
    main()
