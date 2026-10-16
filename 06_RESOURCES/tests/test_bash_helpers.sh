#!/usr/bin/env bash
# Exercise helper contracts with paths containing spaces and no external data.
set -euo pipefail
source 06_RESOURCES/Bash/bash_functions.sh

test_dir=$(mktemp -d "${TMPDIR:-/tmp}/bash-helper-tests.XXXXXX")
trap 'rm -rf -- "$test_dir"' EXIT
table_path="$test_dir/input table.tsv"
printf 'id\tvalue\nA\t2\nB\t4\n' > "$table_path"
cp "$table_path" "$test_dir/original.tsv"
require_command awk
require_file "$table_path"
[[ $(count_tsv_records "$table_path") == 2 ]]
[[ $(list_tsv_columns "$table_path") == $'1\tid\n2\tvalue' ]]
fingerprint=$(file_sha256 "$table_path")
[[ ${fingerprint%% *} == $(file_sha256 "$test_dir/original.tsv" | awk '{print $1}') ]]
[[ ${#fingerprint} -ge 64 ]]
cmp "$table_path" "$test_dir/original.tsv"
printf 'id\tvalue\n' > "$test_dir/header.tsv"
: > "$test_dir/empty.tsv"
[[ $(count_tsv_records "$test_dir/header.tsv") == 0 ]]
[[ $(count_tsv_records "$test_dir/empty.tsv") == 0 ]]
if require_command a_command_that_does_not_exist 2>/dev/null; then exit 1; fi
if require_file "$test_dir/missing.tsv" 2>/dev/null; then exit 1; fi
if file_sha256 "$test_dir/missing.tsv" 2>/dev/null; then exit 1; fi
status=0
require_file 2>/dev/null || status=$?
[[ $status == 2 ]]

# A disposable interpreter records argv and lets us test failure propagation.
mkdir "$test_dir/bin"
cat > "$test_dir/bin/Rscript" <<'MOCK_RSCRIPT'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$ARGUMENT_CAPTURE"
exit "${INTERPRETER_STATUS:-0}"
MOCK_RSCRIPT
chmod +x "$test_dir/bin/Rscript"
script_path="$test_dir/analysis script.R"
: > "$script_path"
export ARGUMENT_CAPTURE="$test_dir/arguments.txt"
PATH="$test_dir/bin:$PATH" run_r_script "$script_path" 'two words' '--literal'
printf '%s\n' --vanilla "$script_path" 'two words' '--literal' > "$test_dir/expected.txt"
cmp "$ARGUMENT_CAPTURE" "$test_dir/expected.txt"
status=0
PATH="$test_dir/bin:$PATH" INTERPRETER_STATUS=7 run_r_script "$script_path" || status=$?
[[ $status == 7 ]]
if run_r_script "$test_dir/missing.R" 2>/dev/null; then exit 1; fi
printf 'PASS: Bash helpers, TSV counts, checksums, quoted arguments and interpreter failures\n'
