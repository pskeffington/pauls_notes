# Git and GitHub from zero to your first push

[Paul's Notes](../README.md) · [Unix and Bash](../01_unix_bash/README.md) · [Contributing](../CONTRIBUTING.md)

**Goal:** Install the tools, identify yourself, get a repository, change a file, commit locally, push to GitHub, and open a pull request. Examples use a terminal in macOS, Linux, Windows PowerShell, or Git Bash; Unix-style `touch` is optional. **Git** tracks history on your computer; **GitHub** hosts repositories and collaborative review. `git commit` saves locally; `git push` sends commits to a remote.

## 1. Install and check

Install [Git](https://git-scm.com/downloads) and create a [GitHub account](https://github.com/signup). Optionally install [GitHub CLI (`gh`)](https://cli.github.com/) to sign in and create PRs in the terminal. On Windows, Git Bash provides a Unix-like command prompt; PowerShell works for the Git commands below.

```bash
git --version
gh --version     # optional; if not installed, use the GitHub website
```

Tell Git how to label **new commits** (this name/email appears in commit metadata; use an appropriate public or GitHub noreply email for public repositories):

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-noreply@example.com"
git config --global init.defaultBranch main
git config --list --show-origin
```

Replace placeholders with your actual values. Configure a GitHub [private/noreply commit email](https://docs.github.com/en/account-and-profile/how-tos/email-preferences/setting-your-commit-email-address) if you do not want a personal email in public history.

## 2. Sign in securely

For HTTPS repositories, use a supported Git credential helper, the GitHub CLI, or Git Credential Manager—not your GitHub account password pasted into Git. With `gh` installed:

```bash
gh auth login
gh auth status
```

Follow the interactive prompts. The GitHub CLI can configure Git HTTPS authentication. SSH is an alternative: create and register an SSH public key with GitHub before using an `git@github.com:OWNER/REPO.git` URL. Never paste tokens, private SSH keys, credentials, participant data, or research records into commits.

## 3. Choose one of two starting routes

### Route A: clone an existing repository (recommended for this project)

On GitHub, open the repository, select **Code**, copy its HTTPS URL, then in your terminal:

```bash
git clone https://github.com/OWNER/REPO.git
cd REPO
git remote -v
git status
```

Replace `OWNER/REPO` with the repository you have permission to access. You need write permission to push to that repository; otherwise use a fork or your own repository.

### Route B: start a brand-new repository

Create an **empty** repository on GitHub first (avoid adding a remote README/license if you have already created them locally), then:

```bash
mkdir my-first-repo
cd my-first-repo
git init -b main
git config --get user.name
git config --get user.email
printf "# My first repository\n" > README.md
git add README.md
git commit -m "docs: add first README"
git remote add origin https://github.com/OWNER/my-first-repo.git
git push -u origin main
```

This is the shortest complete first-push path. `-u` records the remote tracking branch, so later `git push` is usually enough. If the remote already contains a commit, **do not force push**; clone it or reconcile history instead.

## 4. The everyday change → commit → push workflow

For shared repositories, develop on a branch rather than assuming you can push straight to protected `main`:

```bash
git switch main
git pull --ff-only origin main
git switch -c docs/my-first-change
git status
# Edit a file using your text editor, then:
git diff
git add README.md
git diff --cached
git commit -m "docs: clarify the README"
git push -u origin docs/my-first-change
```

Next, open the URL GitHub prints after pushing or open **Pull requests → New pull request** on the GitHub website, compare `docs/my-first-change` into `main`, explain the change, and request review. With `gh`:

```bash
gh pr create --base main --head docs/my-first-change --fill
gh pr status
```

A PR is **not automatically merged**. Wait for required checks and review. After merge, synchronize your local copy:

```bash
git switch main
git pull --ff-only origin main
git branch -d docs/my-first-change
```

If you must amend a shared branch, coordinate before rewriting history. Never force push to shared/protected branches.

## 5. Essential command reference

| Command | Meaning / when to use |
| --- | --- |
| `pwd` / `ls` | Show your current directory / list files (PowerShell supports both aliases) |
| `cd folder` / `cd ..` | Enter a folder / move up |
| `git status` | See branch, modified files, staged files, and pending commits |
| `git clone URL` | Download an existing repository with history |
| `git init -b main` | Start Git tracking in a new local folder |
| `git remote -v` | See which GitHub URL is configured |
| `git remote add origin URL` | Attach a remote to a local repository |
| `git branch --show-current` | Check the current branch |
| `git switch -c BRANCH` | Create and switch to a new branch |
| `git switch BRANCH` | Change to an existing branch |
| `git diff` / `git diff --cached` | Inspect unstaged / staged changes |
| `git add PATH` | Stage a specific file (prefer over blindly staging all) |
| `git commit -m "message"` | Save staged changes as a local commit |
| `git log --oneline -5` | View recent commits |
| `git fetch origin` | Download remote changes without merging |
| `git pull --ff-only origin main` | Update local main only when a fast-forward is possible |
| `git push -u origin BRANCH` | Upload a branch and remember its upstream |
| `git push` | Upload new commits to the configured upstream |
| `gh pr create --base main --head BRANCH --fill` | Open a GitHub PR from terminal if CLI is installed |

## 6. What to do when something goes wrong

- **`fatal: not a git repository`** — `cd` to the cloned project directory; check for the hidden `.git` directory. Do not run `git init` inside an unrelated directory to silence the error.
- **`nothing to commit, working tree clean`** — no tracked changes are staged. Verify the file was saved and run `git status`.
- **`Author identity unknown`** — configure `user.name` and `user.email` from step 1.
- **Authentication failed / 403** — check `gh auth status`, credential-helper setup, remote URL, and write permissions. A password alone is not supported for Git HTTPS pushes.
- **`non-fast-forward` / rejected push** — fetch and inspect the remote changes. Integrate them safely; do not reflexively use `--force`.
- **Merge conflict** — open the conflicted files, choose the correct content, remove conflict markers, stage resolved files, and complete the merge or rebase only after checking tests.
- **Accidentally staged a file** — `git restore --staged PATH` removes it from the staging area **without deleting your working file**.
- **Secret committed** — deleting it in a later commit is not sufficient. Immediately revoke/rotate the credential, stop pushing, and follow the repository's incident/history-remediation process.

## 7. Research repository safety and a small exercise

Before `git add`, inspect `git status` and `git diff`. Keep `.env`, credentials, private keys, virtual environments, generated archives, large analysis outputs, controlled data, patient-linked records, and any source without publication permission **out of Git**. Use a reviewed `.gitignore` but remember that ignoring a file does not untrack files already committed. For Paul's Notes, use **synthetic, nonclinical examples only** unless independent dataset admission and privacy gates authorize a different workflow. Running `git push` publishes to the remote according to that repository's visibility and access controls.

**Practice challenge:** Clone a repository you can write to, create a `docs/practice` branch, change one harmless sentence in a README, run `git status` and `git diff`, stage the README only, commit, push the branch, and open a PR. Show that you can explain where each change lives: working tree → staging area → local commit → remote branch → reviewed merge.

**Completion check:** You can reproduce the workflow without copying a token into code, distinguish commit from push and push from PR merge, and recover safely from an uncommitted change or rejected push.

For official references, use [Pro Git](https://git-scm.com/book/en/v2), [GitHub's Git handbook](https://docs.github.com/en/get-started/using-git/about-git), and [GitHub CLI documentation](https://cli.github.com/manual/).
