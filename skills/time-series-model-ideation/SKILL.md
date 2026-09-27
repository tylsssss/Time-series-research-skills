---
name: time-series-model-ideation
description: Develop, audit, compare, repair, and refine research ideas for time-series models. Use for architecture, representation, information-flow, mechanism-transfer, NAS, objective, and theoretical-claim ideation. Do not use for implementing or debugging a frozen method, literature-only summaries, paper polishing, or final figures.
---

# Time-Series Model Ideation

## Role and Boundary

Act as a research-argument compiler. Build or audit one traceable chain:

```text
Need
-> Observable Failure
-> Causal Mechanism
-> Preserved Invariant
-> Candidate Mechanisms
-> Direct-Use Assessment
-> Time-Series Adaptation
-> Novelty Audit
-> Feasibility
-> Theory Boundary
-> Falsification
-> GO | PIVOT | NEED-EVIDENCE | KILL
```

Keep the work at the research-idea level. Complete the Idea Dossier before handing implementation, paper prose, or figures to another workflow. Stop after the dossier.

## Global Contract

Use `assets/idea-dossier-template.md` as the sole authority for output headings, fields, enums, ID namespaces, lifecycle values, and field order. Update one dossier in place; do not create stage-specific reports or new output sections.

Apply this authority order:

```text
evidence and task constraints
> canonical gate rules
> confirmed personal research priors
> structural analogies and familiar patterns
```

Enforce these rules in every stage:

- Keep claims in the typed `CLM-*` ledger and keep other entities in their dedicated namespaces.
- Separate observations, explanations, mechanisms, hypotheses, assumptions, and evidence.
- Treat planned or running experiments as plans, never as supporting evidence.
- Record missing decision-relevant evidence as `UNRESOLVED` with `E0` inside the active section.
- Preserve supplied evidence, rejected candidates, null results, and stable IDs.
- Return to the earliest affected stage whenever a later audit changes a causal link, invariant, candidate identity, component responsibility, or CORE contribution.
- Keep candidate and system IDs explicit in `COMPARE`; never average heterogeneous subjects.
- Use primary sources for literature claims. Treat search absence only as bounded non-discovery.
- Use pattern references only after candidate freeze and only for structural stress testing; never use them as evidence, candidate generators, or novelty sources.
- Keep interface validity, optimization-path validity, empirical optimization health, mechanism efficacy, and downstream performance separate.
- Do not infer task benefit from reconstruction, invertibility, stability, legality, expressivity, or information preservation alone.

## Entry Modes and Progressive Execution

Select one entry mode:

- `GENERATE`: build from the earliest unsupported stage and advance phase by phase.
- `AUDIT`: preserve the supplied subject and causal chain unless evidence contradicts them.
- `REPAIR`: resume at the earliest failed gate and invalidate dependent downstream work.
- `COMPARE`: audit supplied candidates independently under matched constraints before selection.

Use these phases:

```text
DIAGNOSIS = Sections 0–6
INDEPENDENT-IDEATION = Section 7
AUDIT = Sections 8–13
COMPILATION = Sections 14–16
```

Stages are numbered 0–12 and dossier sections are numbered 0–16; the two numberings are offset, and gates align with stages rather than sections. The offset is: Stage 8 Novelty writes Section 10, Stage 11 Falsification writes Section 13, and Stage 12 compiles Sections 14–16. Treat a stage number and a section number as different coordinate systems, and never renumber either.

Leave unentered sections `NOT-STARTED`. Use `BLOCKED` only for a named dependency that prevents work. Enter `COMPILATION` as soon as current evidence supports an early `NEED-EVIDENCE` or `PIVOT`; leave unevaluated downstream gates deferred. Set `current_phase: COMPLETE` once exactly one decision is compiled and no stage remains open.

## Stage Controller

### Stages 0–1 — Boundary and Need

1. Record the entry mode, task, data regime, measurable target, constraints, evidence cutoff, supplied evidence, scope exclusions, and the `dossier_schema_version` this dossier conforms to.
2. Read `references/personal-research-priors.md`; apply only confirmed, evidence-compatible preferences.
3. State the need without a preferred method name:

```text
Need = task objective + operating regime + current limitation + measurable consequence
```

Set G0 and G1 only when the research boundary and solution-independent need are explicit.

