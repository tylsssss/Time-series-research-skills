# Idea Dossier

<!--
Dossier schema version: 1.1.0. Record it in Section 0 as `dossier_schema_version`. See CHANGELOG.md for the migration note between schema versions; a dossier without the field is implicitly 1.0.0.

Preserve sections 0–16 and their order. Preserve the field names and table columns of every active section.
Emit every section heading, but use the section lifecycle contract to avoid fabricating work that has not begun.

Section status = NOT-STARTED | ACTIVE | COMPLETE | BLOCKED
- ACTIVE or COMPLETE: emit the lifecycle block and the full section body; replace every {{REQUIRED: ...}} placeholder and leave no blank cells.
- NOT-STARTED or BLOCKED: emit only the heading and lifecycle block. Do not instantiate the remaining fields or tables for that section.
- NOT-STARTED records workflow progress, not missing evidence. BLOCKED names a dependency that prevents the section from being completed.
- Represent missing decision-relevant evidence inside an active section as an UNRESOLVED claim with E0; do not hide unresolved work with N/A or NOT-STARTED.

Use the phases progressively:
- DIAGNOSIS: Sections 0–6.
- INDEPENDENT-IDEATION: Section 7; freeze candidates before consulting pattern or method references.
- AUDIT: Sections 8–13.
- COMPILATION: Sections 14–16; derive them from existing IDs and results.

Entry-mode rules:
- GENERATE: advance phase by phase; leave later sections NOT-STARTED until their dependencies are satisfied.
- AUDIT: preserve the supplied candidate and causal chain; do not silently regenerate them.
- REPAIR: resume at the earliest failed gate, mark invalidated downstream sections NOT-STARTED, and recompute them.
- COMPARE: keep candidates SHORTLISTED or PROVISIONALLY-SELECTED until all compared candidates receive a fair audit.

For a structurally inapplicable field, use the value N/A — <reason>. Add YAML quotes only when YAML syntax requires them; do not include literal quote characters in Markdown-table values.
Use PENDING — <reason> for a planned result that does not exist yet; this is not evidence.
Use only these ID namespaces: DOS-*, NEED-*, CLM-*, FAIL-*, LINK-*, RIV-*, INV-*, CAND-*, FIND-*, SYS-*, COMP-*, EXP-*.
Keep CLM-* IDs claim-only. Link all other entities through related_claim_ids or explicit ID columns.
Use stable IDs throughout; never renumber an ID after another record refers to it.
Do not introduce claims in Sections 14–16 that are absent from Sections 2–13.
-->

## 0. Dossier Control

```yaml
section_status: "{{REQUIRED: ACTIVE | COMPLETE}}"
status_reason: "{{REQUIRED: why this section has this status}}"
dossier_id: "DOS-001"
dossier_schema_version: "{{REQUIRED: schema version this dossier conforms to, e.g. 1.1.0}}"
date: "{{REQUIRED: YYYY-MM-DD}}"
evidence_cutoff: "{{REQUIRED: YYYY-MM-DD}}"
entry_mode: "{{REQUIRED: GENERATE | AUDIT | REPAIR | COMPARE}}"
current_phase: "{{REQUIRED: DIAGNOSIS | INDEPENDENT-IDEATION | AUDIT | COMPILATION | COMPLETE}}"
task: "{{REQUIRED: time-series task}}"
data_regime: "{{REQUIRED: data, sampling, horizon, and deployment regime}}"
evaluation_target: "{{REQUIRED: measurable research target}}"
scope_exclusions: "{{REQUIRED: excluded downstream or scientific work}}"
```

## 1. Research Boundary

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
user_request: "{{REQUIRED: problem as supplied by the user}}"
intended_contribution: "{{REQUIRED: contribution category without assuming success}}"
supplied_evidence: "{{REQUIRED: source references or N/A syntax}}"
task_constraints: "{{REQUIRED: data, causality, compute, time, and evaluation constraints}}"
unknowns: "{{REQUIRED: decision-relevant unknowns or N/A syntax}}"
out_of_scope: "{{REQUIRED: implementation, prose, plotting, or excluded research claims}}"
```

## 2. Need

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
need_id: "NEED-001"
task_objective: "{{REQUIRED}}"
operating_regime: "{{REQUIRED}}"
current_limitation: "{{REQUIRED}}"
measurable_consequence: "{{REQUIRED}}"
solution_independent_need: "{{REQUIRED}}"
method_names_removed_check: "{{REQUIRED: PASS | FAIL}}"
claim_boundary: "{{REQUIRED: what this need does not imply}}"
related_claim_ids: "{{REQUIRED: CLM-* IDs}}"
```

