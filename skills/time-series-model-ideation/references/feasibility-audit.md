# Feasibility Audit

Use this reference to execute Stage 9 on the frozen candidate or adapted system that would actually be trained and evaluated. Close the structural implementation and testability contract; do not infer optimization health, mechanism efficacy, downstream performance, novelty, or theory validity.

## Contents

1. Entry and Assessment Subject
2. Feasibility Subject Contract
3. Responsibilities, Flow, and Interfaces
4. Tensors, Operations, State, and Access
5. Update and Constraint Paths
6. Optimization Validity Versus Empirical Health
7. Train/Inference and Resource Contracts
8. Minimum Viable Experiment and Fallback
9. Compile G9 and Route Repairs
10. Stage-Specific Anti-Patterns

## 1. Entry and Assessment Subject

Before a positive G9 decision:

- require G0–G8 to be evaluated and every applicable upstream gate satisfied;
- require stable `CAND-*`, `SYS-*`, and `COMP-*` operations, connections, responsibilities, state, training path, inference path, and constraints;
- require the novelty subject to match the implementation subject; and
- make task-specific causality, data, deployment, latency, compute, and memory limits explicit.

Perform a diagnostic audit when upstream evidence is incomplete, but keep G9 `DEFERRED` when the actual subject may still change.

Use `CAND-*` when no adaptation exists. Use `SYS-*` when component interaction, changed flow, adaptation, or responsibility defines the trainable system. Assess each `COMPARE` subject separately.

Invalidate G9 when the core operator, information access, responsibility, state transition, constraint, objective, update schedule, output contract, search space, or CORE contribution changes. Return to the earliest affected stage and re-freeze.

## 2. Feasibility Subject Contract

Compile internally:

```text
Assessment subject ID:
Base candidate and component IDs:
Primary input and output:
Training-only and inference-available information:
State, initialization, update, detachment, and reset:
Trainable and frozen parameter groups:
Losses, estimators, and update schedules:
Hard and soft constraints:
Core observables and interventions:
Data, compute, memory, and latency budget:
Critical implementation assumptions:
```

Instantiate every canonical Section 11 aspect row. Mark `Executability critical: YES` when failure would make the subject undefined, non-runnable, untestable, out of budget, or different from its frozen definition. Do not mark a missing critical premise noncritical.

Assign each aspect `SATISFIED`, `UNSATISFIED`, or `UNRESOLVED` and link supporting claim IDs. A design intention without an operation is not supporting evidence.

## 3. Responsibilities, Flow, and Interfaces

For every component:

- assign one primary responsibility and declare material secondary effects;
- name the input consumed and output or state changed;
- detect missing, duplicated, circular, or incompatible responsibilities;
- define disable, replacement, observation, and intervention hooks needed for attribution.

Trace one sample end to end:

```text
raw observation
-> preprocessing and indexing
-> inputs and masks
-> representation and state updates
-> decision, recovery, or search operation
-> prediction or structured output
-> loss and parameter update
-> inference output
```

At every boundary record meaning, time index, source, consumer, availability, and whether the value is observed, derived, learned, sampled, or cached.

Reject silent use of future values, labels or validation outcomes at inference, state without lifecycle rules, final-model statistics unavailable after search, or a source-domain variable with no target construction.

Validate both semantic and computational interfaces: meaning, shape, dtype, device, range, axes, masks, missingness, stochasticity, state ownership, and train/inference availability. Shape agreement alone is insufficient.

## 4. Tensors, Operations, State, and Access

Register only quantities that cross modules, change semantic meaning or information access, maintain state, enforce constraints, drive CORE claims, or differ between training and inference.

For each registered quantity verify:

```text
meaning and time index
shape and domain
producer and consumer
operation and reduction/broadcast axes
training and inference availability
state dependence and reset rule
```

For nonstandard operations, define domain, codomain, boundaries, padding, masks, normalization, missing-data behavior, and whether the operation is exact, approximate, stochastic, or learned. Identify undefined, singular, discontinuous, or overflow-prone cases.

Apply inverse, reconstruction, projection, or conservation claims only to the implemented operator, not an idealized source version.

## 5. Update and Constraint Paths

For each trainable parameter group record:

```text
objective and target
gradient or estimator path
differentiable, relaxed, sampled, alternating, or enumerated update
frequency and order
frozen or stop-gradient boundaries
observable failure signal
```

