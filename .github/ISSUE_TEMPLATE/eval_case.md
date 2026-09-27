---
name: Eval case proposal
about: Propose a new behavioral eval case, or a fix to an existing expectation
title: "[eval] "
labels: [evals]
---

The eval suite is how this project's claims stay checkable. Every behavior change is
supposed to arrive with an expectation; this template is for proposing one on its own.

## What behavior needs coverage

<!-- One paragraph. What should the skill do (or refuse to do) that no current case
     checks? -->

## Which entry mode and stage

- Entry mode: `GENERATE` / `AUDIT` / `REPAIR` / `COMPARE`
- Phase boundary (where the run should stop): `DIAGNOSIS` / `INDEPENDENT-IDEATION` /
  `AUDIT` / `COMPILATION`

## Draft case

```json
{
  "id": 0,
  "prompt": "",
  "expected_output": "",
  "files": [],
  "expectations": [
    ""
  ]
}
```

## Why the existing cases do not already cover it

<!-- Cases 1-12 are listed in the README. If an existing case nearly covers this,
     propose tightening that expectation instead of adding a thirteenth. -->

## Is this expectation checkable without a model call?

<!-- If yes, it can join Tier 1 (offline, CI). Describe the structural signal:
     a heading, a field value, an ID namespace, an enum, a forbidden token. -->

## Costs

<!-- Approximate prompt length, whether a fixture file is needed, and whether the
     case requires an unusually long context. -->