## 3. Typed Claim Ledger

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

Allowed values:

```text
Claim type = OBSERVATION | EXPLANATION | MECHANISM | HYPOTHESIS | ASSUMPTION | EVIDENCE
Centrality = CORE | SUPPORTING | CONTEXT
Provenance = USER-SUPPLIED | DIRECT-MEASUREMENT | PRIMARY-LITERATURE | INFERENCE | NONE
Evidence strength = E0 | E1 | E2 | E3 | E4 | E5
Status = SUPPORTED | CONTRADICTED | UNRESOLVED | NOT-APPLICABLE
```

Interpret empirical evidence strength as:

```text
E0 = UNKNOWN; no relevant evidence
E1 = HYPOTHESIS; testable expectation without direct support
E2 = UNCONTROLLED; source report or uncontrolled observation
E3 = DIRECT-DIAGNOSTIC; task-specific measurement of the predicted symptom
E4 = CONTROLLED-INTERVENTION; matched comparison isolates the proposed factor
E5 = REPLICATED-ROBUST; isolated effect persists across relevant regimes
```

Keep theory maturity as a separate Section 12 axis; never use E-levels as proof status.

| Claim ID | Claim type | Centrality | Statement | Provenance | Source refs | Evidence strength | Supports IDs | Contradicts IDs | Status | Decision impact |
|---|---|---|---|---|---|---|---|---|---|---|
| CLM-001 | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: IDs or N/A syntax}} | {{REQUIRED: IDs or N/A syntax}} | {{REQUIRED}} | {{REQUIRED}} |

## 4. Observable Failure

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
failure_id: "FAIL-001"
failure_class: "{{REQUIRED: REPRESENTATION | INFORMATION | OPTIMIZATION | ESTIMATION | RANKING | SELECTION | INTERFACE | ROBUSTNESS | EFFICIENCY | OTHER — reason}}"
operation_under_examination: "{{REQUIRED}}"
affected_object_or_process: "{{REQUIRED: representation, estimator, optimizer, ranking, controller, interface, system, or other target}}"
observable_symptom: "{{REQUIRED: description without a causal explanation}}"
condition: "{{REQUIRED}}"
diagnostic_measurement: "{{REQUIRED}}"
measured_effect: "{{REQUIRED: observed value or UNRESOLVED — EXP-* will measure it}}"
intermediate_effects: "{{REQUIRED: observed intermediate effects or N/A syntax}}"
task_level_effect: "{{REQUIRED: present, absent, or unresolved with measurement}}"
downstream_consequence: "{{REQUIRED: present, absent, or unresolved with measurement}}"
related_claim_ids: "{{REQUIRED: CLM-* IDs}}"
```

## 5. Causal Mechanism and Rivals

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

### 5.1 Causal Links

| Link ID | From claim ID | Relation | To claim ID | Supporting claim IDs | Contradicting claim IDs | Status |
|---|---|---|---|---|---|---|
| LINK-001 | {{REQUIRED: CLM-*}} | {{REQUIRED: one adjacent causal relation}} | {{REQUIRED: CLM-*}} | {{REQUIRED: CLM-* IDs}} | {{REQUIRED: CLM-* IDs or N/A syntax}} | {{REQUIRED: SUPPORTED \| CONTRADICTED \| UNRESOLVED}} |

### 5.2 Rival Explanations

<!-- Add at least two rival rows, including an artifact or confound when plausible. -->

| Rival ID | Explanation claim ID | Shared prediction | Discriminating prediction claim ID | Planned experiment ID | Status |
|---|---|---|---|---|---|
| RIV-001 | {{REQUIRED: CLM-*}} | {{REQUIRED}} | {{REQUIRED: CLM-*}} | {{REQUIRED: EXP-*}} | {{REQUIRED: ACTIVE \| REJECTED \| UNRESOLVED}} |

## 6. Preserved Invariant

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
invariant_id: "INV-001"
property: "{{REQUIRED}}"
preservation_type: "{{REQUIRED: EXACT | APPROXIMATE | EQUIVARIANT | STABLE | TASK-RELEVANT}}"
measurement: "{{REQUIRED}}"
tolerance: "{{REQUIRED}}"
task_relevance: "{{REQUIRED}}"
unnecessary_or_harmful_conditions: "{{REQUIRED: conditions or N/A syntax}}"
related_claim_ids: "{{REQUIRED: CLM-* IDs}}"
```

