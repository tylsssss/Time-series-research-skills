# Mechanism Transfer

Use this reference to execute the cross-domain branch of Stage 5 and to preserve its reasoning through Stages 6–7. Establish an evidence-bounded operational warrant for transfer, expose source assumptions that break in the target regime, and derive only the minimum justified time-series adaptation. Do not recommend methods by name or treat transfer as evidence of novelty or task improvement.

## Contents

1. Purpose and Boundary
2. Entry Conditions and Mode Rules
3. Required Inputs and Dossier Updates
4. Compile the Target Repair Contract
5. Abstract the Source Mechanism
6. Establish the Transfer Warrant
7. Project Source Assumptions into the Target Regime
8. Assess Direct Use
9. Derive the Minimum Time-Series Adaptation
10. Generate Differential Predictions and Falsifiers
11. Update Gates and Return Control
12. Anti-Patterns

## 1. Purpose and Boundary

- Transfer a causal or mathematical operation that addresses named `LINK-*` records while preserving named `INV-*` records.
- Require the target-side repair need to exist independently of the source method, field, terminology, or paper narrative.
- Treat cross-domain transfer as optional. Retain the minimal in-domain correction and fair simple or null baseline even when a transfer candidate is plausible.
- Establish a defensible mechanism hypothesis and target-specific predictions; do not claim that the mechanism has repaired the failure before the relevant experiment is completed.
- Use primary source material only to characterize the source problem, operation, assumptions, established properties, and known limitations. Preserve citations and evidence boundaries.
- Stop source reading once those facts are sufficiently characterized. Do not search for closest time-series neighbors, establish priority, or assign a novelty status within this protocol.
- Do not inherit a source-domain guarantee after changing the operator, assumptions, information access, or optimization regime. Defer target-side theoretical claims to Stage 10.
- Perform only transfer-specific compatibility checks here. Defer full tensor, gradient, optimization, resource, and end-to-end execution audits to Stages 9–10.

Use these two traces as the protocol backbone:

```text
LINK-* + INV-*
-> required target operation
-> source mechanism signature
-> causal or mathematical correspondence
-> target-specific CLM-*
-> falsifying EXP-*
```

```text
source assumption
-> supported target incompatibility
-> FIND-* with ADAPT
-> minimum COMP-*
-> mechanism-retention check
-> ablation or boundary EXP-*
```

## 2. Entry Conditions and Mode Rules

### 2.1 Common entry conditions

Read before transferring:

- [ ] The task, data regime, evaluation target, deployment constraints, and evidence cutoff.
- [ ] The solution-independent `NEED-*`, localized `FAIL-*`, adjacent `LINK-*` records, rival explanations, and measurable `INV-*`.
- [ ] The supporting, contradicting, and unresolved `CLM-*` records for G2–G4.
- [ ] The candidate cap, required candidate roles, and fair attribution baseline from `SKILL.md`.
- [ ] The canonical fields and enums in `assets/idea-dossier-template.md`.

Do not use a transfer protocol to bypass diagnosis. If the target failure, causal mechanism, or invariant changes during transfer, return to the earliest affected stage and invalidate dependent candidate work.

### 2.2 `GENERATE`

- Require G2, G3, and G4 to be `SATISFIED` before designing a new transfer-based architecture.
- Freeze Stages 1–4, the minimal in-domain candidate, and the simple or null baseline.
- Before source lookup, instantiate any optional cross-domain `CAND-*` in source-independent language. Define its core operation only from the Target Repair Contract and a potential causal or mathematical correspondence; do not name a source method yet.
- Include that target-derived transfer candidate in the frozen candidate IDs. Do not add a different candidate because a literature search reveals an attractive method.
- Consult source material only to retain, bound, or reject the frozen transfer candidate and to complete its mapping.
- Omit the cross-domain candidate when no source-independent correspondence can be stated. Do not create one for candidate diversity.

### 2.3 `AUDIT` and `COMPARE`

