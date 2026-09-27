# Novelty Audit

Use this reference to execute Stage 8 as a bounded contribution-delta audit. Compare the frozen candidate or adapted system against its closest technical neighbors, audit every claimed CORE contribution separately, and compile exactly one evidence-bounded novelty status per candidate. Do not regenerate the method, equate search absence with novelty, or use novelty to substitute for mechanism evidence, feasibility, or theoretical soundness.

## Contents

1. Purpose and Boundary
2. Entry Conditions and Subject Freeze
3. Required Inputs and Dossier Updates
4. Compile Atomic Contribution Contracts
5. Define the Bounded Search Protocol
6. Identify the Closest Technical Neighbors
7. Construct the Claim-Level Contribution Delta
8. Test Substantiveness and Obviousness
9. Separate Adaptation, Combination, and Supporting Engineering
10. Require Distinguishing Consequences
11. Compile the Candidate-Level Novelty Status
12. Route Repairs and Update G8
13. Anti-Patterns

## 1. Purpose and Boundary

- Audit what a frozen research subject contributes relative to the closest prior work; do not design a new subject during search.
- Define novelty as a positive, technically specific delta supported by direct comparison, not as failure to find an exact title, phrase, module name, or application.
- Trace every claimed delta to a diagnosed problem, causal or theoretical gap, invariant, broken assumption, or component responsibility.
- Distinguish a research contribution from a useful inherited mechanism, implementation choice, feasibility repair, optimization aid, or engineering safeguard.
- Require a distinguishing mechanism behavior, empirical prediction, counterexample, formal consequence, or result under weaker assumptions. Do not require every contribution to masquerade as an empirical performance prediction.
- Use primary sources to support technical comparisons. Use reviews, surveys, indexes, and secondary explanations only for discovery or terminology expansion.
- Preserve negative results, equivalent terminology, adjacent-field precedents, and unresolved overlap.
- Audit objective and theoretical-property contributions for novelty here, but defer objective effectiveness, theorem correctness, and assumption validity to the appropriate evidence, feasibility, and theory gates.

Use these two traces:

```text
FAIL-* / LINK-* / INV-* / FIND-*
-> reason an inherited design is insufficient
-> smallest research delta
-> changed object, mechanism, information flow, responsibility, constraint,
   granularity, objective, or theoretical property
-> distinguishing consequence CLM-*
```

```text
CORE contribution CLM-*
-> bounded terminology and neighbor search
-> inherited elements and exact delta
-> substantiveness and bridge-evidenced obviousness audit
-> claim-level outcome
-> one candidate-level novelty status
```

## 2. Entry Conditions and Subject Freeze

### 2.1 Require evaluated and satisfied upstream gates

Before entering Stage 8:

- [ ] Require G0–G7 to be `EVALUATED` for the audit subject wherever those gates apply.
- [ ] Require the subject's applicable upstream gates to be `SATISFIED`; do not treat `section_status: COMPLETE` as evidence that an upstream argument holds.
- [ ] Require every referenced `CAND-*`, `SYS-*`, `COMP-*`, `CLM-*`, `FIND-*`, and `INV-*` to exist and have stable IDs.
- [ ] Require the actual training and inference subject, component connections, and responsibility boundaries to be defined sufficiently to compare.
- [ ] Require a dated evidence cutoff.

If an applicable upstream gate is unresolved or unsatisfied, defer G8 and return to the earliest affected stage. A literature search may still be recorded as background evidence, but do not issue a positive novelty status for an unstable subject.

### 2.2 Select the actual audit subject

- Use `CAND-*` when the candidate is used directly and Section 9 records `NO-ADAPTATION-REQUIRED`.
- Use `SYS-*` when the claimed contribution depends on an adapted system, component interaction, changed information flow, or system-level responsibility boundary.
- Treat the base `CAND-*` as inherited foundation when `SYS-*` is the subject.
- List every `COMP-*` participating in the claimed delta.
- Scope a comparison row to one `COMP-*` only when the contribution and distinguishing consequence belong to that component independently of system interactions; retain its enclosing `CAND-*` or `SYS-*` as the audit subject.
- Keep the final novelty status candidate-level even when the actual comparison subject is a `SYS-*`.

### 2.3 Distinguish the two freezes

Do not confuse:

```text
Candidate-set freeze at Stage 5
  = candidate identities, roles, target-side mechanisms, and attribution baseline

Novelty-subject freeze after Stage 7
  = actual CAND-* or SYS-* implementation concept, participating COMP-* IDs,
    CORE contribution claims, responsibility boundaries, and distinguishing consequences
```