## 7. Candidate Mechanism Set

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

<!-- Keep 2–3 candidates. For COMPARE with three supplied candidates, place any extra fair baseline in Section 13 rather than adding a fourth candidate. -->

Allowed values:

```text
Source = SUPPLIED | GENERATED
Mechanism class = IN-DOMAIN | CROSS-DOMAIN | BASELINE
Evaluation role = PRIMARY | MINIMAL | SIMPLE-BASELINE | NULL-BASELINE
Candidate status = ACTIVE | SHORTLISTED | PROVISIONALLY-SELECTED | SELECTED | REJECTED | UNRESOLVED
```

Use `SELECTED` only after the relevant candidates have completed Direct Use, Novelty, Feasibility, Theory, and Falsification audits. Use `PROVISIONALLY-SELECTED` when downstream audit needs a focal candidate before final selection.

| Candidate ID | Source | Mechanism class | Evaluation role | Core operation | Addressed LINK-* IDs | Preserved INV-* IDs | New prediction CLM-* IDs | Candidate status |
|---|---|---|---|---|---|---|---|---|
| CAND-001 | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| CAND-002 | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |

### 7.1 Cross-Domain Transfer Mapping

| Candidate ID | Source problem | Source mechanism | Causal/mathematical correspondence | Source assumptions | Time-series mapping | Broken assumptions | New prediction claim IDs |
|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-* or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: value or N/A syntax}} | {{REQUIRED: CLM-* IDs or N/A syntax}} |

### 7.2 Candidate Freeze and Reference-Use Log

```yaml
candidate_set_frozen: "{{REQUIRED: YES | NO | N/A — supplied candidate set}}"
frozen_candidate_ids: "{{REQUIRED: CAND-* IDs}}"
freeze_basis: "{{REQUIRED: problem, causal links, and invariant used before pattern or method search}}"
```

| Reference | Consulted after freeze | Purpose | Structural mismatch or transfer risk found | Effect on candidate set |
|---|---|---|---|---|
| {{REQUIRED: consulted pattern card ID, mechanism-transfer, or N/A syntax}} | {{REQUIRED: YES \| NO \| N/A syntax}} | {{REQUIRED}} | {{REQUIRED: at least one mismatch/risk when consulted, otherwise N/A syntax}} | {{REQUIRED: retained, bounded, rejected, or N/A syntax}} |

## 8. Direct-Use Assessment

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

Allowed values:

```text
Finding type = FAILURE | BROKEN-ASSUMPTION | BOUNDARY-CONDITION | NONE
Disposition = ADAPT | BOUND-CLAIM | REJECT | NO-ADAPTATION-REQUIRED
```

| Finding ID | Candidate ID | Finding type | Finding | Evidence claim IDs | Disposition | Consequence |
|---|---|---|---|---|---|---|
| FIND-001 | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: finding or N/A syntax for NONE}} | {{REQUIRED: CLM-* IDs}} | {{REQUIRED}} | {{REQUIRED}} |

## 9. Time-Series Adaptation and Component Contracts

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

### 9.1 Adaptation Summary

| Candidate ID | Adaptation status | Repaired FIND-* IDs | Adapted system ID |
|---|---|---|---|
| {{REQUIRED: CAND-*}} | {{REQUIRED: ADAPTED \| NO-ADAPTATION-REQUIRED}} | {{REQUIRED: FIND-* IDs or N/A syntax}} | {{REQUIRED: SYS-* or N/A syntax}} |

### 9.2 System Definition

<!-- Define every SYS-* referenced anywhere in the dossier. Use one N/A row only when no adapted system exists. -->

| System ID | Base candidate ID | Component IDs | Input contract | Output contract | Component connections | Training path | Inference path | State and constraints | Related claim IDs |
|---|---|---|---|---|---|---|---|---|---|
| {{REQUIRED: SYS-* or N/A syntax}} | {{REQUIRED: CAND-* or N/A syntax}} | {{REQUIRED: COMP-* IDs or N/A syntax}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: CLM-* IDs or N/A syntax}} |

### 9.3 Component Contracts

