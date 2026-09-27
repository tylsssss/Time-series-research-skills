# Pattern E — Reroute Information or Computation Flow

## Route When

Use when required information exists but reaches an operation too late, through the wrong direction, after destructive mixing, or through repeated computation.

```text
source S contains quantity q
-> path P blocks, delays, aliases, or recomputes q
-> path P' exposes q to operation O under legal access
-> predicted intermediate M changes before task performance
```

## Structural Contract

- Draw the current and proposed directed computation paths.
- Name the exact edge, timing, or routing rule that changes.
- Verify train-time and inference-time access separately.
- Control shorter gradient paths, extra capacity, and extra parameters.
- State what information must not traverse the new path.

## Minimum Contrast

Change the smallest edge or rule, intervene through blocking or replacement, compare a capacity-matched bypass, measure the predicted intermediate, and report execution cost when order or communication changes.

## Reject or Return When

Reject or repair when edge intervention does not change the intermediate, a matched bypass behaves identically, the path leaks unavailable information, improvement is only generic optimization relief, or communication cost violates the regime.

## Time-Series Hazards

Audit causal direction, look-back windows, state update order, cross-scale and cross-variable communication, and train/inference consistency.