Set `novelty_subject_frozen: YES` before novelty search. Record the frozen IDs, `declared_contribution_claim_ids`, current CORE claims, and claim basis. Do not change the operation, components, connections, responsibilities, or CORE contribution claims while preserving the same freeze.

### 2.4 Apply entry modes

- **`GENERATE`:** Audit the final subject produced by Stages 5–7. Do not use search findings to silently redesign it.
- **`AUDIT`:** Preserve the supplied subject and claims. Require missing upstream definitions or gate evidence before issuing a positive status.
- **`COMPARE`:** Freeze each subject independently; use the same evidence cutoff, search protocol, inclusion rules, and stopping condition. Do not require the same paper count or identical query count.
- **`REPAIR`:** Re-enter at the earliest stage whose substance changes. Re-freeze the novelty subject before re-auditing.

## 3. Required Inputs and Dossier Updates

Read before auditing:

- [ ] Sections 1–9 of the current dossier and the Stage-Gate Summary for G0–G7.
- [ ] All CORE and SUPPORTING `CLM-*` records linked to the proposed contribution.
- [ ] The candidate's new prediction claims, component contracts, system definition, and direct-use findings.
- [ ] User-supplied novelty claims and citations without treating them as conclusions.
- [ ] `references/personal-research-priors.md` for the user's innovation and attribution rules.
- [ ] The canonical fields in `assets/idea-dossier-template.md`.

Update only:

- [ ] Section 3 with primary-literature findings, equivalence claims, overlap claims, and evidence-bounded contribution claims.
- [ ] Section 10 with the frozen audit subjects, CORE contribution claims, search boundary, claim-level comparisons, and one candidate-level status.
- [ ] Section 15 with G8 and the earliest return stage.

Do not modify Sections 7–9 while claiming that the subject remains frozen. Route a substantive repair back to the appropriate earlier stage. Do not complete Stage 11 experiments, Stage 9 feasibility, Stage 10 theory soundness, or the final decision here.

Treat these as internal compilation objects, not new dossier sections:

| Novelty audit object | Compile into the canonical dossier |
|---|---|
| Novelty Subject Freeze | Section 10 freeze fields and assessment-subject IDs |
| Atomic Contribution Contract | Section 3 CORE `CLM-*`; Section 10 contribution-claim rows |
| Contribution Fingerprint | Section 10 search boundary and comparison axes |
| Neighbor Role | Section 10 allowed neighbor-role tokens |
| Claim-Level Outcome | Section 10 surviving, covered or downgraded, and unresolved fields |
| Repair Route | Section 15 G8 blocking item and earliest return stage |

## 4. Compile Atomic Contribution Contracts

Decompose the subject before searching. Use one contract for every contribution declared CORE at audit entry:

```text
Candidate ID:
Audit subject ID:
Contribution claim CLM-*:
Contribution claim type and centrality:
Affected COMP-* IDs:
Inherited foundation:
Diagnosed or theoretical reason for change:
Addressed FAIL-* / LINK-* / FIND-* IDs:
Preserved INV-* IDs:
Smallest proposed delta:
Changed research axis:
Distinguishing consequence CLM-* IDs:
Claim boundary:
```

- [ ] Make the smallest delta precise enough to compare with a paper's operation, objective, constraint, or formal statement.
- [ ] State what is inherited before stating what is new.
- [ ] Link a design contribution to the diagnosed failure or broken assumption it repairs.
- [ ] Link a theoretical contribution to an explicit gap, stronger conclusion, weaker assumption, counterexample, or previously uncharacterized boundary.
- [ ] Keep the contribution claim distinct from its consequence claims. A contribution claim is normally a `MECHANISM` or `EXPLANATION`; a predicted empirical consequence is normally a `HYPOTHESIS`.
- [ ] Do not let one `CLM-*` assert both “the design is different” and “therefore its prediction is evidence of difference.”
- [ ] Mark a useful but inherited or implementation-only element `SUPPORTING` or `CONTEXT`, not `CORE`.

Do not proceed when the proposed contribution cannot be stated without paper-level slogans such as “a novel framework,” “a new architecture,” or “first application.”

## 5. Define the Bounded Search Protocol

### 5.1 Build a contribution fingerprint

Derive search terms from each atomic contract:

- target problem and observable failure;
- modeled object or representation;
- causal or mathematical operation;
- preserved invariant;
- information-flow change;
- component responsibility;
- constraint or search granularity;
- objective or optimization target;
- theoretical property, assumptions, or formal consequence;
- equivalent terminology, equations, functional descriptions, and adjacent-field names.