| Component ID | Candidate or system ID | Repairs FIND-* IDs | Primary responsibility | Material secondary effects | Existence reason | Mathematical/computational operation | Input/output contract | Risk | Mitigation | Ablation EXP-* IDs |
|---|---|---|---|---|---|---|---|---|---|---|
| {{REQUIRED: COMP-* or N/A syntax}} | {{REQUIRED: CAND-*, SYS-*, or N/A syntax}} | {{REQUIRED: IDs or N/A syntax}} | {{REQUIRED}} | {{REQUIRED: effects or N/A syntax}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |

## 10. Novelty Audit

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
novelty_subject_frozen: "{{REQUIRED: YES | NO}}"
novelty_subject_freeze_basis: "{{REQUIRED: frozen CAND-*, SYS-*, COMP-*, and current CORE contribution CLM-* IDs}}"
assessment_subject_candidate_ids: "{{REQUIRED: CAND-* IDs}}"
assessment_subject_system_ids: "{{REQUIRED: SYS-* IDs or N/A — no adapted system}}"
assessment_subject_component_ids: "{{REQUIRED: COMP-* IDs or N/A syntax}}"
declared_contribution_claim_ids: "{{REQUIRED: CLM-* IDs declared as CORE contributions at audit entry}}"
current_core_contribution_claim_ids: "{{REQUIRED: CLM-* IDs remaining CORE after any explicit refreeze, or N/A syntax}}"
search_boundary: "{{REQUIRED: sources, queries, dates, and scope}}"
```

```text
Neighbor role token = SAME-PROBLEM | SAME-MECHANISM | SAME-AXIS | SAME-COMBINATION | NEGATIVE-OR-BOUNDARY
```

Use one or more comma-separated neighbor-role tokens. Use `CAND-*` as the audit subject when no adaptation exists and `SYS-*` when the claimed contribution depends on an adapted system. Keep the contribution claim ID distinct from every distinguishing consequence claim ID.

| Candidate ID | Audit subject ID | Contribution claim ID | Affected component IDs | Neighbor role | Closest work | Modeled object | Information flow | Responsibility boundary | Constraint or granularity | Inherited part | Proposed difference | Why it matters | Distinguishing consequence claim IDs | Citation |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-*}} | {{REQUIRED: CAND-* or SYS-*}} | {{REQUIRED: declared contribution CLM-*}} | {{REQUIRED: COMP-* IDs or N/A syntax}} | {{REQUIRED: one or more allowed tokens}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: CLM-* IDs distinct from the contribution claim ID}} | {{REQUIRED}} |

| Candidate ID | Novelty status | Surviving core contribution claim IDs | Covered or downgraded contribution claim IDs | Unresolved contribution claim IDs | Bounded novelty claim | Unresolved overlap | Supporting claim IDs |
|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-*}} | {{REQUIRED: PASS \| CONDITIONAL \| FAIL \| UNKNOWN}} | {{REQUIRED: CLM-* IDs or N/A syntax}} | {{REQUIRED: CLM-* IDs or N/A syntax}} | {{REQUIRED: CLM-* IDs or N/A syntax}} | {{REQUIRED}} | {{REQUIRED: overlap or N/A syntax}} | {{REQUIRED: CLM-* IDs}} |

## 11. Feasibility Assessment

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```text
System status = SATISFIED | UNSATISFIED | UNRESOLVED
```

```yaml
assessment_subject_candidate_ids: "{{REQUIRED: CAND-* IDs}}"
assessment_subject_system_ids: "{{REQUIRED: SYS-* IDs or N/A — no adapted system}}"
assessment_subject_component_ids: "{{REQUIRED: COMP-* IDs or N/A syntax}}"
```

| Candidate or system ID | System aspect | Contract or requirement | Executability critical | Status | Evidence claim IDs | Risk | Mitigation |
|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-* or SYS-*}} | Responsibility boundary | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | End-to-end data flow | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Input/output and state | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Tensor shapes and mathematical operations | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Training signal and gradient/estimator path | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Constraint enforcement | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Numerical and optimization dynamics | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Training/inference consistency | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |
| {{REQUIRED: CAND-* or SYS-*}} | Compute, memory, and data | {{REQUIRED}} | {{REQUIRED: YES \| NO}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |

| Candidate or system ID | Interface valid | Optimization path valid | Mechanism testable | End-to-end executable | Resources within budget | Minimum viable experiment ID | Fallback design |
|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-* or SYS-*}} | {{REQUIRED: YES \| NO \| UNRESOLVED}} | {{REQUIRED: YES \| NO \| UNRESOLVED}} | {{REQUIRED: YES \| NO \| UNRESOLVED}} | {{REQUIRED: YES \| NO \| UNRESOLVED}} | {{REQUIRED: YES \| NO \| UNRESOLVED}} | {{REQUIRED: EXP-*}} | {{REQUIRED}} |

## 12. Theory Boundary

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```yaml
assessment_subject_candidate_ids: "{{REQUIRED: CAND-* IDs}}"
assessment_subject_system_ids: "{{REQUIRED: SYS-* IDs or N/A — no adapted system}}"
assessment_subject_component_ids: "{{REQUIRED: COMP-* IDs or N/A syntax}}"
declared_theory_claim_ids: "{{REQUIRED: all CLM-* IDs assessed in this section}}"
```

<!-- Assess theory per CLM-* row. Do not assign one T-level to the whole candidate. Include at least the core mechanism-consistency claim. -->

| Theory subject ID | Theory claim ID | Theory role | Theory maturity | Assumption claim IDs | Assumption applicability | Consistency conditions | Formalization status | Formal claim | Guarantees | Does not guarantee | Proof/derivation basis | Weakest assumption | Empirical counterpart claim IDs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| {{REQUIRED: CAND-*, SYS-*, or COMP-*}} | {{REQUIRED: CLM-*}} | {{REQUIRED: CONSISTENCY \| FORMAL-PROPERTY \| LIMITATION}} | {{REQUIRED: T0-ASSUMED \| T1-DERIVED \| T2-PROVED}} | {{REQUIRED: ASSUMPTION CLM-* IDs or N/A — unconditional claim}} | {{REQUIRED: SUPPORTED \| UNRESOLVED \| CONTRADICTED}} | {{REQUIRED}} | {{REQUIRED: FORMAL-CLAIM \| NO-FORMAL-THEOREM-CLAIMED}} | {{REQUIRED: bounded claim or N/A syntax}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: outline/source or N/A syntax}} | {{REQUIRED}} | {{REQUIRED: CLM-* IDs or N/A — permitted only for a non-core purely formal limitation or counterexample}} |

| Candidate or system ID | Overall theory status | Decisive theory claim IDs |
|---|---|---|
| {{REQUIRED: CAND-* or SYS-*}} | {{REQUIRED: SATISFIED \| UNSATISFIED \| UNRESOLVED}} | {{REQUIRED: CLM-* IDs}} |

## 13. Claim-to-Falsification Matrix

<!-- Preserve diagnostic EXP-* IDs created during Stages 2–4. Extend them at Stage 11; do not renumber or duplicate those experiments. -->

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
```

```text
Experiment status = PLANNED | RUNNING | COMPLETED | INVALIDATED
```

Planned or running experiments do not support a claim. Only a valid observed result with source references may be linked as evidence in Section 3.

| Experiment ID | Assessment subject IDs | Claim IDs | Test/intervention | Status | Expected result | Falsifying result | Observed result | Result source refs | Rival explanation claim IDs | Ablation | Fairest simple baseline | What the result cannot prove | Decision change if falsified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXP-001 | {{REQUIRED: NEED-*, FAIL-*, CAND-*, or SYS-* IDs}} | {{REQUIRED: CLM-* IDs}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: result or PENDING syntax}} | {{REQUIRED: refs, PENDING syntax, or N/A syntax if invalidated}} | {{REQUIRED: CLM-* IDs}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} |