- Freeze every supplied candidate and its target-side causal claims before reading source material.
- Preserve the supplied candidate even when G2–G4 are unresolved so that its mapping can be audited.
- Expose mapping gaps, unsupported assumptions, and invalid inherited properties, but do not form a positive transfer conclusion or add adaptation components while a decisive earlier gate remains unresolved.
- Apply the protocol separately to every supplied cross-domain candidate. Keep candidate IDs explicit and retain a fair simple or null baseline.

### 2.4 `REPAIR`

- Return to the earliest failed transfer element: target repair contract, source signature, correspondence, assumption compatibility, or adaptation contract.
- Repair only the downstream elements that depend on the failed element.
- Exit this protocol and return to Stages 3–4 if the repair requires changing a causal `LINK-*` or `INV-*`.
- Return to Stage 5 and re-freeze the candidate if the adaptation removes the source mechanism's defining operation.

## 3. Required Inputs and Dossier Updates

Treat the following objects as internal compilation checklists, not new dossier sections:

| Transfer audit object | Compile into the canonical dossier |
|---|---|
| Target Repair Contract | Section 7 core operation, addressed `LINK-*` IDs, preserved `INV-*` IDs; Section 13 fair baseline |
| Source Mechanism Signature | Section 7.1 source problem, source mechanism, source assumptions; source claims in Section 3 |
| Transfer Warrant | Section 7 and 7.1 correspondence and mapping; warrant claims in Section 3 |
| Assumption projection | Section 3 assumption or hypothesis claims; supported incompatibilities in Section 8 |
| Differential prediction | Section 3 `HYPOTHESIS` claims referenced by Sections 7 and 7.1 |
| Adapted mechanism | Section 9 `SYS-*` and `COMP-*` records |
| Falsifier | Section 13 `EXP-*` records |

Update only as each stage is entered:

- **Stage 5:** Update Sections 3, 7, 7.1, 7.2, and any necessary planned rows in Section 13. Update G5 without pre-completing Stages 6–7.
- **Stage 6:** Update Section 8 and G6 for each non-null candidate.
- **Stage 7:** Update Section 9 and G7 only for candidates that proceed to direct use or adaptation.

At Stage 5, put only already-established target incompatibilities in Section 7.1 `Broken assumptions`. Otherwise use the template's `PENDING — <reason>` syntax and resolve the field during Stage 6; do not present a possible mismatch as an observed finding.

Do not assign novelty, full feasibility, theory, or final-decision results. Preserve `assets/idea-dossier-template.md` as the sole authority for fields, enums, IDs, lifecycle values, and field order.

## 4. Compile the Target Repair Contract

Compile the target need before naming or searching for a source mechanism:

```text
Addressed failure:
Addressed causal LINK-* IDs:
Preserved INV-* IDs:
Required operation:
Allowed information:
Forbidden information:
Target operating constraints:
Required attribution contrast:
```

Apply these checks:

- [ ] Derive the required operation from the diagnosed causal link rather than from a known module.
- [ ] Describe what the operation must change and what it must preserve.
- [ ] State the information available at training and inference; forbid future access when the deployment regime is causal.
- [ ] State shape, state, sampling, latency, or deployment constraints only when already fixed by the target regime.
- [ ] Name the fairest simple explanation that could repair the same link, such as a residual path, matched-capacity correction, regularizer, smaller search space, or constrained head.
- [ ] Use the simple explanation as the required attribution contrast. Do not formulate a source-mechanism-specific prediction until the source operation is known.
- [ ] Remove every source-domain name and repeat the derivation. Reject a contract that no longer follows from `FAIL-*`, `LINK-*`, and `INV-*`.

Do not define the required operation as “apply method X.” Prefer an operation-level statement such as “predict an omitted cross-part quantity, preserve its residual, and feed a bounded correction back to the retained representation.”

## 5. Abstract the Source Mechanism

Represent the source mechanism with the smallest signature needed to judge transfer:

```text
Source problem:
Source objects and relations:
Source operation or operator:
Immediate causal or mathematical effect:
Preserved or established property:
Required assumptions:
Known failure conditions:
Source-side prediction or guarantee:
Primary source references:
```

