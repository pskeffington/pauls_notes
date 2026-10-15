#!/usr/bin/env bash
# Local, offline regression tests for the standalone synthetic-data example.
set -euo pipefail

module_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
script="$module_dir/examples/summarize_metadata.sh"
bash -n "$script"

scratch=$(mktemp -d "${TMPDIR:-/tmp}/pauls-notes-test.XXXXXX")
cleanup() {
  if [[ -n "${scratch:-}" && -d "$scratch" ]]; then
    rm -rf "$scratch"
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

input="$scratch/sample input.tsv"
output="$scratch/group summary.tsv"
expected="$scratch/expected.tsv"
printf 'Sample_ID\tGroup\tValue\nS01\tControl\t0.7\nS02\tTreatment\tNA\nS03\tControl\t1.2\nS04\tTreatment\t0.9\nS05\tTreatment\t1.1\n' > "$input"
cp "$input" "$scratch/unchanged.tsv"
printf 'Group\tn_total\tn_measured\tn_missing\nControl\t2\t2\t0\nTreatment\t3\t2\t1\n' > "$expected"
bash "$script" "$input" "$output" > /dev/null
cmp -s "$output" "$expected" || { printf 'Wrong summary\n' >&2; exit 1; }
cmp -s "$input" "$scratch/unchanged.tsv" || { printf 'Input mutated\n' >&2; exit 1; }

# Existing results must not be replaced.
if bash "$script" "$input" "$output" > /dev/null 2>&1; then
  printf 'Overwriting existing output was incorrectly permitted\n' >&2
  exit 1
fi
cmp -s "$output" "$expected" || { printf 'Existing output changed\n' >&2; exit 1; }

assert_rejected() {
  local label=$1
  local bad_input=$2
  local candidate="$scratch/rejected-$label.tsv"
  if bash "$script" "$bad_input" "$candidate" > /dev/null 2>&1; then
    printf 'Accepted invalid case: %s\n' "$label" >&2
    exit 1
  fi
  if [[ -e "$candidate" ]]; then
    printf 'Published invalid result: %s\n' "$label" >&2
    exit 1
  fi
}

printf 'bad\theader\n' > "$scratch/bad-header.tsv"
assert_rejected header "$scratch/bad-header.tsv"
printf 'Sample_ID\tGroup\tValue\nA\tControl\t1\nA\tTreatment\t2\n' > "$scratch/duplicate.tsv"
assert_rejected duplicate "$scratch/duplicate.tsv"
printf 'Sample_ID\tGroup\tValue\nA\tControl\t1\nB\tUnknown\t2\n' > "$scratch/bad-group.tsv"
assert_rejected group "$scratch/bad-group.tsv"
printf 'Sample_ID\tGroup\tValue\nA\tControl\tNaN\nB\tTreatment\t2\n' > "$scratch/bad-value.tsv"
assert_rejected value "$scratch/bad-value.tsv"
printf 'Sample_ID\tGroup\tValue\nA\tControl\t1\n' > "$scratch/one-group.tsv"
assert_rejected group-count "$scratch/one-group.tsv"
printf 'Sample_ID\tGroup\tValue\n' > "$scratch/empty.tsv"
assert_rejected empty "$scratch/empty.tsv"
assert_rejected missing "$scratch/not-present.tsv"

if command -v shellcheck > /dev/null 2>&1; then
  shellcheck "$script" "$0"
else
  printf 'ShellCheck not installed: optional lint skipped\n'
fi
printf 'PASS: Bash syntax, known result, unchanged input, and 7 rejection cases\n'