```yaml
core_claim_ids: "{{REQUIRED: all CORE CLM-* IDs}}"
covered_core_claim_ids: "{{REQUIRED: CORE CLM-* IDs referenced by EXP-* rows}}"
uncovered_core_claim_ids: "{{REQUIRED: IDs or N/A syntax}}"
coverage_complete: "{{REQUIRED: YES | NO; derive from the three fields above}}"
```

<!--
coverage_complete: NO leaves G11 EVALUATED and UNRESOLVED — never satisfied — so the decision is capped at NEED-EVIDENCE, and each uncovered CORE claim must be named as the smallest next action. See SKILL.md Stage 11.
-->

## 14. Compiled Research Argument

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
compilation_mode: "DERIVED-ONLY"
```

<!-- Compile only from existing IDs. Do not introduce new claims or stronger wording than the cited rows support. -->

| Argument element | Compiled statement | Source IDs |
|---|---|---|
| Need | {{REQUIRED}} | {{REQUIRED}} |
| Observable failure | {{REQUIRED}} | {{REQUIRED}} |
| Causal mechanism | {{REQUIRED}} | {{REQUIRED}} |
| Preserved invariant | {{REQUIRED}} | {{REQUIRED}} |
| Selected or provisional mechanism | {{REQUIRED}} | {{REQUIRED}} |
| Direct-use assessment | {{REQUIRED}} | {{REQUIRED}} |
| Adaptation or no-adaptation result | {{REQUIRED}} | {{REQUIRED}} |
| Mechanism-level novelty | {{REQUIRED}} | {{REQUIRED}} |
| Feasibility basis | {{REQUIRED}} | {{REQUIRED}} |
| Theory boundary | {{REQUIRED}} | {{REQUIRED}} |
| Decisive falsifier | {{REQUIRED}} | {{REQUIRED}} |

## 15. Stage-Gate Summary

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
compilation_mode: "DERIVED-ONLY"
```

