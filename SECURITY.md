# Security Policy

## What this project is

This repository ships Markdown instructions, a dependency-free Python eval runner, and
two Node scripts. It runs no server, ships no executable artifact to end users, and
collects no data.

## Supported versions

Only the latest tagged release and the default branch are supported.

## Reporting a vulnerability

Report privately through GitHub: **Security → Report a vulnerability** on this
repository, or by email to **sazhang@bjtu.edu.cn**. Do not open a public issue for a
security problem. Please include the
affected file, a reproduction, and the impact you believe it has. Expect an initial
response within a week.

## In scope

* **Installer path handling.** `scripts/install.sh` writes into a user's skill
  directories. Unsafe path construction, symlink traversal, or a destructive default
  (overwriting without a backup) is a real vulnerability. It must stay safe under
  `--dry-run` and must never delete anything it did not create.
* **Bundle builder inlining.** `scripts/build-bundle.mjs` copies referenced files into a
  single output document. Reading outside the skill directory, following an absolute
  path, or inlining a path that escapes the repository is in scope.
* **Prompt injection with real consequences.** A reference file, fixture, or contributed
  dossier that instructs an agent to exfiltrate data, run destructive commands, or
  bypass the skill's own gates is in scope. The skills are instruction surfaces, so
  contributed text is executable-ish content and is reviewed accordingly.
* **Credential handling in the eval runner.** Tier 2 reads API keys from environment
  variables. Keys must never be written to disk, echoed, logged, or embedded in a
  results file.

## Out of scope

* The quality or correctness of a dossier produced by a model. That is a behavioral bug
  — please use the *Behavioral failure* issue template instead, so it can be turned into
  an eval case.
* The accuracy of statements in `skills/*/evals/files/` fixtures about cited published
  work. Fixtures are synthetic test inputs, not claims; see NOTICE.
* Vulnerabilities in third-party model providers or agent platforms.
* A user's own profile content under `profiles/`, including anything a user swaps into
  the `personal-*.md` slots locally.

## Secrets hygiene

Nothing in this repository requires a secret to use. Tier 2 of the eval runner is
opt-in and reads `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `DEEPSEEK_API_KEY` from the
environment; it skips cleanly when they are absent. Never commit a key, a results file
containing a key, or a `.env` file — `.gitignore` covers the usual paths, but do not
rely on it.
