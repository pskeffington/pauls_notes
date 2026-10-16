#!/usr/bin/env bash
# Build APA examples in an isolated directory; publish only a successful PDF.
set -euo pipefail
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
output_dir=
name=Example_APA_7_Manuscript
bib=Example_References.bib
while [[ $# -gt 0 ]]; do
  case "$1" in
    --output-dir) [[ $# -ge 2 ]] || { printf 'Missing output directory\n' >&2; exit 2; }; output_dir=$2; shift 2 ;;
    *) printf 'Usage: bash compile_manuscript.sh --output-dir new-directory\n' >&2; exit 2 ;;
  esac
done
[[ -n "$output_dir" ]] || { printf 'Supply --output-dir new-directory\n' >&2; exit 2; }
[[ ! -e "$output_dir" && ! -L "$output_dir" ]] || { printf 'Output already exists: %s\n' "$output_dir" >&2; exit 2; }
[[ -d $(dirname -- "$output_dir") ]] || { printf 'Output parent must exist\n' >&2; exit 2; }
output_parent=$(cd -- "$(dirname -- "$output_dir")" && pwd -P)
output_dir="$output_parent/$(basename -- "$output_dir")"
repo_dir=$(cd -- "$source_dir/../.." && pwd -P)
case "$output_dir/" in
  "$repo_dir/"*) printf 'Choose an output directory outside the repository\n' >&2; exit 2 ;;
esac
[[ -f "$source_dir/$name.tex" && -f "$source_dir/$bib" ]] || { printf 'Missing manuscript source or bibliography\n' >&2; exit 1; }
for cmd in pdflatex biber kpsewhich; do
  command -v "$cmd" >/dev/null 2>&1 || { printf 'Missing tool: %s\n' "$cmd" >&2; exit 1; }
done
for pkg in biblatex.sty apa.bbx csquotes.sty babel.sty mathptmx.sty; do
  [[ -n $(kpsewhich "$pkg") ]] || { printf 'Missing TeX package: %s\n' "$pkg" >&2; exit 1; }
done
apa_build_dir=$(mktemp -d "${TMPDIR:-/tmp}/apa-build.XXXXXX")
trap 'rm -rf -- "$apa_build_dir"' EXIT
cp -- "$source_dir/$name.tex" "$source_dir/$bib" "$apa_build_dir/"
cd -- "$apa_build_dir"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
mkdir -p "$apa_build_dir/biber-runtime"
PAR_GLOBAL_TEMP="$apa_build_dir/biber-runtime" biber --validate-datamodel "$name"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
pdflatex -interaction=nonstopmode -halt-on-error "$name.tex"
if grep -E 'Citation .* undefined|There were undefined references|Please \(re\)run Biber' "$name.log"; then
  printf 'Unresolved bibliography or references\n' >&2
  exit 1
fi
[[ -s "$name.pdf" ]] || { printf 'Build produced no PDF\n' >&2; exit 1; }
# Reserve a new destination; an existing directory is never reused.
mkdir -- "$output_dir"
if ! cp -- "$name.pdf" "$output_dir/$name.pdf"; then
  rm -f -- "$output_dir/$name.pdf"
  rmdir -- "$output_dir"
  exit 1
fi
printf 'Built %s.pdf from %s in an isolated directory.\n' "$name" "$bib"
