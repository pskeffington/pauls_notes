# Filesystem and navigation

**Question:** How can a command locate the intended file without modifying unrelated data?

A **terminal** is the interface that displays a command session. A **shell**, such as Bash, parses commands and launches programs. The **current working directory** is the base for relative paths. Unix-like systems organize paths as a tree rooted at `/`; a leading `/` makes a path absolute.

## Inspect before acting

~~~bash
pwd
printf 'Home: %s\n' "$HOME"
ls -la
~~~

The first command prints your current directory. `ls -la` also shows hidden directory entries; this is an inspection command, not a change. Do not infer that a file is safe or complete merely because it exists.

Relative paths depend on where the program runs. `data/observations.tsv` is resolved below the current directory, whereas `/tmp/observations.tsv` names an absolute location. `.` means the current directory and `..` its parent. Use tab completion and inspect paths before a write.

## Deliberately scoped practice

The commands below create a new temporary workspace and leave its location visible so you can inspect it. They do not operate on your home directory or existing research data.

~~~bash
practice=$(mktemp -d "${TMPDIR:-/tmp}/pauls-paths.XXXXXX") || exit 1
mkdir -p "$practice/inputs" "$practice/results"
printf 'record\n' > "$practice/inputs/example one.txt"
ls -l "$practice/inputs"
cat "$practice/inputs/example one.txt"
printf 'Workspace: %s\n' "$practice"
~~~

Why the quotes? Without them, a filename with spaces can undergo word splitting. In Bash, `"$practice/inputs/example one.txt"` remains one argument. ShellCheck's [SC2086 explanation](https://www.shellcheck.net/wiki/SC2086) documents this failure mode.

## Copying, moving, and removal

`cp` creates a copy; `mv` relocates or renames a directory entry. Either can replace an existing destination, depending on flags and conditions. For research inputs, prefer an **immutable source** plus a separately named output and verify the result before further processing. Do not use recursive deletion as a routine learning command. If a workspace needs removal, first print and validate its exact path; never build `rm -rf` from unchecked variables.

Avoid portability assumptions: macOS/BSD and GNU implementations may differ in flags and `stat` output. Use `man command` locally to confirm the utility on your machine.

## Research interpretation

The filesystem identifies where bytes are stored, not what they mean. Record paths, file formats, checksums when appropriate, software versions, and data permissions separately. A file's existence and a successful `cp` do not prove that its contents or scientific annotations are correct.

**References:** [Software Carpentry filesystem lesson](https://swcarpentry.github.io/shell-novice/02-filedir.html) · [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html) · [Source register](reference-register.md)

**Next:** [Streams and text tools](streams-and-text.md).
