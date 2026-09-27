# Pattern D — Reassign Component Responsibilities

## Route When

Use when responsibilities conflict, are duplicated or missing, or cannot be attributed to a component.

```text
entangled responsibilities
-> failure or gain cannot be localized
-> assign one primary owner per responsibility
-> connect owners through explicit interfaces
```

## Structural Contract

- Define every responsibility as an operation on named inputs and outputs.
- Identify the conflict, duplication, or missing role that causes the failure.
- Assign one primary owner and declare material secondary effects.
- Give each interface a legal training signal and inference path.
- Test whether one simpler component can perform the combined role.

## Minimum Contrast

Write input/output/state contracts, trace connections end to end, replace each owner with a matched simple alternative, ablate interfaces as well as components, and test any claimed coordination effect.

## Reject or Return When

Reject or repair when responsibilities remain circular or overlapping, an interface is untrainable or illegal at inference, a simpler owner matches the system, the effect cannot be attributed, or separation adds cost without changing the diagnosed behavior.

## Time-Series Hazards

Separate representation, temporal dynamics, cross-variable interaction, uncertainty, constraint, and decision roles only when the task requires them. Do not add a temporal module merely to signal domain specificity.