- [ ] Describe the operative transformation, update, constraint, or estimator rather than an architecture family.
- [ ] Use a minimal equation or algorithmic trace when prose leaves the mechanism ambiguous.
- [ ] Separate the operation from its source implementation and from downstream source-task performance.
- [ ] Separate assumptions required by the operation from assumptions required only by a source proof or implementation.
- [ ] Record whether each source property is empirical, derived, or formally proved in the cited source. Do not convert it into target evidence.
- [ ] Record source limitations and negative results when the primary source reports them.
- [ ] Mark an unavailable or ambiguous source fact `UNRESOLVED`; do not reconstruct it from a method name or common reputation.

Reject signatures consisting only of terminology, module shapes, diagrams, or broad principles such as “multi-scale,” “adaptive,” “physical,” or “information preserving.”

## 6. Establish the Transfer Warrant

Create canonical `CLM-*` records for the material warrant claims and assign each `SUPPORTED`, `UNRESOLVED`, or `CONTRADICTED` according to available evidence. Do not create a new warrant-status schema.

### 6.1 Check the correspondence

Check all applicable axes:

1. **Object and relation alignment:** Map the source objects and relations to target objects and relations without relying on tensor-shape similarity alone.
2. **Operation alignment:** Show that the mapped operator performs the operation required by the Target Repair Contract.
3. **Causal or mathematical alignment:** Show how the mapped operation addresses named `LINK-*` records. A mathematical analogy must still connect to the diagnosed target mechanism.
4. **Invariant alignment:** Show how the mapped operation is expected to preserve or recover named `INV-*` records under explicit conditions.
5. **Information-regime alignment:** Check that the mapping does not silently introduce unavailable observations, future leakage, privileged labels, or inconsistent state.

For every axis:

- [ ] State the source element, target element, mapping, required assumptions, and strongest mismatch.
- [ ] Link the mapping to existing `LINK-*`, `INV-*`, and `CLM-*` IDs.
- [ ] Distinguish a logical correspondence from evidence that the target effect occurs.
- [ ] Record at least one structural mismatch or transfer risk in Section 7.2 whenever this reference or a source pattern is consulted.

### 6.2 Apply warrant outcomes

- If object, operation, causal or mathematical, or invariant alignment is `CONTRADICTED`, mark the transfer candidate `REJECTED` unless a materially different candidate is re-frozen.
- If a decisive alignment is `UNRESOLVED`, keep the candidate `UNRESOLVED` or `SHORTLISTED` as appropriate, create the smallest discriminating `EXP-*`, and do not state a positive transfer conclusion.
- If the core alignments are supported, retain the candidate for direct-use assessment. Do not infer task benefit.
- Treat inability to translate a material source assumption as `UNRESOLVED`, not as compatibility.

Apply this counterfactual test:

```text
If the source-domain name and story are removed,
does the mapped operation still follow from the target repair contract,
and does it predict something the attribution baseline does not?
```

Reject solution-first transfer when the answer is no.

## 7. Project Source Assumptions into the Target Regime

Translate every material source assumption into a target-side condition. Inspect only applicable categories:

- information access, causality, and leakage;
- sampling, indexing, alignment, and missingness;
- locality, stationarity, noise, and distribution shift;
- variable dependence and cross-series behavior;
- partition, scale, topology, or ordering structure;
- exactness, invertibility, identifiability, and boundary handling;
- parameterization, learnability, differentiability, and estimator requirements;
- numerical stability and error amplification;
- training/inference consistency, state, and interface requirements.

Classify the basis of each target-side assessment:

- `TASK-CONTRACT`: The target or deployment definition directly establishes compatibility or incompatibility.
- `SUPPORTED-EVIDENCE`: A cited or measured target result establishes it.
- `UNRESOLVED-EMPIRICAL`: A target fact must be measured.
- `NOT-MATERIAL`: The assumption is not required for the transferred operation; justify why.

