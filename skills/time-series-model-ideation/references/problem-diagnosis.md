# Problem Diagnosis

Use this reference to execute Stages 2–4 as a causal-diagnosis protocol. Convert a broad need into a measurable failure, a testable causal chain, discriminating rivals, and a task-relevant invariant. Do not construct a method.

## Contents

1. Purpose and Boundary
2. Required Inputs and Dossier Updates
3. Localize the Failure
4. Design Diagnostic Measurements
5. Construct the Minimal Causal Chain
6. Generate and Discriminate Rival Explanations
7. Extract the Preserved Invariant
8. Update Evidence, Experiments, and Gates
9. Anti-Patterns

## 1. Purpose and Boundary

- Diagnose what must be repaired and why it matters before proposing how to repair it.
- Keep the need solution-independent.
- Separate observation, explanation, mechanism, assumption, and evidence.
- Treat a diagnostic plan as planned work, not as evidence that the diagnosis is true.
- Update the canonical Idea Dossier in place; do not emit a separate partial dossier.
- Return control to `SKILL.md` after updating Stage 2–4 records.
- Do not execute Stage 5 or read Stage-5 references within this protocol.
- Do not create `CAND-*`, `FIND-*`, `SYS-*`, or `COMP-*` records.
- Do not judge novelty, choose a transferred mechanism, approve feasibility, or issue the final decision.

## 2. Required Inputs and Dossier Updates

Read before diagnosing:

- [ ] The research boundary, entry mode, task, data regime, evaluation target, and constraints.
- [ ] The solution-independent `NEED-*` record.
- [ ] User-supplied observations, citations, assumptions, and unknowns.
- [ ] Existing `CLM-*` records and their provenance, evidence strength, and status.
- [ ] The canonical field definitions in `assets/idea-dossier-template.md`; do not redefine them here.

Update only:

- [ ] Section 3 with diagnosis-related `CLM-*` records.
- [ ] Section 4 with the `FAIL-*` summary.
- [ ] Section 5 with adjacent `LINK-*` records and at least two `RIV-*` records.
- [ ] Section 6 with the `INV-*` record.
- [ ] Section 13 with diagnostic `EXP-*` plans needed to establish or discriminate claims.
- [ ] Section 15 with evidence-accurate G2, G3, and G4 states.

Preserve the asset as the sole output-schema authority. Use the taxonomies below only as diagnostic lenses; do not add fields, enums, or ID types to the dossier.

## 3. Localize the Failure

### 3.1 Trace the Processing Chain

Trace the actual path from raw data through sampling/windowing, decomposition/tokenization, representation, interaction/transformation, objective/optimization, decision/output, and evaluation.

For each relevant transition:

- [ ] Name the exact operation rather than an architecture family.
- [ ] Identify the pre-operation and post-operation quantities.
- [ ] State the condition under which the symptom appears.
- [ ] Identify the earliest point at which the symptom becomes measurable.
- [ ] Treat that point as a localization boundary, not automatically as the root cause.
- [ ] Check whether an upstream change becomes visible only after a downstream operation.
- [ ] Prefer the narrowest operation whose intervention could distinguish explanations.

### 3.2 Classify Without Explaining

Use one or more internal lenses:

- `DATA`: missingness, noise, irregular sampling, misalignment, or distribution change.
- `REPRESENTATION`: aggregation, compression, aliasing, mixing, or semantic loss.
- `INTERACTION`: incorrect dependency, receptive field, direction, or information flow.
- `OPTIMIZATION`: gradient failure, collapse, poor coverage, ranking error, or numerical dynamics.
- `INTERFACE`: illegal output, unenforced constraint, incompatible contract, or unclear responsibility.
- `EVALUATION`: leakage, unequal budget, metric artifact, split artifact, or unfair baseline.

Do not treat a lens as an explanation. Express every proposed explanation as a `CLM-*` record and test it.

### 3.3 Separate the Three Losses

Assess independently:

1. `Signal information loss`: Test whether a measurable signal property changes or disappears.
2. `Task-relevant information loss`: Test whether the changed property is useful for the target under the allowed input regime.
3. `Downstream performance loss`: Test whether the operation changes the task metric under a controlled comparison.

