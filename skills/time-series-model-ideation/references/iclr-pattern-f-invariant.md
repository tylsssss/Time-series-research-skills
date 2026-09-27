# Pattern F — Constrain Change to Preserve an Invariant

## Route When

Use when an otherwise useful update or transformation damages a separately measurable property needed elsewhere.

```text
change delta achieves target A
-> delta damages invariant I
-> restrict delta to feasible set S(I)
-> retain progress on A while bounding damage to I
```

## Structural Contract

- Define `I` independently of downstream performance.
- Establish that the unconstrained change damages `I`.
- Link preservation to task behavior through evidence or an explicit derivation.
- State whether preservation is exact, approximate, equivariant, stable, or task-relevant.
- State when the constraint could block useful adaptation.

## Minimum Contrast

Specify the constraint or parameterization, compare constrained and unconstrained changes under matched update budget, measure target progress and preservation separately, vary tolerance, and test a boundary regime.

## Reject or Return When

Reject or bound the claim when `I` is not damaged, preserving it does not change predicted behavior, the constraint only reduces update magnitude, a generic regularizer matches it, or the feasible set blocks the needed change.

## Time-Series Hazards

Check causal information, phase, ordering, scale consistency, calibration, state evolution, and recoverability only when diagnosed. Do not map reconstruction or stability directly to forecast gain.