Search the contribution fingerprint, not only the candidate's chosen method name.

### 5.2 Cover the neighbor roles

Attempt to identify the strongest available neighbor for each applicable role:

- `SAME-PROBLEM`: addresses the same failure or research gap;
- `SAME-MECHANISM`: uses the same operative causal or mathematical mechanism;
- `SAME-AXIS`: changes the same object, information flow, responsibility, invariant, constraint, granularity, objective, or theoretical property;
- `SAME-COMBINATION`: combines the same mechanisms or responsibilities at system level;
- `NEGATIVE-OR-BOUNDARY`: reports failure, equivalence, limitation, counterexample, or a relevant boundary.

One work may serve multiple roles. Do not force one different paper per role, and do not substitute a weak paper merely to fill a category.

### 5.3 Record the search boundary

Record in `search_boundary`:

```text
Evidence cutoff:
Databases, proceedings, and archives:
Exact query families:
Terminology and synonym families:
Backward and forward citation traversal:
Primary-source inclusion rules:
Exclusions:
Unavailable sources or unresolved terminology:
Stopping condition:
```

- Use primary papers, official proceedings, author manuscripts, or formal technical reports for final comparisons.
- Use surveys, reviews, blogs, and indexes only to discover terminology or primary sources.
- Trace citations backward and forward when they can reveal an earlier mechanism, equivalent formulation, or later combination.
- Consolidate multiple versions of the same work; compare against the technically relevant version and cite it precisely.
- Search adjacent fields when the mechanism or mathematical structure predates its time-series use.
- Search negative results and limitations; do not hide a failed close precedent.
- Stop when new justified query families and citation paths return already reviewed technical families and every CORE contribution has a credible closest neighbor or a named unresolved search gap.

Treat this stopping condition as bounded search saturation, not proof that no prior work exists.

## 6. Identify the Closest Technical Neighbors

Choose neighbors by technical distance, not venue prestige, citation count, author group, title similarity, or chronology alone.

For every CORE contribution claim:

- [ ] Include the strongest overlap, not a convenient weak baseline.
- [ ] Compare the actual operation, information access, objective, constraint, and formal claim rather than abstract wording.
- [ ] Inspect appendices or formal definitions when the main narrative hides equivalence.
- [ ] Check whether different terminology implements the same responsibility or operator.
- [ ] Include same-problem work even when its mechanism differs.
- [ ] Include same-mechanism work even when its task differs.
- [ ] Include same-axis or same-combination work needed to test whether the proposed delta is routine.
- [ ] Record missing access or ambiguous equivalence as unresolved overlap.

Do not use the personal or ICLR pattern indexes and cards as novelty evidence. A cited source associated with a pattern may be used only after reading and citing its primary technical record independently.

## 7. Construct the Claim-Level Contribution Delta

Create at least one Section 10 comparison row for every contribution declared CORE at audit entry and each decisive closest work. Preserve those rows if a claim is later covered or downgraded. Reuse the same candidate ID across rows while keeping the `Audit subject ID`, contribution claim, affected components, and neighbor role explicit.

Compare all applicable axes:

- problem framing and diagnosed gap;
- modeled object or representation;
- preserved invariant;
- causal or mathematical mechanism;
- information flow and information access;
- component responsibility and interaction;
- constraint or granularity;
- objective;
- theoretical assumptions and property;
- distinguishing empirical or formal consequence.

For each row, state:

```text
Inherited part:
Exact shared element:
Smallest proposed difference:
Why the diagnosed or theoretical gap requires it:
What behavior or formal consequence changes:
What the comparison does not establish:
```

Use a positive contrast whenever possible:

```text
Work W performs operation A on object X under conditions S.
The frozen subject inherits I but changes delta D because of gap G.
D changes axis Z and entails distinguishing consequence CLM-P.
```

Do not write “no work does D” unless the statement is explicitly bounded by the recorded search. Search absence alone supports `not found within the stated boundary`, never novelty.

Do not mark a technically correct mechanism claim `CONTRADICTED` merely because prior work already contains it. Record the coverage with primary-literature evidence, classify that claimed contribution as covered, and revise its contribution centrality only through an explicit claim refreeze.

## 8. Test Substantiveness and Obviousness

### 8.1 Test research substance

Treat a delta as potentially substantive only when it changes at least one research axis and has a gap-derived reason plus a distinguishing consequence. Inspect whether it changes:

- what is modeled;
- what information is available or preserved;
- how responsibilities are divided;
- what operation or interaction occurs;
- what constraint or granularity defines the valid design space;
- what objective is optimized;
- what assumptions or formal property hold.

Treat renaming, parameter-count changes, routine format conversion, ordinary hyperparameter selection, first application to time series, and unexplained structural difference as insufficient on their own.

### 8.2 Require bridge evidence for obviousness

Do not declare a delta obvious because it looks short or familiar. Support an obviousness conclusion with a documented bridge:

```text
closest work W
+ substitution, adaptation, or combination rule R documented in prior work or standard practice
+ compatibility conditions S already known to hold
-> frozen subject without a new diagnosis, invariant, constraint, interaction, or consequence
```

- Cite the source for `R` and the evidence for compatibility conditions `S`.
- Treat a one-step change as non-decisive when the original assumptions fail, a new invariant is required, responsibilities change, or a consequence cannot be derived from the neighbor.
- Use `CONDITIONAL`, not `FAIL`, when the bridge is plausible but its rule or compatibility evidence remains unresolved.
- Do not use the auditor's intuition, popularity of a component, or retrospective simplicity as bridge evidence.

### 8.3 Apply pressure tests

- **One-step substitution:** Can a documented standard substitution produce the subject under already-satisfied conditions?
- **Responsibility equivalence:** Do differently named components perform the same operation with the same information and consequence?
- **Granularity equivalence:** Does prior work already search or control the same atomic decisions under the same semantic interface?
- **Standard adaptation:** Does the delta only make an existing method accept the target shape, format, or training loop?
- **Combination path:** Do existing components combine independently, or does the proposal introduce a gap-required interaction with a combination-specific consequence?
- **Consequence equivalence:** Would the closest work and proposal make the same conditional empirical or formal predictions?

## 9. Separate Adaptation, Combination, and Supporting Engineering

### 9.1 Audit adaptation novelty

- Treat a change that merely makes the source mechanism runnable as feasibility support, not automatically as novelty.
- Treat an adaptation as a possible contribution only when a target-specific broken assumption requires a substantive change in operation, information flow, responsibility, constraint, objective, or formal property.
- Compare the adapted `SYS-*`, not only its base `CAND-*`, when the delta depends on the adaptation.
- Preserve inherited source mechanisms and standard safeguards as inherited parts.
- Require an adaptation-specific distinguishing consequence.

### 9.2 Audit combination novelty

- Treat independently stacked known components with additive responsibilities as an implementation combination unless a positive contrast shows otherwise.
- Treat system-level interaction as a possible contribution when one component changes another component's validity conditions, information access, optimization role, or observable behavior.
- Compare the full `SYS-*` with the closest known combination and compare its participating components with their individual precedents.
- Require a combination-specific consequence or interaction claim that neither component alone entails.

### 9.3 Classify supporting engineering honestly

Keep legality checks, output typing, shape adapters, ordinary residual paths, standard linear heads, stability clamps, and similar safeguards `SUPPORTING` unless the audit establishes a substantive gap-derived delta. A good feasibility repair may be essential to the method without being a novelty contribution.

Do not require every component to be novel. Require every claimed CORE contribution to survive the audit.

## 10. Require Distinguishing Consequences

Keep the contribution claim and consequence claims as different `CLM-*` records.

Accept one or more of:

- a mechanism-specific intermediate behavior;
- an empirical prediction that differs by condition or intervention;
- an invariant-preservation consequence distinct from downstream performance;
- a boundary regime where the proposal and neighbor diverge;
- a counterexample to an inherited claim;
- a formal result under weaker assumptions, a stronger or different conclusion, or a newly characterized limitation.

Stage 8 asks:

```text
Does the frozen subject entail a consequence that its closest neighbor does not?
```

Stage 11 asks:

```text
Which intervention, control, metric, and decision rule can falsify that consequence?
```

Do not complete the full Stage 11 experiment design here. Do not treat a planned or observed consequence as evidence that the contribution is novel; novelty evidence comes from the technical contrast with prior work. If no distinct empirical or formal consequence can be derived, the contribution cannot support `PASS`.

## 11. Compile the Candidate-Level Novelty Status

First classify each contribution declared CORE at audit entry as surviving, covered or downgraded, or unresolved. Record the remaining CORE set after any explicit refreeze. Then compile exactly one status per candidate; do not average claims or candidates.

### `PASS`

Assign only when:

- at least one CORE contribution survives a direct closest-neighbor comparison as substantive and not bridge-evidenced obvious;
- no unresolved overlap could reasonably cover that surviving contribution;
- every other originally CORE claim that is covered has been explicitly downgraded to `SUPPORTING` or inherited;
- the contribution contract and novelty subject have been re-frozen after any downgrade;
- all affected comparison rows have been re-run after the refreeze;
- a distinct empirical or formal consequence exists;
- the bounded novelty claim states what is inherited, what survives, and the search boundary.

Do not assign `PASS` while a failed CORE claim remains silently advertised as a contribution.

### `CONDITIONAL`

Assign when a concrete, positive, potentially substantive delta has been identified, but an equivalent combination, terminology family, claim scope, bridge rule, or overlap that could cover it remains unresolved.

### `FAIL`

Assign when every CORE contribution is covered, is a documented standard substitution or adaptation, lacks a distinguishing consequence, or reduces to cosmetic or implementation-only difference after fair comparison.

### `UNKNOWN`

Assign when the audit subject, CORE claims, terminology space, primary-source access, search coverage, or closest-neighbor identification is insufficient to formulate a reliable positive delta.

Use `CONDITIONAL` only when a specific positive delta hypothesis exists. Use `UNKNOWN` when the audit cannot yet identify such a delta reliably. Never assign a numeric novelty score.

## 12. Route Repairs and Update G8

Do not hard-code every repair to Stage 5 or Stage 7. Return to the earliest stage whose substance changes:

| Audit finding | Required route |
|---|---|
| Only the novelty claim scope is too broad; the subject is unchanged | Narrow the claim in Stage 8, explicitly re-freeze the contribution contract, and re-run affected comparisons |
| A component operation, responsibility, or connection must change | Return to Stage 7 |
| The core candidate mechanism must change | Return to Stage 5 |
| Applicable primary evidence under compatible assumptions invalidates a causal link | Return to Stage 3 |
| Applicable primary evidence under compatible assumptions invalidates the invariant or its necessity | Return to Stage 4 |
| Applicable primary evidence in the target regime invalidates the observable failure | Return to Stage 2 |
| Applicable primary evidence in the target regime invalidates the solution-independent need | Return to Stage 1 |
| All CORE claims fail and no substantive pivot remains | Mark G8 `UNSATISFIED + CONTRADICTED`; let the main workflow consider `KILL` |

Preserve old claims, comparisons, and candidate IDs when recording a pivot; do not rewrite audit history to make the repaired subject appear independently generated.

Apply G8 as follows:

- Candidate `PASS`: G8 may be `SATISFIED` for that candidate when the audit is complete.
- Candidate `CONDITIONAL` or `UNKNOWN`: G8 is `UNRESOLVED`; name the smallest decisive search or scope clarification.
- Candidate `FAIL` with a substantive repair path: G8 is `UNSATISFIED + REPAIRABLE`.
- Candidate `FAIL` with no substantive repair: G8 is `UNSATISFIED + CONTRADICTED`.

Completing the audit does not imply G8 is satisfied. In `COMPARE`, retain separate claim rows and statuses for every candidate under the common protocol. A final `GO` remains impossible unless the selected candidate has novelty `PASS` and every other gate is satisfied.

Return control to `SKILL.md` after updating Section 10 and G8. Do not perform feasibility, proof, complete falsification, or final-decision work here.

## 13. Anti-Patterns

- Do not begin novelty search before freezing the actual `CAND-*` or `SYS-*` subject and its CORE claims.
- Do not equate completed sections with satisfied upstream gates.
- Do not audit only the base candidate when the claimed contribution exists in the adapted system.
- Do not use one self-confirming `CLM-*` for both the contribution and its consequence.
- Do not compare only against same-task work while ignoring same-mechanism or adjacent-field precedents.
- Do not choose weak neighbors to create an easy contrast.
- Do not call a one-step change obvious without bridge evidence and compatible conditions.
- Do not call a standard adaptation, format repair, stability aid, or constrained head novel merely because it is necessary.
- Do not call a component combination novel without a combination-specific interaction and consequence.
- Do not require every useful component to be novel.
- Do not let one surviving claim conceal other still-advertised CORE claims that were covered.
- Do not silently downgrade, narrow, or replace a contribution claim without re-freezing and re-auditing it.
- Do not turn a distinguishing prediction into empirical evidence of novelty.
- Do not complete Stage 11 experiment design, Stage 9 feasibility, Stage 10 proof, or the final decision here.