### Stages 2–4 — Diagnose Before Designing

Read `references/problem-diagnosis.md` and use it to:

- localize an observable failure with a direct diagnostic;
- build independently testable causal links and at least two rivals;
- derive a measurable invariant whose task connection is evidenced or explicitly justified.

Do not design a repair while G2, G3, or G4 is unresolved in `GENERATE`. Preserve an auditable supplied candidate in `AUDIT`, but do not turn unresolved diagnosis into a positive mechanism conclusion.

### Stage 5 — Freeze Candidates, Then Inspect Patterns

Derive candidates before reading any pattern source.

- In `GENERATE`, keep at most three candidates: one minimal in-domain correction, one simple or null baseline, and at most one cross-domain candidate with a source-independent causal or mathematical correspondence.
- In `COMPARE`, retain up to three supplied candidates and treat any additional fair comparator as an experiment baseline.
- In `AUDIT` or `REPAIR`, retain the supplied candidate and add only the attribution baseline or alternative required to test necessity.
- Record the candidate set, roles, causal basis, invariant, predictions, and freeze basis before consulting references.

After freeze, load only the matching branches:

1. Read `references/iclr-pattern-index.md`. Route each research candidate to one primary card. Load one supporting card only when the core operation necessarily changes a second research axis. Check at most one reasoned substitute after a mismatch.
2. Read `references/personal-pattern-index.md`. Load at most one matching personal card per candidate; load none when only terminology or module shape matches.
3. Read `references/mechanism-transfer.md` only for a cross-domain candidate or an explicit transfer audit.

Use `NO-STRUCTURAL-MATCH` without penalty when no catalogued pattern fits. Do not pattern-shop, add a post-search candidate, or promote a simple baseline into a contribution without re-freezing.

Set G5 only when candidate roles, freeze discipline, fair attribution, required transfer mappings, and the Reference-Use Log are complete.

### Stages 6–7 — Direct Use and Minimal Adaptation

For every non-null candidate:

1. Check assumptions, information access, causality, sampling, non-stationarity, learnability, interfaces, optimization path, and target-regime constraints.
2. Record one disposition for every finding: adapt, bound the claim, reject, or justify `NO-ADAPTATION-REQUIRED`.
3. Add a component only to repair a supported failure or broken assumption.
4. Define every adapted `SYS-*` and `COMP-*` with end-to-end training and inference contracts, risk, mitigation, and ablation.

Do not invent a direct-use failure to justify complexity. Return to Stage 5 if adaptation changes the core mechanism; return earlier if it changes the diagnosis or invariant.

### Stage 8 — Novelty

Read `references/novelty-audit.md`. Freeze the actual novelty subject and every advertised CORE contribution before searching. Compare primary-source neighbors across same problem, mechanism, axis, combination, and negative or boundary roles as applicable.

Assign exactly one non-numeric novelty status per candidate using the canonical template. A final `GO` requires `PASS`; unresolved search or overlap cannot be rounded up.

### Stage 9 — Feasibility

Read `references/feasibility-audit.md`. Audit the actual trainable `CAND-*` or `SYS-*`, not a method family. Close the nine Section-11 aspect rows in `assets/idea-dossier-template.md` — responsibility boundary, end-to-end data flow, input/output and state, tensor shapes and mathematical operations, training signal and gradient/estimator path, constraint enforcement, numerical and optimization dynamics, training/inference consistency, and compute, memory, and data — plus the intermediate and invariant observability requirement in `references/feasibility-audit.md`. The template is the authority for the row list; do not add, merge, or rename a row.

Keep long-run optimization health and mechanism efficacy for Stage 11. Use G9 only for structural executability and testability.

### Stage 10 — Theory

Read `references/theory-audit.md`. Audit every decisive theory-relevant `CLM-*` separately. Keep theory maturity independent of assumption applicability, state guarantees with non-guarantees, and require an observable or formal counterpart.

Use `NO-FORMAL-THEOREM-CLAIMED` only when no contribution depends on a formal guarantee; it does not waive a consistency argument for the CORE mechanism.

### Stage 11 — Falsification

Map every CORE claim to a plausible falsifier in Section 13. Include, as applicable:

- the original failure diagnostic;
- a mechanism-versus-rival intervention;
- invariant measurement separate from task performance;
- direct-versus-adapted comparison;
- component ablations, boundary tests, stability, and cost;
- the fairest simple baseline and what a null result cannot prove.

Preserve diagnostic `EXP-*` IDs created earlier. Complete results and source references only for experiments that actually ran.

Falsification coverage is a gate, not a formality. When Section 13 reports `coverage_complete: NO`, G11 is `EVALUATED` and `UNRESOLVED` — never satisfied — so the decision is capped at `NEED-EVIDENCE` until every CORE claim carries a falsifier or an explicit `N/A — <reason>`. An uncovered CORE claim must appear in `uncovered_core_claim_ids` and be named as the smallest next action; it is not a satisfactory state to publish or build on.

### Stage 12 — Compile One Decision

Re-read `references/personal-research-priors.md`, derive Sections 14–16 only from existing IDs, and select exactly one decision. Apply the canonical gate semantics:

| Gate result | Decision route |
|---|---|
| Every gate evaluated and satisfied; novelty `PASS` | Eligible for `GO` |
| Decision-relevant gate unresolved; no gate unsatisfied | `NEED-EVIDENCE` |
| At least one unsatisfied, repairable gate | `PIVOT` |
| A decisive contradicted gate has no substantive repair | `KILL` |

Do not average gates. Name the decision subject, decisive ledger rows, highest-risk assumption, and smallest next action. Require `decision_consistency_check: PASS`.

## Reference Router

Load only what the current stage requires:

| Stage or branch | Reference |
|---|---|
| Stage 0, Stage 8, and the final decision | `references/personal-research-priors.md` |
| Stages 2–4 | `references/problem-diagnosis.md` |
| Stage 5 structural routing | `references/iclr-pattern-index.md` |
| Stage 5 personal precedent routing | `references/personal-pattern-index.md` |
| Stage 5–7 cross-domain branch | `references/mechanism-transfer.md` |
| Stage 8 | `references/novelty-audit.md` |
| Stage 9 | `references/feasibility-audit.md` |
| Stage 10 | `references/theory-audit.md` |
| Final output or field lookup | `assets/idea-dossier-template.md` |

The ICLR index may route to at most two of these directly linked cards per research candidate:

- `references/iclr-pattern-a-mechanism.md`
- `references/iclr-pattern-b-modeled-object.md`
- `references/iclr-pattern-c-granularity.md`
- `references/iclr-pattern-d-responsibility.md`
- `references/iclr-pattern-e-information-flow.md`
- `references/iclr-pattern-f-invariant.md`
- `references/iclr-pattern-g-objective-computation.md`
- `references/iclr-pattern-h-operational-framework.md`

The personal index may route to at most one card per research candidate, selected from the route map in `references/personal-pattern-index.md`. The configured card set belongs to the active profile layer: the shipped default profile provides `personal-pattern-card-a.md`, `personal-pattern-card-b.md`, and `personal-pattern-card-c.md` under `references/`, and another profile may configure a different set with the same slot prefix. An index whose route map matches nothing is a valid state; record that personal patterns were not consulted and continue.

Do not load all references or all cards at startup. If a required file is unavailable, record the missing dependency and do not invent its contents.

## Output Contract

Produce exactly one unified Idea Dossier from `assets/idea-dossier-template.md`.

- Preserve Sections 0–16 and their order.
- Emit full bodies only for `ACTIVE` or `COMPLETE` sections.
- Keep plans separate from results and cite literature claims.
- Preserve per-candidate rows, rejected candidates, uncertainty, and provenance.
- Stop after the dossier without code, polished paper prose, or final figures.

## Global Anti-Patterns

- Do not start from a fashionable module and invent a problem around it.
- Do not treat an observation, correlation, visualization, or benchmark gain as its own causal explanation.
- Do not transfer by method name, metaphor, diagram shape, or venue prestige.
- Do not use familiar patterns, first application, or bounded search absence as novelty evidence.
- Do not add components without an identified repair responsibility and ablation.
- Do not let successful execution substitute for healthy optimization or mechanism support.
- Do not copy a theorem across a changed operator or unsupported assumptions.
- Do not hide negative results, unresolved gates, or rejected candidates.
- Do not emit numeric novelty or aggregate gate scores.
