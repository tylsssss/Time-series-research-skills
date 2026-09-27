# Pattern A — Unify Failures Through a Measurable Mechanism

## Route When

Use when several observed vulnerabilities or behaviors may arise from one localized intermediate mechanism.

```text
failures F1 ... Fk
-> independently measurable intermediate Z
-> an intervention on Z changes the failures as predicted
-> the repair targets Z rather than each surface symptom
```

## Structural Contract

- Define `Z` independently of the proposed repair and downstream metric.
- Show a shared prediction under `Z` and a different prediction under at least one rival.
- Localize `Z` directly and state which failures it does not explain.
- Control capacity, data access, and optimization effort when intervening on `Z`.
- Treat a new name or retrospective story without a differential prediction as a mismatch.

## Minimum Contrast

Measure `Z` in at least two exposing conditions. Compare one targeted intervention with a matched negative control and a symptom-specific or simple repair. Measure the intermediate separately from task performance.

## Reject or Return When

Reject or revisit the diagnosis when `Z` is absent, the failures do not vary as predicted, changing `Z` leaves the target behavior unchanged, a simpler rival explains the observations, or the repair works without affecting `Z`.

## Time-Series Hazards

Localize horizon, scale, variable, phase, regime, state, or optimization effects without renaming aggregate forecast error as a mechanism. Check that the measurement remains causal and available in the target regime.