Use these labels only as internal reasoning aids. Compile the underlying statements into canonical `CLM-*` records rather than adding them to the dossier schema.

Do not let a merely plausible failure justify a component:

- Allow `ADAPT` only when a broken assumption follows directly from the task contract or has supporting target evidence.
- Keep an empirical incompatibility `UNRESOLVED` when the decisive measurement is missing. Create a targeted `EXP-*`; do not add a `COMP-*`.
- Use `BOUND-CLAIM` when a known or conservatively assumed boundary can be handled by narrowing the regime or claim without changing the mechanism.
- Use `REJECT` when compatibility would require abandoning the target contract, the defining source operation, or the preserved invariant.

## 8. Assess Direct Use

Create the canonical Section 8 finding only after tracing the source assumption to a target consequence. Use exactly the dossier dispositions.

| Condition | Section 8 result | Consequence |
|---|---|---|
| A supported incompatibility is repairable without changing the target need or defining source operation | `ADAPT` | Enter Stage 7 and design the minimum repair |
| A limitation only narrows the valid regime or claim | `BOUND-CLAIM` | Preserve the boundary in `CLM-*` and `FIND-*`; add no component |
| The mechanism or mapping is invalid in the target regime | `REJECT` | Mark the candidate `REJECTED`; do not create a Section 9 adaptation row |
| No material incompatibility is found after the complete assessment | `NO-ADAPTATION-REQUIRED` | Preserve direct use and add no component |
| A decision-relevant incompatibility remains empirically unresolved | Use `BOUNDARY-CONDITION` with a conservative `BOUND-CLAIM`; keep G6 `UNRESOLVED` | Record the unresolved claim and decisive experiment; do not enter Stage 9 or manufacture a component or no-risk conclusion |

For an unresolved incompatibility, keep Section 8 `ACTIVE`, state the finding as `UNRESOLVED — <EXP-* will test the target condition>`, link its `E0` or otherwise justified unresolved claim, and use `BOUND-CLAIM` as a conservative temporary disposition. This representation bounds what may currently be claimed; it does not establish that the boundary is real. Keep G6 `UNRESOLVED`, do not add this candidate to Section 9, and return `NEED-EVIDENCE` through the main workflow. If no other candidate enters Stage 7, leave Section 9 `NOT-STARTED`.

Do not equate candidate rejection with failure to execute G6. G6 may be `SATISFIED` when a candidate has been fairly assessed and validly rejected.

## 9. Derive the Minimum Time-Series Adaptation

Enter this section only for a supported `ADAPT` disposition.

- [ ] Define the smallest change that repairs the recorded incompatibility while retaining the source mechanism's defining operation.
- [ ] Prefer changing an operator, constraint, information path, parameterization, or boundary rule over adding a general-purpose module.
- [ ] Create each `COMP-*` only after identifying at least one `FIND-*` with `ADAPT` that it repairs.
- [ ] Map every `ADAPT` finding to at least one `COMP-*`, or record the unresolved implementation dependency and keep G7 `UNRESOLVED`.
- [ ] Do not create components for `BOUND-CLAIM`, `REJECT`, or unresolved empirical incompatibilities.
- [ ] Give every component one primary responsibility, an explicit operation, input/output contract, material risk, mitigation, and ablation `EXP-*`.
- [ ] Preserve a candidate with `NO-ADAPTATION-REQUIRED` without creating a `SYS-*` or `COMP-*`.

Compile Section 8 dispositions into Section 9 as follows:

| Section 8 disposition | Section 9 handling |
|---|---|
| `ADAPT` | Use `ADAPTED`; define the `SYS-*`, required `COMP-*`, and repaired `FIND-*` IDs |
| `NO-ADAPTATION-REQUIRED` | Use `NO-ADAPTATION-REQUIRED`; create no system or component IDs and use the template's required `N/A — <reason>` values or rows |
| `BOUND-CLAIM` | Use `NO-ADAPTATION-REQUIRED` only when the bounded direct mechanism remains coherent; preserve the limitation in `CLM-*` and `FIND-*`, create no system or component IDs, and use the required `N/A — <reason>` values or rows |
| `REJECT` | Mark the candidate `REJECTED` and omit it from adaptation design |

