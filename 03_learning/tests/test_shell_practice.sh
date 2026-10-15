#!/usr/bin/env bash
set -euo pipefail
base=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
filter="$base/examples/filter_records.sh"
work=$(mktemp -d "${TMPDIR:-/tmp}/research-shell-check.XXXXXX")
trap 'rm -rf -- "$work"' EXIT
input="$work/source with spaces.tsv"
printf 'record_id\tpanel\tsignal_au\n01\tAlpha\t4\n02\tBeta\t8\n03\tAlpha\tNA\n04\tBeta\t10\n05\tAlpha\t6\n06\tBeta\t12\n' > "$input"
cp -- "$input" "$work/original.tsv"
cp -- "$input" "$work/copy.tsv"
mv -- "$work/copy.tsv" "$work/renamed.tsv"
cmp -- "$input" "$work/renamed.tsv"
[[ $(wc -l < "$input") -eq 7 ]]
[[ $(head -n 1 "$input") == $'record_id\tpanel\tsignal_au' ]]
[[ $(tail -n 1 "$input") == $'06\tBeta\t12' ]]
tail -n +2 "$input" | cut -f 2 | LC_ALL=C sort | uniq -c > "$work/counts.txt"
[[ $(awk '$2=="Alpha" {print $1}' "$work/counts.txt") -eq 3 ]]
[[ $(awk '$2=="Beta" {print $1}' "$work/counts.txt") -eq 3 ]]
grep -q Alpha "$input"
if grep -q Gamma "$input"; then exit 1; else [[ $? -eq 1 ]]; fi
if grep -q Alpha "$work/absent.tsv" 2>/dev/null; then exit 1; else [[ $? -eq 2 ]]; fi
if (set -o pipefail; false | cat >/dev/null); then exit 1; else [[ $? -ne 0 ]]; fi
for panel in Alpha Beta; do
  bash "$filter" "$input" "$panel" "$work/$panel.tsv"
  [[ $(wc -l < "$work/$panel.tsv") -eq 4 ]]
done
printf 'record_id\tpanel\tsignal_au\n01\tAlpha\t4\n03\tAlpha\tNA\n05\tAlpha\t6\n' > "$work/expected.tsv"
cmp -- "$work/Alpha.tsv" "$work/expected.tsv"
# Calling bash does not need an executable bit; direct execution does.
cp -- "$filter" "$work/executable filter.sh"
chmod u+x "$work/executable filter.sh"
"$work/executable filter.sh" "$input" Beta "$work/direct-execution.tsv"
cmp -- "$work/direct-execution.tsv" "$work/Beta.tsv"
count_panel() {
  [[ $# -eq 2 && -f "$1" ]] || return 2
  [[ "$2" == Alpha || "$2" == Beta ]] || return 2
  awk -F '\t' -v panel="$2" 'NR>1 && $2==panel {n++} END {print n+0}' "$1"
}
[[ $(count_panel "$input" Alpha) -eq 3 ]]
if count_panel "$input" Unsupported >/dev/null; then exit 1; else [[ $? -eq 2 ]]; fi
# Header-only selection is valid and does not invent a record.
printf 'record_id\tpanel\tsignal_au\nOnly\tBeta\t2\n' > "$work/beta-only.tsv"
bash "$filter" "$work/beta-only.tsv" Alpha "$work/empty-selection.tsv"
[[ $(wc -l < "$work/empty-selection.tsv") -eq 1 ]]
reject() {
  if bash "$filter" "$@" > /dev/null 2>&1; then
    printf 'Accepted invalid filter invocation\n' >&2; exit 1
  fi
}
reject "$input" Alpha "$work/Alpha.tsv"
cmp -- "$work/Alpha.tsv" "$work/expected.tsv"

reject "$input" Alpha "$input"
ln -s "$input" "$work/input-link.tsv"
reject "$input" Alpha "$work/input-link.tsv"
reject "$input" Unsupported "$work/no-category.tsv"
reject "$input" Alpha
reject "$work/missing.tsv" Alpha "$work/no-input.tsv"
for type in duplicate header value category fields; do
  case "$type" in
    duplicate) printf 'record_id\tpanel\tsignal_au\nX\tAlpha\t4\nX\tBeta\t6\n' ;;
    header) printf 'wrong\tpanel\tsignal_au\nX\tAlpha\t4\n' ;;
    value) printf 'record_id\tpanel\tsignal_au\nX\tAlpha\tNaN\n' ;;
    category) printf 'record_id\tpanel\tsignal_au\nX\tOther\t4\n' ;;
    fields) printf 'record_id\tpanel\tsignal_au\nX\tAlpha\t4\textra\n' ;;
  esac > "$work/$type.tsv"
  reject "$work/$type.tsv" Alpha "$work/rejected-$type.tsv"
  [[ ! -e "$work/rejected-$type.tsv" ]]
done
cmp -- "$input" "$work/original.tsv"
# A real quoted CSV field is one field to a CSV parser, not to naive comma splitting.
printf 'id,label\n01,"two, words"\n' > "$work/quoted.csv"
[[ $(tail -n 1 "$work/quoted.csv" | awk -F, '{print NF}') -eq 3 ]]
if command -v Rscript >/dev/null 2>&1; then
  Rscript --vanilla "$base/tests/test_signal_bridge.R" "$input" "$work"
fi
printf 'PASS: shell paths, counts, search statuses, pipe failures, filtering, missing values, empty selection, rejection and unchanged inputs\n'
