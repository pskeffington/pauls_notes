#!/usr/bin/env bash
# Independent practice example: summarize a deliberately limited synthetic TSV.
# Requires Bash 3.2+, awk, mktemp, dirname, and mv.
set -euo pipefail

fail() {
  printf 'Error: %s\n' "$1" >&2
  exit 2
}

if [[ $# -ne 2 ]]; then
  printf 'Usage: bash %s INPUT.tsv OUTPUT.tsv\n' "${0##*/}" >&2
  exit 2
fi

input=$1
output=$2
[[ -f "$input" && -r "$input" ]] || fail 'Input must be a readable regular file'
[[ ! -e "$output" && ! -L "$output" ]] || fail 'Output already exists; refusing to overwrite'
output_dir=$(dirname "$output")
[[ -d "$output_dir" && -w "$output_dir" ]] || fail 'Output directory must exist and be writable'

tmp=$(mktemp "$output_dir/.metadata-summary.XXXXXX") || fail 'Could not create temporary output'
cleanup() {
  if [[ -n "${tmp:-}" && -e "$tmp" ]]; then
    rm -f "$tmp"
  fi
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

tab=$(printf '\t')
LC_ALL=C awk -F "$tab" '
  BEGIN { OFS = FS }
  NR == 1 {
    if (NF != 3 || $1 != "Sample_ID" || $2 != "Group" || $3 != "Value") {
      print "Invalid TSV header" > "/dev/stderr"
      bad = 1
      exit 2
    }
    next
  }
  {
    if (NF != 3 || $1 !~ /^[A-Za-z0-9][A-Za-z0-9_-]*$/) {
      print "Invalid record or sample ID at line " NR > "/dev/stderr"
      bad = 1
      exit 2
    }
    if (seen[$1]++) {
      print "Duplicate sample ID at line " NR > "/dev/stderr"
      bad = 1
      exit 2
    }
    if ($2 != "Control" && $2 != "Treatment") {
      print "Unsupported group at line " NR > "/dev/stderr"
      bad = 1
      exit 2
    }
    if ($3 != "NA" && $3 !~ /^[0-9]+([.][0-9]+)?$/) {
      print "Invalid measurement at line " NR > "/dev/stderr"
      bad = 1
      exit 2
    }
    total[$2]++
    if ($3 == "NA") missing[$2]++
    else measured[$2]++
  }
  END {
    if (bad) exit 2
    if (NR < 2 || total["Control"] < 1 || total["Treatment"] < 1) {
      print "Expected data rows in both groups" > "/dev/stderr"
      exit 2
    }
    print "Group", "n_total", "n_measured", "n_missing"
    print "Control", total["Control"], measured["Control"] + 0, missing["Control"] + 0
    print "Treatment", total["Treatment"], measured["Treatment"] + 0, missing["Treatment"] + 0
  }
' "$input" > "$tmp" || fail 'TSV validation failed; output not published'

[[ ! -e "$output" && ! -L "$output" ]] || fail 'Output appeared during processing; refusing to overwrite'
mv "$tmp" "$output" || fail 'Could not publish the validated output'
tmp=''
printf 'Validated summary: %s\n' "$output"
