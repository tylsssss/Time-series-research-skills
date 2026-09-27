# Personal Research Priors

This is the shipped `default` profile: **no preferences are configured.**

The canonical gate rules and the evidence hierarchy in `SKILL.md` are unaffected by this
file and always apply. What is absent here is only the personal layer — the tie-breakers
used when several alternatives are equally compatible with the evidence.

## Contents

1. Authority and Decision Philosophy
2. Evidence and Attribution Preferences
3. Logic and Innovation Preferences
4. Feasibility and Selection Preferences
5. Rejection and Update Protocol

## 1. Authority and Decision Philosophy

No confirmed preference. Until this section is filled in, resolve every choice by
evidence, task constraints, and the canonical gates alone, and record the tie-break as
`NO-PERSONAL-PREFERENCE` in the dossier rather than inventing a preference.

## 2. Evidence and Attribution Preferences

No confirmed preference.

## 3. Logic and Innovation Preferences

No confirmed preference.

## 4. Feasibility and Selection Preferences

No confirmed preference.

## 5. Rejection and Update Protocol

Add a permanent prior only after you have explicitly confirmed it, one block per prior:

```text
Prior:
Type: HARD-GATE | DEFAULT-PREFERENCE | REJECTION
Source:
Scope:
Rationale:
Exceptions:
Conflicts:
Last confirmed:
```

Guidance for writing your own:

* state each prior as a rule that selects between alternatives that already satisfy the
  evidence, never as a rule that overrides it;
* give it a scope narrow enough to be wrong in a describable situation;
* keep `HARD-GATE` rare — a hard gate that evidence cannot satisfy makes the workflow
  unusable rather than rigorous;
* preserve unresolved conflicts between priors instead of silently resolving them;
* do not generalize a prior from one successful project.
