#!/usr/bin/env bash
# Offline contract checks using tool stubs; these do not validate TeX layout.
set -euo pipefail
repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
builder="$repo_dir/06_RESOURCES/LaTeX/compile_manuscript.sh"
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/manuscript-tests.XXXXXX")
trap 'rm -rf -- "$test_dir"' EXIT
mkdir "$test_dir/bin"
cat > "$test_dir/bin/pdflatex" <<'EOF'
#!/usr/bin/env bash
set -eu
[[ ${MOCK_TEX_FAIL:-0} == 0 ]] || exit 1
printf 'Stub PDF for build-contract testing only\n' > Example_APA_7_Manuscript.pdf
printf 'Stub successful log\n' > Example_APA_7_Manuscript.log
EOF
cat > "$test_dir/bin/biber" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
cat > "$test_dir/bin/kpsewhich" <<'EOF'
#!/usr/bin/env bash
printf '/stub/package\n'
EOF
chmod +x "$test_dir/bin/"*
export PATH="$test_dir/bin:$PATH"
expect_failure() {
  if bash "$builder" "$@" > "$test_dir/log" 2>&1; then
    printf 'Expected failure: %s\n' "$*" >&2; exit 1
  fi
}
expect_failure
expect_failure --catalogue
expect_failure --output-dir "$repo_dir/outputs"
mkdir "$test_dir/existing"
printf 'keep\n' > "$test_dir/existing/sentinel"
expect_failure --output-dir "$test_dir/existing"
[[ $(cat "$test_dir/existing/sentinel") == keep ]]
ln -s "$test_dir/absent" "$test_dir/dangling"
expect_failure --output-dir "$test_dir/dangling"
export MOCK_TEX_FAIL=1
expect_failure --output-dir "$test_dir/failed"
[[ ! -e "$test_dir/failed" ]]
export MOCK_TEX_FAIL=0
bash "$builder" --output-dir "$test_dir/output with spaces" > "$test_dir/log"
[[ -s "$test_dir/output with spaces/Example_APA_7_Manuscript.pdf" ]]
expect_failure --output-dir "$test_dir/output with spaces"
printf 'PASS: manuscript build arguments, output protection and failure cleanup (stub tools)\n'
