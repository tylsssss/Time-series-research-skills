# Pattern C — Change the Design Granularity

## Route When

Use when one coarse choice changes several responsibilities and confounds attribution, ranking, or semantic comparison.

```text
coarse choice C jointly changes p1 ... pn
-> the decision signal is confounded
-> expose the smallest causally relevant choice g
-> preserve the surrounding interface
```

## Structural Contract

- Identify the properties changed unintentionally by the coarse choice.
- Define the smallest unit that still expresses the suspected mechanism.
- Preserve semantic meaning, shape, information access, receptive field, and responsibility outside that unit.
- State interactions that cannot be isolated as independent fine-grained choices.
- Include an equally sized or equally regularized reduced-space rival.

## Minimum Contrast

Implement one narrow, typed decision family; hold architecture and budget fixed; observe coverage and interactions when searched; validate selected choices outside inherited shared weights; compare random and reduced-space alternatives.

## Reject or Return When

Reject or bound the granularity claim when the finer unit does not improve attribution or ranking reliability, the interface changes, interactions dominate, a reduced or random search matches it, or added search cost overwhelms the distinction.

## Time-Series Hazards

Preserve causal context, temporal semantics, scale and variable roles, and effective look-back length across choices. Do not compare options with different future access.

