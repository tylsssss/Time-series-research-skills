---
name: Behavioral failure
about: The skill produced a dossier that violates its own contract
title: "[behavior] "
labels: [behavior, needs-triage]
---

A behavioral failure is the most valuable bug report this repository can receive. The
whole point of the project is that its rules are enforceable, so a dossier that breaks
them is a real defect — not a matter of taste.

## What violated the contract

<!-- Check every box that applies. -->

- [ ] A gate was passed while decision-relevant evidence was still `UNRESOLVED`
- [ ] A planned or running experiment (`PENDING`) was used as supporting evidence
- [ ] A numeric novelty score or an aggregate gate score was emitted
- [ ] A `NOT-STARTED` section instantiated records it should not have
- [ ] A candidate, `SYS-*`, or `COMP-*` was invented to justify a preferred module
- [ ] A claim appeared in sections 14–16 that is absent from sections 2–13
- [ ] An ID was renumbered after being referenced
- [ ] A personal pattern card, or a public pattern card, was used as evidence
- [ ] Something else (describe below)

## Reproduction

**Exact prompt sent** (include the entry mode and any constraints):

```text

```

**Model and interface** (for example: Claude Sonnet 4.5 via Claude Code, GPT-5 via
Codex, or a raw API call):

```text

```

**Skill version** (tag or commit):

```text

```

## Offending excerpt

<!-- Paste the smallest excerpt that shows the violation, with its section number and
     the relevant ID. Redact anything you do not want public. -->

```markdown

```

## Tier-1 report, if you ran it

```text
$ python3 evals/run.py --grade <your-dossier>.md
```

```text

```

## What you expected instead

<!-- Which rule did you expect to bind, and where is it written? -->
