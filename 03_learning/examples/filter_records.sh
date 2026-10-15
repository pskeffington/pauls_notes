#!/usr/bin/env bash
# A deliberately constrained TSV filter: no quoted or embedded separators.
set -euo pipefail
fail() { printf 'Record filter: %s\n' "$1" >&2; exit 2; }
[[ $# -eq 3 ]] || fail 'expected INPUT.tsv PANEL NEW_OUTPUT.tsv'
source_file=$1
panel=$2
target_file=$3
[[ "$panel" == Alpha || "$panel" == Beta ]] || fail 'panel must be Alpha or Beta'
[[ -f "$source_file" && -r "$source_file" ]] || fail 'input is not readable'
[[ ! -e "$target_file" && ! -L "$target_file" ]] || fail 'output already exists'
target_dir=$(dirname -- "$target_file")
[[ -d "$target_dir" ]] || fail 'output parent does not exist'
staged=$(mktemp "$target_dir/.record-selection.XXXXXX")
trap 'rm -f -- "$staged"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
if ! LC_ALL=C awk -v chosen="$panel" '
BEGIN { FS = "\t" }
NR == 1 {
  if ($0 != "record_id\tpanel\tsignal_au") { bad = 1; exit 2 }
  print; next
}
{
  if (NF != 3 || $1 !~ /^[A-Za-z0-9_-]+$/ || seen[$1]++ ||
      ($2 != "Alpha" && $2 != "Beta") ||
      ($3 != "NA" && $3 !~ /^[+-]?[0-9]+([.][0-9]+)?$/)) { bad = 1; exit 2 }
  if ($2 == chosen) print
}
END { if (bad || NR == 0) exit 2 }
' "$source_file" > "$staged"; then
  fail 'input violates the TSV contract'
fi
[[ ! -e "$target_file" && ! -L "$target_file" ]] || fail 'output appeared during processing'
mv -- "$staged" "$target_file"
