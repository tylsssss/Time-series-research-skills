# Pattern B — Change the Modeled Object or Representation

## Route When

Use when the inherited representation treats the wrong semantic entity as the unit of prediction, comparison, interaction, or learning.

```text
task-relevant entity U
-> representation R merges, fragments, or hides U
-> required operation O cannot express the distinction
-> representation R' exposes U while preserving invariant I
```

## Structural Contract

- Name `U` before defining `R'`.
- Demonstrate what `R` makes inaccessible or confounded.
- Separate representation sufficiency from learner capacity.
- State what `R'` preserves, discards, or makes equivariant.
- Check whether a simpler readout on `R` can express the same mechanism.

## Minimum Contrast

Specify `X -> R'`, hold the downstream learner fixed where possible, measure the alleged property in `R` and `R'`, compare a capacity-matched representation baseline, and test a boundary where the new object should stop helping.

## Reject or Return When

Reject or bound the candidate when `U` is unidentifiable, `R'` leaks target information, a simple readout on `R` matches the prediction, the representation diagnostic changes without the expected consequence, or its cost violates the regime.

## Time-Series Hazards

Define timestamp, event, variable, patch, cycle, scale, regime, or latent-state semantics explicitly. Check irregular sampling, missingness, alignment, horizon dependence, and inference-time causality.