Require an executable signal for every trainable group and an intentional reason for every frozen group. Define estimators for discrete choices; define data splits and state for alternating or bilevel updates; handle argmax, serialization, external decoding, and detached state explicitly.

For every critical constraint record:

```text
constrained object and valid set
enforcement operation and timing
invalid or empty input behavior
gradient or estimator behavior
train/inference equivalence
violation observable
```

Distinguish hard validity, soft preference, and empirical coverage. Only hard validity and executable soft enforcement belong to G9; coverage quality belongs to Stage 11.

## 6. Optimization Validity Versus Empirical Health

Set `Optimization path valid: YES` only when objectives, estimators, update paths, nondifferentiable boundaries, structural numerical conditions, and risk observables are defined without a known contradiction.

Do not use G9 to claim observed convergence, conditioning, coverage, ranking quality, seed stability, task gain, or realized long-run efficiency. Represent these as hypotheses with Stage-11 experiments.

Use `UNRESOLVED` only for a critical executability premise, such as whether a required estimator produces any update or whether a projection can be computed at target scale. Use `UNSATISFIED` for a known contradiction, such as an impossible shape, detached trainable controller with no estimator, illegal information, or a claimed hard constraint the decoder can violate.

## 7. Train/Inference and Resource Contracts

Check that every inference input exists in deployment; train-only relaxations have an inference mapping; sampled decisions have a hard policy when required; state and normalization lifecycles match deployment; search, selection, and final training are not conflated; and constraints remain enforced.

Estimate or bound:

- parameters, optimizer state, activations, and persistent state;
- forward and backward compute;
- search, sampling, controller, or alternating-update multipliers;
- data, metadata, pretraining, and repeated-training requirements;
- inference latency, memory, and state retention; and
- the cost of fair baselines and decisive experiments.

`Resources within budget: YES` requires a credible bound or measurement under the declared task budget. Treat a missing critical estimate as unresolved and a known violation as unsatisfied.

## 8. Minimum Viable Experiment and Fallback

Create one `EXP-*` that preserves every nonstandard path at the smallest useful scale and can check:

- forward execution;
- backward or estimator execution for every trainable group;
- hard-constraint validity and violation logging;
- train and inference paths;
- core intermediate and invariant observability;
- disable and replacement hooks; and
- a coarse resource ceiling.

The MVE tests executability, not superiority, mechanism attribution, or long-run health. It may remain planned when inspection closes every critical contract.

Set `Mechanism testable: YES` only when core intermediates and invariants can be read, the mechanism can be intervened on, matched interfaces exist, and rivals can receive discriminating tests.

Record a fallback for the highest implementation risk. Treat a routine change that preserves the same operator and claims as mitigation. Treat any fallback that changes the operator, information flow, responsibility, constraint, search space, or mechanism as a new adaptation or candidate requiring refreeze.

## 9. Compile G9 and Route Repairs

Derive each canonical summary field from its source aspect rows:

```text
any required source UNSATISFIED -> NO
else any required source UNRESOLVED -> UNRESOLVED
else -> YES
```

Compile G9:

```text
any critical aspect UNSATISFIED -> G9 UNSATISFIED
else any critical aspect UNRESOLVED -> G9 UNRESOLVED
else any required summary NO -> G9 UNSATISFIED
else any required summary UNRESOLVED -> G9 UNRESOLVED
else -> G9 SATISFIED
```

Route the earliest repair:

| Finding | Return |
|---|---|
| Interface, state, connection, or component responsibility changes | Stage 7 |
| Core operator, objective, mechanism, or search space changes | Stage 5 |
| Causal link fails | Stage 3 |
| Invariant is unmeasurable or unnecessary | Stage 4 |
| Only an implementation routine changes | Stage 9 |
| Critical premise is testable but unknown | Keep G9 unresolved and name the MVE |

Use `PIVOT` for a repairable contradiction and reserve `KILL` for a decisive contradiction with no substantive direction left. Renew Stage 8 whenever a repair changes a CORE contribution.

## 10. Stage-Specific Anti-Patterns

- Do not call a method feasible because a dry run executes.
- Do not call optimization healthy because a symbolic gradient exists.
- Do not enumerate ordinary temporary tensors into an implementation manual.
- Do not treat a prompt or uncalibrated penalty as a hard constraint.
- Do not use an MVE to claim causal attribution or baseline superiority.
- Do not let a fallback make the current subject pass.

