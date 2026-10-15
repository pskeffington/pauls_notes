#!/usr/bin/env bash
# Publish a synthetic R analysis only after the R process succeeds.
set -euo pipefail
if [[ $# -ne 1 ]]; then
  printf 'Usage: bash %s NEW_OUTPUT_DIRECTORY\n' "${0##*/}" >&2
  exit 2
fi
command -v Rscript >/dev/null 2>&1 || { printf 'Rscript is required\n' >&2; exit 2; }
case_source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
Rscript --vanilla "$case_source_dir/research_case.R" "$1"
