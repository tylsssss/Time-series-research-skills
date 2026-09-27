# Delivery Report Template

Sole authority for the Phase 5 report structure in SKILL.md. Use these headings in this order; fill every section; do not add new top-level sections.

```markdown
# {{Method}} on {{Dataset}} — Implementation Report

## What was built

{{One paragraph: the frozen method, the file layout, and which Phase-0 SPEC this fulfills.}}

## How to run

```bash
{{exact commands: install, then run — nothing the user must guess}}
```

## Verification status

| Check | Status | Evidence |
|---|---|---|
| Smoke test (synthetic, shapes, finite loss) | PASS / FAIL / NOT-RUN | {{loss value or error}} |
| Overfit test (fits one small batch) | PASS / FAIL / NOT-RUN | {{final loss}} |
| Baseline sanity (beats persistence/mean/linear) | PASS / FAIL / NOT-RUN | {{numbers}} |
| Reference comparison (when reproducing) | MATCHED / GAP / N/A | {{published vs. ours}} |
| Real run (agreed seeds) | DONE / NOT-RUN | {{seeds used}} |

## Results

| Dataset | Method | Metric | mean ± std | Trivial baseline | Delta |
|---|---|---|---|---|---|
| {{dataset}} | {{method}} | MSE | {{x.xxx ± y.yyy}} | {{z.zzz}} | {{%}} |
| {{dataset}} | {{method}} | MAE | {{x.xxx ± y.yyy}} | {{z.zzz}} | {{%}} |

## Provenance

| Component | Source | Commit | License | Changes |
|---|---|---|---|---|
| {{component}} | {{repo URL or "written from scratch"}} | {{hash or —}} | {{license or —}} | {{what changed and why}} |

## Deviations from SPEC

{{Every difference between the frozen SPEC and the implementation, with the reason. "None" is a valid answer.}}

## Unverified / next steps

{{What still needs checking, and the smallest next action for each.}}
```

Rules:

- Report one row per dataset, never an average across heterogeneous datasets.
- State `FAIL` plainly when a check fails; the report is for the researcher, not a sales pitch.
- Quote exact commit hashes in Provenance; "borrowed from TSLib" without a hash is not provenance.
- If results contradict the original idea, say so in `## Deviations from SPEC` and `## Unverified / next steps` — do not bury it.
