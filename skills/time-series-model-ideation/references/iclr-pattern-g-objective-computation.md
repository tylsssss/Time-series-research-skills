# Pattern G — Reframe an Objective or Expensive Computation

## Route When

Use when the inherited objective, estimator, or repeated computation evaluates the wrong unit, is infeasible at the target scale, or misaligns with the actual decision.

```text
target quantity Q
-> inherited estimator E is mismatched or infeasible
-> derive E' at the correct unit or execution stage
-> preserve or bound the relation to Q
```

## Structural Contract

- Define `Q` before proposing `E'`.
- State whether `E'` is exact, unbiased, consistent, bounded, or heuristic.
- Identify the removed assumption or repeated computation.
- Trace estimation and gradient paths.
- Separate lower cost from improved decision quality.

## Minimum Contrast

Check fidelity against `E` in a tractable regime, report asymptotic and measured cost, expose bias or variance, test whether the decision changes beyond the speedup, and compare a simple surrogate or cached baseline.

## Reject or Return When

Reject or repair when `E'` changes the estimand without justification, approximation destroys the relevant decision, routine batching or caching gives the same benefit, the estimator is structurally unstable, or the target regime does not require reframing.

## Time-Series Hazards

Justify any horizon-, scale-, variable-, event-, or regime-aware objective from the diagnosis. Ensure evaluation aggregation does not hide the failure the objective claims to repair.