- [ ] Use an independent measurement for each loss.
- [ ] Do not use one performance result to fill all three conclusions.
- [ ] Do not infer task relevance from reconstruction error alone.
- [ ] Do not infer causal performance loss from information preservation alone.
- [ ] Mark any unmeasured link `UNRESOLVED` at the justified evidence level.

Apply this three-loss split only when information loss is part of the diagnosed problem. For optimization, interface, ranking, or evaluation failures, define the corresponding independent intermediate and task-level measurements instead.

## 4. Design Diagnostic Measurements

### 4.1 Use the Minimal Diagnostic Ladder

Apply the tiers in order. Select the smallest set capable of changing a gate state.

**Tier A — Establishment**

- [ ] Use an observation test to determine whether the symptom exists.
- [ ] Use a localization test to determine where it first becomes measurable.

**Tier B — Causal discrimination**

Choose at least one test whose predictions differ across the main mechanism and a rival:

- `Matched bypass`: Replace or bypass the suspected operation while matching capacity, information access, and training budget.
- `Oracle intervention`: Restore only the hypothesized property without adding unavailable future information.
- `Dose response`: Vary disruption severity only when the mechanism predicts a direction or response shape.
- `Negative control`: Apply a matched intervention to a property the mechanism predicts should be irrelevant.

**Tier C — Scope and reliability**

- [ ] Use boundary tests to find regimes where the mechanism should hold or fail.
- [ ] Use robustness tests across relevant seeds, datasets, horizons, or budgets after the core phenomenon has support.

Do not require every diagnostic type. If an oracle or dose response is invalid or unnecessary, choose another discriminating test.

### 4.2 Protect Intervention Validity

For every planned diagnostic:

- [ ] Name the target claim and rival claims.
- [ ] Specify the intervention, matched control, readout, and condition.
- [ ] Record different expected outcomes under competing explanations.
- [ ] Match capacity, parameter count, information path, optimization effort, and compute where they could confound attribution.
- [ ] Keep forecasting diagnostics causal; do not expose future values unavailable at inference.
- [ ] Distinguish an oracle upper bound from a deployable intervention.
- [ ] Check that a bypass does not merely shorten the path or remove regularization.
- [ ] State what the result cannot prove.
- [ ] Create or reserve a stable `EXP-*` ID in Section 13.
- [ ] Use `NEED-*` or `FAIL-*` as the assessment subject before candidates exist.

## 5. Construct the Minimal Causal Chain

Express every causal node as an existing `CLM-*` record. Connect only adjacent claims from the operation through object/process change, intermediate effect, symptom, and task consequence.

- [ ] Give each adjacent transition one stable `LINK-*` ID.
- [ ] Put only `CLM-*` IDs in `From claim ID` and `To claim ID`.
- [ ] Make each link independently testable.
- [ ] Link supporting and contradicting claims.
- [ ] Mark an untested link `UNRESOLVED`; do not upgrade it because the full story is plausible.
- [ ] Avoid skipping directly from an operation to task performance.
- [ ] Treat the earliest measurable boundary as localization evidence, not proof of upstream causation.
- [ ] Prefer the smallest chain that explains the symptom and creates a discriminating prediction.

Summarize the observable symptom in `FAIL-*`; do not create new entity types for intermediate nodes.

## 6. Generate and Discriminate Rival Explanations

Create at least two rivals. Include a simpler explanation and an artifact or confound when plausible.

Check common sources:

- capacity, parameter count, receptive field, or information access;
- optimization difficulty, gradient path, regularization, or training budget;
- data split, leakage, preprocessing, sampling, or metric artifacts;
- stochastic variation, implementation error, or hyperparameter effort;
- reversed causality or a simpler information path;
- interface validity without mechanism efficacy;
- output legality without healthy exploration or optimization.

For each rival:

- [ ] Express the explanation as a `CLM-*` record.
- [ ] Identify predictions shared with the main mechanism.
- [ ] State at least one prediction that differs.
- [ ] Link the discriminating prediction to a stable diagnostic `EXP-*` ID.
- [ ] Reject the rival only when evidence contradicts it; otherwise keep it active or unresolved.
- [ ] Do not use vague rivals that cannot change an experimental prediction.

## 7. Extract the Preserved Invariant

Derive the invariant from the diagnosed failure, not from a preferred method.

Ask what measurable property exists before the implicated operation, degrades after it, and should change a diagnostic or task behavior when selectively restored under the allowed information regime.

- [ ] Define the property independently of any candidate mechanism.
- [ ] Select the appropriate preservation meaning: exact, approximate, equivariant, stable, or task-relevant.
- [ ] Define a measurement and tolerance.
- [ ] Link the property to task behavior through intervention evidence or an explicit justified derivation.
- [ ] State conditions where preservation is unnecessary or harmful.
- [ ] Distinguish raw signal preservation from task-relevant preservation.
- [ ] Do not define performance itself as the invariant.
- [ ] Do not infer task improvement from invertibility, reconstruction, or stability alone.
- [ ] Do not use future information to demonstrate an inference-time invariant.

If the property is measurable but its task connection is untested, keep G4 `UNRESOLVED`.

## 8. Update Evidence, Experiments, and Gates

### 8.1 Preserve Evidence Integrity

- [ ] Apply the canonical evidence levels from `assets/idea-dossier-template.md` without inflation.
- [ ] Treat a planned measurement as `E1` at most unless other evidence supports the claim.
- [ ] Treat successful execution only as feasibility evidence.
- [ ] Upgrade a causal claim only with a discriminating intervention or equivalent evidence.
- [ ] Record ambiguous and null results; do not convert them into supporting prose.
- [ ] Bound every conclusion by the evaluated regime and controls.

### 8.2 Preserve Experiment Identity

- [ ] Create diagnostic `EXP-*` records in Section 13 during Stages 2–4 when rivals or gates require them.
- [ ] Keep those IDs stable when Stage 11 expands the falsification matrix.
- [ ] Extend an existing experiment when it tests the same intervention and claims.
- [ ] Create a new ID only when the intervention, decisive contrast, or claim coverage materially differs.
- [ ] Do not duplicate an experiment merely because it appears in a later stage.

### 8.3 Apply Strict Gate Semantics

| Gate | `SATISFIED` | `UNRESOLVED` | `UNSATISFIED` |
|---|---|---|---|
| G2 Failure | Direct diagnostic measurement or equivalent task-specific evidence supports the symptom | Measurement is planned, unexecuted, ambiguous, or not target-regime specific | Adequate controls show the symptom is absent or task-irrelevant |
| G3 Causality | Discriminating intervention or equivalent evidence supports the mechanism beyond a rival | Differential predictions exist, but the decisive test is unexecuted or ambiguous | The mechanism-specific prediction fails and a rival explains the result better |
| G4 Invariant | The property is measurable and task relevance has intervention evidence or an explicit justified derivation | The property is measurable, but its task connection remains hypothetical | Selective restoration does not change predicted behavior, or preservation is harmful |

- [ ] Set the canonical failure mode only when a gate is `UNSATISFIED`.
- [ ] Use `REPAIRABLE` when the diagnosis can be materially revised without abandoning the need.
- [ ] Use `CONTRADICTED` when decisive evidence refutes the claim and no substantive repair remains.
- [ ] Never mark a gate `SATISFIED` solely because a good experiment has been designed.
- [ ] Return control to `SKILL.md`; let the main workflow decide whether to continue, pivot, request evidence, or kill.

## 9. Anti-Patterns

- Do not treat a broad benchmark gap as a localized failure.
- Do not equate the earliest measurable symptom with the root cause.
- Do not use reconstruction loss as task-relevance evidence.
- Do not use downstream improvement as causal proof.
- Do not use an unmatched deletion as a valid bypass.
- Do not allow an oracle diagnostic to leak future information.
- Do not label a taxonomy category as the mechanism.
- Do not accept a rival that makes no distinct prediction.
- Do not mark an unexecuted diagnostic as supporting evidence.