Allowed values:

```text
Evaluation status = EVALUATED | DEFERRED
State = SATISFIED | UNRESOLVED | UNSATISFIED
Failure mode = null | REPAIRABLE | CONTRADICTED
```

Use `failure_mode = null` unless `state = UNSATISFIED`. For a deferred gate, use `evaluation_status = DEFERRED`, `state = UNRESOLVED`, and name the earlier dependency; do not pretend the gate was evaluated.

| Gate | Evaluation status | State | Failure mode | Decisive ledger IDs | Blocking item | Earliest return stage |
|---|---|---|---|---|---|---|
| G0 Boundary | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G1 Need | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G2 Failure | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G3 Causality | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G4 Invariant | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G5 Candidates | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G6 Direct Use | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G7 Adaptation | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G8 Novelty | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G9 Feasibility | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G10 Theory | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |
| G11 Falsification | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED}} | {{REQUIRED: blocker or N/A syntax}} | {{REQUIRED: stage or N/A syntax}} |

## 16. Final Decision

```yaml
section_status: "{{REQUIRED: NOT-STARTED | ACTIVE | COMPLETE | BLOCKED}}"
status_reason: "{{REQUIRED: progress rationale or blocker}}"
compilation_mode: "DERIVED-ONLY"
```

```yaml
decision: "{{REQUIRED: GO | PIVOT | NEED-EVIDENCE | KILL}}"
decision_subject_type: "{{REQUIRED: DOSSIER | CANDIDATE | ADAPTED-SYSTEM}}"
decision_subject_id: "{{REQUIRED: DOS-*, CAND-*, or SYS-* ID}}"
decisive_ledger_ids: "{{REQUIRED: CLM-* IDs}}"
highest_risk_assumption_claim_id: "{{REQUIRED: CLM-* ID or N/A syntax}}"
smallest_next_action: "{{REQUIRED}}"
stage_to_revisit: "{{REQUIRED: stage or N/A syntax}}"
reusable_observation_claim_ids: "{{REQUIRED: CLM-* IDs or N/A syntax}}"
decision_rationale: "{{REQUIRED: concise evidence-bounded rationale}}"
unresolved_gate_ids: "{{REQUIRED: gate IDs or N/A syntax; derive from Section 15}}"
repairable_gate_ids: "{{REQUIRED: gate IDs or N/A syntax; derive from Section 15}}"
contradicted_gate_ids: "{{REQUIRED: gate IDs or N/A syntax; derive from Section 15}}"
decision_rule_triggered: "{{REQUIRED: ALL-SATISFIED | UNRESOLVED-EVIDENCE | REPAIRABLE-FAILURE | FATAL-CONTRADICTION}}"
decision_consistency_check: "{{REQUIRED: PASS | FAIL}}"
```

Decision consistency rules:

- `GO`: every gate is EVALUATED and SATISFIED; novelty is PASS; no unresolved, repairable, or contradicted gate exists.
- `NEED-EVIDENCE`: at least one decision-relevant gate is UNRESOLVED, no gate is UNSATISFIED, and the smallest decisive test or search is named.
- `PIVOT`: at least one gate is UNSATISFIED + REPAIRABLE and no fatal contradiction makes repair meaningless.
- `KILL`: at least one decisive gate is UNSATISFIED + CONTRADICTED and no substantive repair remains.
- Set `decision_consistency_check: PASS` only when the stated decision follows the matching rule and all listed gate IDs agree with Section 15.