### 9.1 Run the mechanism-retention check

After defining the adaptation, re-run the Transfer Warrant:

- [ ] Verify that the defining source operation still exists in the adapted data flow.
- [ ] Verify that the mapped causal or mathematical correspondence still addresses the same `LINK-*` records.
- [ ] Verify that the `INV-*` remains independently measurable and is still predicted to be preserved.
- [ ] Verify that the repaired assumption is actually enforced rather than merely described.
- [ ] Identify new failures, information paths, or responsibility changes introduced by the adaptation.
- [ ] Downgrade every inherited source property whose assumptions or operator changed; do not preserve a theorem label by analogy.
- [ ] Link the retention, repair, and boundary claims to separate ablation or falsification `EXP-*` records where needed.

If the defining source operation disappears, stop calling the design a transfer of that mechanism. Return to Stage 5, preserve the rejected or superseded candidate, and re-freeze the new design as an in-domain or materially different candidate.

## 10. Generate Differential Predictions and Falsifiers

After establishing the Transfer Warrant, generate target-side predictions that distinguish the transferred operation from rivals and simple baselines.

Require each prediction to be:

- target-specific rather than copied from the source task;
- conditional on named assumptions or regimes;
- connected to a mechanism, invariant, adaptation, or boundary;
- different under at least one fair rival or attribution baseline;
- falsifiable by a plausible result;
- recorded as a canonical `HYPOTHESIS` `CLM-*` and linked to an `EXP-*`.

Cover the following when applicable:

1. **Mechanism prediction:** State the intermediate change expected if the transferred operation repairs the named causal link.
2. **Invariant prediction:** Measure invariant preservation separately from downstream performance.
3. **Attribution prediction:** Distinguish the mechanism from added capacity, a residual path, regularization, altered information access, or another simple repair.
4. **Boundary prediction:** State a regime where the mechanism should weaken, fail, or become unnecessary.
5. **Adaptation-necessity prediction:** Compare direct transfer with the adapted system when adaptation is proposed.

Include a matched simple baseline, direct-versus-adapted comparison when relevant, and an ablation for every added component. State what a null result cannot prove and how falsification changes the candidate status or gate.

## 11. Update Gates and Return Control

Evaluate gates as workflow checks rather than popularity or quality scores:

- **G5:** Check that candidate roles, freeze discipline, attribution baseline, and every cross-domain mapping are complete. A rejected transfer candidate does not by itself make G5 fail when the remaining candidate set is valid.
- **G6:** Check that every non-null candidate receives a complete direct-use assessment and a justified disposition or an explicit unresolved blocker. A valid `REJECT` may coexist with G6 `SATISFIED`.
- **G7:** Check only candidates that proceed. Require every `ADAPT` finding to close through component contracts and the mechanism-retention check; require every no-adaptation path to remain coherent and preserve the invariant.

Use canonical gate states and failure modes. Do not average candidates or gate results. If all substantive candidates are rejected, return control to `SKILL.md` to determine whether the candidate-set failure is repairable or fatal.

Return to the main workflow after each stage update. Do not continue into novelty, full feasibility, theory, or final decision within this protocol.

## 12. Anti-Patterns

- Do not add a cross-domain candidate after source search unless Stage 5 is explicitly revisited and the candidate set is independently re-frozen.
- Do not use “physical,” “engineering,” or “information preserving” as a mechanism description.
- Do not assume an untranslated source assumption is compatible.
- Do not turn an unresolved empirical risk into an adaptation component.
- Do not invent a broken assumption to justify architectural complexity.
- Do not add a component without an `ADAPT` finding, explicit responsibility, and ablation.
- Do not preserve the source mechanism label when adaptation removes its defining operation.
- Do not perform nearest-neighbor novelty search or assign novelty status in this protocol.
- Do not let rejection of one candidate masquerade as failure of the transfer-audit workflow.
