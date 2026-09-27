# Idea Dossier Schema

Normative reference for the Idea Dossier format produced by
`skills/time-series-model-ideation/`.

This document restates the contract defined by
`skills/time-series-model-ideation/assets/idea-dossier-template.md`. It does not extend
it. `SKILL.md` states the authority rule directly:

> Use `assets/idea-dossier-template.md` as the sole authority for output headings,
> fields, enums, ID namespaces, lifecycle values, and field order.
> — `skills/time-series-model-ideation/SKILL.md` line 31

Where this document quotes the template, the template's wording is authoritative. Where
the template is silent or ambiguous, the gap is recorded under
[Unspecified in the template](#unspecified-in-the-template) instead of being filled with
an invented rule. Nothing outside those two files is a rule.

## Authority map

| Artifact | Authority over |
|---|---|
| `skills/time-series-model-ideation/assets/idea-dossier-template.md` | Sections and their order, field names, enums, ID namespaces, lifecycle values, decision consistency rules |
| `skills/time-series-model-ideation/SKILL.md` | Stage controller, entry modes, phase list, reference router, canonical gate-result-to-decision table, anti-patterns |
| `skills/time-series-model-ideation/references/*.md` | Stage-level protocols (diagnosis, transfer, novelty, feasibility, theory) that compile into the template's existing fields only |
| `CONTRIBUTING.md` | Change process for this schema and the eval-expectation requirement |
| `CHANGELOG.md` | Schema versioning and migration notes |

`CONTRIBUTING.md` freezes this contract:

> The dossier schema is frozen except by explicit migration. Section count, section
> order, ID namespaces, enum values, and gate semantics are a public contract.
> — `CONTRIBUTING.md` lines 21–23

## 1. Section lifecycle

Every section carries `section_status` and `status_reason`. The four lifecycle values and
their emission obligations, quoted from the template header (lines 9–13):

| Value | What the writer must emit |
|---|---|
| `ACTIVE` | The lifecycle block and the full section body; replace every `{{REQUIRED: ...}}` placeholder and leave no blank cells |
| `COMPLETE` | Same emission obligations as `ACTIVE` |
| `NOT-STARTED` | Only the heading and the lifecycle block; do not instantiate the remaining fields or tables for that section |
| `BLOCKED` | Only the heading and the lifecycle block; `status_reason` names the dependency that prevents completion |

Rules:

- `NOT-STARTED` "records workflow progress, not missing evidence"; `BLOCKED` "names a
  dependency that prevents the section from being completed" (`idea-dossier-template.md` lines 12–13).
  `SKILL.md` line 76 adds: "Use `BLOCKED` only for a named dependency that prevents
  work."
- Missing decision-relevant evidence belongs inside an **active** section as an
  `UNRESOLVED` claim with `E0`. It must not be hidden with `N/A` or `NOT-STARTED`
  (`idea-dossier-template.md` line 13; `SKILL.md` line 47).
- Two sentinel forms replace values: `N/A — <reason>` for a structurally inapplicable
  field, and `PENDING — <reason>` for a planned result that does not exist yet, which
  "is not evidence" (`idea-dossier-template.md` line 28). Add YAML quotes only when YAML syntax requires
  them; do not include literal quote characters inside Markdown-table values (template
  line 25).
- Section 0 restricts its own enum to `ACTIVE | COMPLETE` (`idea-dossier-template.md` line 38). Sections
  1–16 accept all four lifecycle values.
- `SKILL.md` restates the emission rule as an output contract: "Emit full bodies only
  for `ACTIVE` or `COMPLETE` sections" (`SKILL.md` line 214).
- Work is updated in one dossier in place: "Update one dossier in place; do not create
  stage-specific reports or new output sections" (`SKILL.md` line 31); "do not emit a
  separate partial dossier" (`references/problem-diagnosis.md` line 23).

### 1.1 Section 0 control fields

Section 0 is the control block (`idea-dossier-template.md` lines 38–49):

| Field | Allowed value |
|---|---|
| `section_status` | `ACTIVE | COMPLETE` — Section 0 is never `NOT-STARTED` or `BLOCKED` |
| `status_reason` | Why this section has this status |
| `dossier_id` | `DOS-*` |
| `dossier_schema_version` | "schema version this dossier conforms to, e.g. 1.1.0" |
| `date` | `YYYY-MM-DD` |
| `evidence_cutoff` | `YYYY-MM-DD` |
| `entry_mode` | `GENERATE | AUDIT | REPAIR | COMPARE` |
| `current_phase` | `DIAGNOSIS | INDEPENDENT-IDEATION | AUDIT | COMPILATION | COMPLETE` |
| `task` | Time-series task |
| `data_regime` | Data, sampling, horizon, and deployment regime |
| `evaluation_target` | Measurable research target |
| `scope_exclusions` | Excluded downstream or scientific work |

`dossier_schema_version` is required and is recorded at Stage 0: "Record the entry mode,
task, data regime, measurable target, constraints, evidence cutoff, supplied evidence,
scope exclusions, and the `dossier_schema_version` this dossier conforms to"
(`SKILL.md` line 82).

### 1.2 Schema version and migration

The template carries its own version and the rule for a dossier written before the field
existed:

> Dossier schema version: 1.1.0. Record it in Section 0 as `dossier_schema_version`. See
> CHANGELOG.md for the migration note between schema versions; a dossier without the
> field is implicitly 1.0.0.
> — `idea-dossier-template.md` lines 3–4

The migration table is in `CHANGELOG.md` (lines 18–21):

| Schema | Change | Migration |
|---|---|---|
| 1.0.0 | Original contract; dossiers written before the version field existed are implicitly 1.0.0 | None |
| 1.1.0 | Section 0 gains the required `dossier_schema_version` field; `coverage_complete: NO` in Section 13 makes G11 `EVALUATED` and `UNRESOLVED`, capping the decision at `NEED-EVIDENCE` | Add `dossier_schema_version: "1.0.0"` to an old dossier, or regenerate it. No section was renumbered and no ID namespace or enum value changed |

Two version numbers move independently: the project version (`0.x.y`) and the dossier
schema version, which is "the field/enum/gate contract of
`skills/time-series-model-ideation/assets/idea-dossier-template.md`" (`CHANGELOG.md` lines
11–14). The repository process for a future schema change is fixed: "A schema change
requires: updating `assets/idea-dossier-template.md`, adding a `CHANGELOG.md` entry with a
migration note under a new schema version, and updating `docs/schema.md`. Never renumber
an existing section to make room." (`CONTRIBUTING.md` lines 21–26)

## 2. Phase map

The template defines the phases over **section ranges** (`idea-dossier-template.md` lines 15–19);
`SKILL.md` repeats the same ranges (`SKILL.md` lines 67–72):

| Phase | Sections | Template rule | Stages writing them | Gates set |
|---|---|---|---|---|
| `DIAGNOSIS` | 0–6 | — | Stages 0–4 | G0–G4 |
| `INDEPENDENT-IDEATION` | 7 | "freeze candidates before consulting pattern or method references" | Stage 5 | G5 |
| `AUDIT` | 8–13 | — | Stages 6–11 | G6–G11 |
| `COMPILATION` | 14–16 | "derive them from existing IDs and results" | Stage 12 | none |

The stage and gate columns above align `SKILL.md`'s stage headings and gate names with
the template's section ranges. `SKILL.md` states the two coordinate systems explicitly:

> Stages are numbered 0–12 and dossier sections are numbered 0–16; the two numberings are
> offset, and gates align with stages rather than sections. The offset is: Stage 8 Novelty
> writes Section 10, Stage 11 Falsification writes Section 13, and Stage 12 compiles
> Sections 14–16. Treat a stage number and a section number as different coordinate
> systems, and never renumber either.
> — `SKILL.md` line 74

The alignment is not one-to-one for two sections: Stage 0 writes Sections 0 and 1, Stage 2
writes the claim ledger (Section 3) and the failure record (Section 4), and diagnostic
`EXP-*` rows are created in Section 13 during Stages 2–4
(`references/problem-diagnosis.md` lines 41–46, 206–210). This offset was previously
unstated; [Known inconsistencies](#known-inconsistencies) item 1 records the repair.

Progressive execution rules:

- "Leave unentered sections `NOT-STARTED`" and "Enter `COMPILATION` as soon as current
  evidence supports an early `NEED-EVIDENCE` or `PIVOT`; leave unevaluated downstream
  gates deferred" (`SKILL.md` line 76).
- `current_phase` allowed values are
  `DIAGNOSIS | INDEPENDENT-IDEATION | AUDIT | COMPILATION | COMPLETE` (`idea-dossier-template.md` line 45).
  Set `COMPLETE` only "once exactly one decision is compiled and no stage remains open"
  (`SKILL.md` line 76).
- Sections 14, 15, and 16 carry `compilation_mode: "DERIVED-ONLY"` (`idea-dossier-template.md` lines 394,
  411, 444) and must not introduce claims absent from Sections 2–13 (`idea-dossier-template.md` line 32).

## 3. Entry modes

`entry_mode` is a Section 0 field with exactly four values:
`GENERATE | AUDIT | REPAIR | COMPARE` (`idea-dossier-template.md` line 44).

| Mode | `SKILL.md` rule (lines 60–63) | Template rule (lines 22–25) |
|---|---|---|
| `GENERATE` | "build from the earliest unsupported stage and advance phase by phase" | "advance phase by phase; leave later sections NOT-STARTED until their dependencies are satisfied" |
| `AUDIT` | "preserve the supplied subject and causal chain unless evidence contradicts them" | "preserve the supplied candidate and causal chain; do not silently regenerate them" |
| `REPAIR` | "resume at the earliest failed gate and invalidate dependent downstream work" | "resume at the earliest failed gate, mark invalidated downstream sections NOT-STARTED, and recompute them" |
| `COMPARE` | "audit supplied candidates independently under matched constraints before selection" | "keep candidates SHORTLISTED or PROVISIONALLY-SELECTED until all compared candidates receive a fair audit" |

Mode-specific behavioral rules stated in the sources:

- **`GENERATE`** — keep at most three candidates: "one minimal in-domain correction, one
  simple or null baseline, and at most one cross-domain candidate with a
  source-independent causal or mathematical correspondence" (`SKILL.md` line 106). Do
  not design a repair while G2, G3, or G4 is unresolved (`SKILL.md` line 100). Require
  G2–G4 `SATISFIED` before designing a transfer-based architecture
  (`references/mechanism-transfer.md` line 67). Do not use novelty-search findings to
  silently redesign the subject (`references/novelty-audit.md` line 92).
- **`AUDIT`** — retain the supplied candidate and "add only the attribution baseline or
  alternative required to test necessity" (`SKILL.md` line 108). Preserve the supplied
  candidate even when G2–G4 are unresolved, so its mapping can be audited
  (`references/mechanism-transfer.md` line 77), but do not turn unresolved diagnosis
  into a positive mechanism conclusion (`SKILL.md` line 100).
- **`REPAIR`** — dependent downstream work is invalidated, not carried forward.
  Preserve old claims, comparisons, and candidate IDs when recording a pivot; "do not
  rewrite audit history" (`references/novelty-audit.md` line 409). Exit the transfer
  protocol back to Stages 3–4 if the repair requires changing a causal `LINK-*` or
  `INV-*` (`references/mechanism-transfer.md` line 85), and re-freeze the novelty
  subject before re-auditing (`references/novelty-audit.md` line 95).
- **`COMPARE`** — "retain up to three supplied candidates and treat any additional fair
  comparator as an experiment baseline" (`SKILL.md` line 107); the template places that
  extra comparator in Section 13 rather than adding a fourth candidate (`idea-dossier-template.md` line
  189). "Keep candidate and system IDs explicit in `COMPARE`; never average
  heterogeneous subjects" (`SKILL.md` line 50). Keep the same evidence cutoff, search
  protocol, inclusion rules, and stopping condition across compared subjects
  (`references/novelty-audit.md` line 94); keep separate claim rows and statuses for
  every candidate (`references/novelty-audit.md` line 418); produce one overall G10
  result per final subject (`references/theory-audit.md` line 23).

## 4. ID namespaces

The namespace list is closed (`idea-dossier-template.md` lines 29–31):

> Use only these ID namespaces: DOS-\*, NEED-\*, CLM-\*, FAIL-\*, LINK-\*, RIV-\*,
> INV-\*, CAND-\*, FIND-\*, SYS-\*, COMP-\*, EXP-\*.
> Keep CLM-\* IDs claim-only. Link all other entities through related_claim_ids or
> explicit ID columns.

| Prefix | Entity | Holds | May not hold |
|---|---|---|---|
| `DOS-*` | Dossier | Dossier identity (`dossier_id`, `idea-dossier-template.md` line 40) and the Section 16 decision subject | Claims or evidence |
| `NEED-*` | Need | Task objective, operating regime, current limitation, measurable consequence, solution-independent need (Section 2) | A preferred method name (`method_names_removed_check` must be `PASS`, `idea-dossier-template.md` line 82) |
| `CLM-*` | Claim | Every observation, explanation, mechanism, hypothesis, assumption, and evidence statement, with type, centrality, provenance, evidence strength, and status (Section 3) | Any non-claim entity; the ledger is claim-only |
| `FAIL-*` | Observable failure | One localized failure record with symptom, condition, diagnostic measurement, and effects (Section 4) | A causal explanation (`observable_symptom` is recorded "without a causal explanation", `idea-dossier-template.md` line 133) |
| `LINK-*` | Causal link | One adjacent causal relation between two claims (Section 5.1) | Non-claim endpoints; `From claim ID` and `To claim ID` take only `CLM-*` IDs (`references/problem-diagnosis.md` line 142) |
| `RIV-*` | Rival explanation | A competing explanation with shared and discriminating predictions linked to an `EXP-*` (Section 5.2) | Rivals without a distinct prediction (`references/problem-diagnosis.md` line 173) |
| `INV-*` | Preserved invariant | Property, preservation type, measurement, tolerance, task relevance, harmful conditions (Section 6) | Downstream performance itself as the invariant (`references/problem-diagnosis.md` line 187) |
| `CAND-*` | Candidate mechanism | Candidate identity, source, mechanism class, evaluation role, core operation, addressed links, preserved invariants, new predictions, status (Section 7) | Post-freeze additions without an explicit re-freeze (`SKILL.md` line 117) |
| `FIND-*` | Direct-use finding | One finding with type, evidence claims, disposition, and consequence (Section 8) | A component; findings do not create components by themselves |
| `SYS-*` | Adapted system | Base candidate, components, input/output contracts, connections, training and inference paths, state and constraints (Section 9.2) | A system with no adaptation basis; `NO-ADAPTATION-REQUIRED` candidates create no `SYS-*` (`references/mechanism-transfer.md` line 259) |
| `COMP-*` | Component contract | Repaired `FIND-*` IDs, primary responsibility, secondary effects, existence reason, operation, contract, risk, mitigation, ablation experiments (Section 9.3) | A component without an `ADAPT` finding, responsibility, and ablation (`references/mechanism-transfer.md` line 326) |
| `EXP-*` | Experiment | Assessment subject, claims, test, status, expected and falsifying results, observed result, sources, rivals, ablation, baseline, limits, decision change (Section 13) | Supporting evidence while `PLANNED` or `RUNNING` (`idea-dossier-template.md` line 372) |

Further namespace rules:

- **`CLM-*` is claim-only.** Other entities reach claims through `related_claim_ids`
  fields (Sections 2, 4, 6, 9.2) or explicit ID columns (`Addressed LINK-* IDs`,
  `Preserved INV-* IDs`, `New prediction CLM-* IDs`, `Evidence claim IDs`,
  `Repaired FIND-* IDs`, `Ablation EXP-* IDs`).
- **No new ID types.** Stage protocols update the template's existing fields only:
  "do not add fields, enums, or ID types to the dossier"
  (`references/problem-diagnosis.md` line 48); the same rule is repeated for transfer
  audits (`references/mechanism-transfer.md` line 224) and novelty audits
  (`references/novelty-audit.md` lines 116–125).
- **Stable IDs.** "Use stable IDs throughout; never renumber an ID after another record
  refers to it" (`idea-dossier-template.md` line 31). Preserve supplied evidence, rejected candidates,
  null results, and stable IDs (`SKILL.md` line 48). Preserve diagnostic `EXP-*` IDs
  created during Stages 2–4 when Stage 11 extends the matrix (`idea-dossier-template.md` line 361;
  `SKILL.md` line 161); extend an existing experiment when the intervention and claims
  match, and create a new ID only when the intervention, decisive contrast, or claim
  coverage materially differs (`references/problem-diagnosis.md` lines 208–209).
- **Gates are not an ID namespace.** Gate rows are literal labels `G0`–`G11`, written in
  the first column of the Section 15 table (`idea-dossier-template.md` lines 433–444). No `GATE-*` prefix
  exists.
- **Claim identity.** Keep the contribution claim ID distinct from every distinguishing
  consequence claim ID (`idea-dossier-template.md` line 292); do not use one `CLM-*` for both the
  contribution and its consequence (`references/novelty-audit.md` line 152).

## 5. Claim record (Section 3)

### 5.1 Allowed values

Quoted from `idea-dossier-template.md` lines 97–102:

```text
Claim type = OBSERVATION | EXPLANATION | MECHANISM | HYPOTHESIS | ASSUMPTION | EVIDENCE
Centrality = CORE | SUPPORTING | CONTEXT
Provenance = USER-SUPPLIED | DIRECT-MEASUREMENT | PRIMARY-LITERATURE | INFERENCE | NONE
Evidence strength = E0 | E1 | E2 | E3 | E4 | E5
Status = SUPPORTED | CONTRADICTED | UNRESOLVED | NOT-APPLICABLE
```

The template enumerates the six claim types without prose definitions. Operational
guidance appears in the references and is quoted here with its source rather than
restated as schema:

- the ledger must "separate observations, explanations, mechanisms, hypotheses,
  assumptions, and evidence" (`SKILL.md` line 45);
- a contribution claim "is normally a `MECHANISM` or `EXPLANATION`" and "a predicted
  empirical consequence is normally a `HYPOTHESIS`"
  (`references/novelty-audit.md` line 151);
- material data, operator, representation, optimization, information-access, boundary,
  and sampling conditions are represented as `ASSUMPTION` claims
  (`references/theory-audit.md` line 56);
- every causal node is expressed as an existing `CLM-*` record
  (`references/problem-diagnosis.md` line 139).

### 5.2 Evidence levels

Quoted verbatim from `idea-dossier-template.md` lines 104–113:

```text
E0 = UNKNOWN; no relevant evidence
E1 = HYPOTHESIS; testable expectation without direct support
E2 = UNCONTROLLED; source report or uncontrolled observation
E3 = DIRECT-DIAGNOSTIC; task-specific measurement of the predicted symptom
E4 = CONTROLLED-INTERVENTION; matched comparison isolates the proposed factor
E5 = REPLICATED-ROBUST; isolated effect persists across relevant regimes
```

Rules that constrain how E-levels may be used:

- The E-level scale is **empirical evidence strength only**. "Keep theory maturity as a
  separate Section 12 axis; never use E-levels as proof status" (`idea-dossier-template.md` line 115).
  The theory axis is `T0-ASSUMED | T1-DERIVED | T2-PROVED`
  (`references/theory-audit.md` line 98).
- Missing decision-relevant evidence is recorded as an `UNRESOLVED` claim with `E0`
  (`idea-dossier-template.md` line 13; `SKILL.md` line 47).
- "Treat a planned measurement as `E1` at most unless other evidence supports the
  claim"; "Treat successful execution only as feasibility evidence"; "Upgrade a causal
  claim only with a discriminating intervention or equivalent evidence"
  (`references/problem-diagnosis.md` lines 198–200).
- Planned or running experiments do not support a claim: "Only a valid observed result
  with source references may be linked as evidence in Section 3" (`idea-dossier-template.md` line 372).
- Apply the levels "without inflation", record ambiguous and null results, and bound
  every conclusion by the evaluated regime and controls
  (`references/problem-diagnosis.md` lines 197, 201–202).
- Status values are not interchangeable: "Do not mark a technically correct mechanism
  claim `CONTRADICTED` merely because prior work already contains it. Record the
  coverage with primary-literature evidence" (`references/novelty-audit.md` line 269).

### 5.3 Ledger columns

The Section 3 table has eleven columns, in this order (`idea-dossier-template.md` line 117):

`Claim ID | Claim type | Centrality | Statement | Provenance | Source refs | Evidence strength | Supports IDs | Contradicts IDs | Status | Decision impact`

`Supports IDs` and `Contradicts IDs` accept IDs or the `N/A — <reason>` syntax.

## 6. Candidate records (Section 7)

### 6.1 Allowed values

Quoted from `idea-dossier-template.md` lines 194–197:

```text
Source = SUPPLIED | GENERATED
Mechanism class = IN-DOMAIN | CROSS-DOMAIN | BASELINE
Evaluation role = PRIMARY | MINIMAL | SIMPLE-BASELINE | NULL-BASELINE
Candidate status = ACTIVE | SHORTLISTED | PROVISIONALLY-SELECTED | SELECTED | REJECTED | UNRESOLVED
```

### 6.2 Candidate record fields

The Section 7 table columns, in order (`idea-dossier-template.md` line 202):

`Candidate ID | Source | Mechanism class | Evaluation role | Core operation | Addressed LINK-* IDs | Preserved INV-* IDs | New prediction CLM-* IDs | Candidate status`

Status semantics:

- "Use `SELECTED` only after the relevant candidates have completed Direct Use,
  Novelty, Feasibility, Theory, and Falsification audits. Use
  `PROVISIONALLY-SELECTED` when downstream audit needs a focal candidate before final
  selection." (`idea-dossier-template.md` line 200)
- In `COMPARE`, keep candidates `SHORTLISTED` or `PROVISIONALLY-SELECTED` until all
  compared candidates receive a fair audit (`idea-dossier-template.md` line 25).
- A rejected transfer candidate is marked `REJECTED`, and "do not create a Section 9
  adaptation row" for it (`references/mechanism-transfer.md` line 241).
- Badge roles are contrasts, not contribution shapes: "Do not route `SIMPLE-BASELINE`
  or `NULL-BASELINE` candidates. They are experimental contrasts, not contribution
  shapes." (`references/iclr-pattern-index.md` line 34).

### 6.3 Candidate set size

- The template comment states: "Keep 2–3 candidates. For COMPARE with three supplied
  candidates, place any extra fair baseline in Section 13 rather than adding a fourth
  candidate." (`idea-dossier-template.md` line 189)
- `GENERATE`: at most three candidates with the role composition quoted in
  [section 3](#3-entry-modes) (`SKILL.md` line 106).

### 6.4 Cross-domain transfer mapping (Section 7.1)

Columns, in order (`idea-dossier-template.md` line 209):

`Candidate ID | Source problem | Source mechanism | Causal/mathematical correspondence | Source assumptions | Time-series mapping | Broken assumptions | New prediction claim IDs`

Rule: at Stage 5, put only already-established target incompatibilities in `Broken
assumptions`; otherwise use the `PENDING — <reason>` syntax and resolve the field during
Stage 6 — "do not present a possible mismatch as an observed finding"
(`references/mechanism-transfer.md` line 108).

### 6.5 `CAND-*` freeze discipline

Section 7.2 records the freeze (`idea-dossier-template.md` lines 215–219):

```yaml
candidate_set_frozen: "{{REQUIRED: YES | NO | N/A — supplied candidate set}}"
frozen_candidate_ids: "{{REQUIRED: CAND-* IDs}}"
freeze_basis: "{{REQUIRED: problem, causal links, and invariant used before pattern or method search}}"
```

Discipline rules:

- "Derive candidates before reading any pattern source"; "Record the candidate set,
  roles, causal basis, invariant, predictions, and freeze basis before consulting
  references" (`SKILL.md` lines 104, 107).
- "Do not pattern-shop, add a post-search candidate, or promote a simple baseline into a
  contribution without re-freezing" (`SKILL.md` line 117). The same prohibition is
  repeated for cross-domain candidates (`references/mechanism-transfer.md` line 321) and
  for post-search redesign (`references/novelty-audit.md` line 92).
- Set G5 only when candidate roles, freeze discipline, fair attribution, required
  transfer mappings, and the Reference-Use Log are complete (`SKILL.md` line 119).
- Return to Stage 5 when pattern inspection changes candidate identity, causal links,
  the invariant, or the CORE prediction (`references/iclr-pattern-index.md` line 125).
- Do not confuse the two freezes: the Stage-5 candidate-set freeze covers candidate
  identities, roles, target-side mechanisms, and the attribution baseline; the
  novelty-subject freeze after Stage 7 covers the actual `CAND-*` or `SYS-*`
  implementation concept, participating `COMP-*` IDs, CORE contribution claims,
  responsibility boundaries, and distinguishing consequences
  (`references/novelty-audit.md` lines 75–88).

Reference-Use Log columns, in order (`idea-dossier-template.md` line 221):

`Reference | Consulted after freeze | Purpose | Structural mismatch or transfer risk found | Effect on candidate set`

Effect values are exactly three: `retained`, `bounded`, `rejected`
(`references/iclr-pattern-index.md` line 135). Record "at least one mismatch/risk when
consulted" (`idea-dossier-template.md` line 223); "Record one concrete mismatch, unsupported assumption,
or transfer risk even for a useful match" (`references/iclr-pattern-index.md` line 83);
for `NO-STRUCTURAL-MATCH`, use effect `retained` unless the separate three-principle
audit establishes an actual defect (`references/iclr-pattern-index.md` line 137).

## 7. Gates `G0`–`G11` and decision routing

### 7.1 Gate roster

The Section 15 table defines twelve gates. Subject names are the template's own row
labels (`idea-dossier-template.md` lines 433–444):

| Gate | Subject | Template row | Primary operational reference |
|---|---|---|---|
| `G0` | Boundary | 433 | `SKILL.md` Stages 0–1 |
| `G1` | Need | 434 | `SKILL.md` Stages 0–1 |
| `G2` | Failure | 435 | `references/problem-diagnosis.md` section 8.3 |
| `G3` | Causality | 436 | `references/problem-diagnosis.md` section 8.3 |
| `G4` | Invariant | 437 | `references/problem-diagnosis.md` section 8.3 |
| `G5` | Candidates | 438 | `SKILL.md` line 119; `references/iclr-pattern-index.md`; `references/mechanism-transfer.md` line 311 |
| `G6` | Direct Use | 439 | `SKILL.md` Stages 6–7; `references/mechanism-transfer.md` line 312 |
| `G7` | Adaptation | 440 | `SKILL.md` Stages 6–7; `references/mechanism-transfer.md` line 313 |
| `G8` | Novelty | 441 | `references/novelty-audit.md` section 12 |
| `G9` | Feasibility | 442 | `references/feasibility-audit.md` section 9 |
| `G10` | Theory | 443 | `references/theory-audit.md` section 6 |
| `G11` | Falsification | 444 | `SKILL.md` Stage 11 |

There is no `G12`: the roster ends at `G11`, and Stage 12 compiles the decision with no
gate of its own. A description that refers to gates "G0–G12" (thirteen gates) is a
refuted external claim, not a discrepancy inside the sources; see
[Known inconsistencies](#known-inconsistencies) item 2.

### 7.2 Gate fields and state values

Columns, in order (`idea-dossier-template.md` line 431):

`Gate | Evaluation status | State | Failure mode | Decisive ledger IDs | Blocking item | Earliest return stage`

Quoted from `idea-dossier-template.md` lines 424–426:

```text
Evaluation status = EVALUATED | DEFERRED
State = SATISFIED | UNRESOLVED | UNSATISFIED
Failure mode = null | REPAIRABLE | CONTRADICTED
```

Rules:

- "Use `failure_mode = null` unless `state = UNSATISFIED`." (`idea-dossier-template.md` line 429)
- "For a deferred gate, use `evaluation_status = DEFERRED`, `state = UNRESOLVED`, and
  name the earlier dependency; do not pretend the gate was evaluated." (`idea-dossier-template.md` line
  429)
- "Set the canonical failure mode only when a gate is `UNSATISFIED`"; use `REPAIRABLE`
  when the diagnosis can be materially revised without abandoning the need, and
  `CONTRADICTED` when decisive evidence refutes the claim and no substantive repair
  remains (`references/problem-diagnosis.md` lines 220–222).
- "Never mark a gate `SATISFIED` solely because a good experiment has been designed."
  (`references/problem-diagnosis.md` line 223)
- Completing a section is not gate evidence: "do not treat `section_status: COMPLETE` as
  evidence that an upstream argument holds" (`references/novelty-audit.md` line 59).

Stage-level `SATISFIED / UNRESOLVED / UNSATISFIED` criteria for G2–G4 are tabulated in
`references/problem-diagnosis.md` lines 214–218. Gate compilation procedures are stated
per gate: G8 (`references/novelty-audit.md` lines 411–416), G9
(`references/feasibility-audit.md` lines 181–189), G10
(`references/theory-audit.md` lines 134–140).

### 7.3 Canonical gate-result-to-decision routing

Quoted from `SKILL.md` lines 169–174:

| Gate result | Decision route |
|---|---|
| Every gate evaluated and satisfied; novelty `PASS` | Eligible for `GO` |
| Decision-relevant gate unresolved; no gate unsatisfied | `NEED-EVIDENCE` |
| At least one unsatisfied, repairable gate | `PIVOT` |
| A decisive contradicted gate has no substantive repair | `KILL` |

The template states the same rules as decision consistency rules (`idea-dossier-template.md` lines
471–477) and assigns each a `decision_rule_triggered` token
(`idea-dossier-template.md` line 467):

| Decision | Template consistency rule (lines 473–476) | `decision_rule_triggered` |
|---|---|---|
| `GO` | every gate is EVALUATED and SATISFIED; novelty is PASS; no unresolved, repairable, or contradicted gate exists | `ALL-SATISFIED` |
| `NEED-EVIDENCE` | at least one decision-relevant gate is UNRESOLVED, no gate is UNSATISFIED, and the smallest decisive test or search is named | `UNRESOLVED-EVIDENCE` |
| `PIVOT` | at least one gate is UNSATISFIED + REPAIRABLE and no fatal contradiction makes repair meaningless | `REPAIRABLE-FAILURE` |
| `KILL` | at least one decisive gate is UNSATISFIED + CONTRADICTED and no substantive repair remains | `FATAL-CONTRADICTION` |

Additional routing rules:

- "Do not average gates." (`SKILL.md` line 176); "do not average claims or candidates"
  (`references/novelty-audit.md` line 364); "Do not average rows" (`references/theory-audit.md`
  line 142); "Do not average candidates or gate results" (`references/mechanism-transfer.md`
  line 315).
- "Set `decision_consistency_check: PASS` only when the stated decision follows the
  matching rule and all listed gate IDs agree with Section 15." (`idea-dossier-template.md` line 477)
- A final `GO` requires novelty `PASS`: "unresolved search or overlap cannot be rounded
  up" (`SKILL.md` line 136).
- Section 16 also names the decision subject, decisive ledger IDs, highest-risk
  assumption, smallest next action, stage to revisit, reusable observations, and the
  unresolved/repairable/contradicted gate ID lists, all derived from Section 15
  (`idea-dossier-template.md` lines 454–468).
- An incomplete Section 13 coverage record forces `NEED-EVIDENCE` even when every other
  gate is satisfied; see [section 7.4](#74-falsification-coverage-caps-the-decision).

### 7.4 Falsification coverage caps the decision

Section 13's coverage block decides G11 when coverage is incomplete. The template's note
and `SKILL.md` Stage 11 state the same rule:

> `coverage_complete: NO` leaves G11 EVALUATED and UNRESOLVED — never satisfied — so the
> decision is capped at NEED-EVIDENCE, and each uncovered CORE claim must be named as the
> smallest next action.
> — `idea-dossier-template.md` lines 385–387

`SKILL.md` line 163 states the same consequence and adds that an uncovered CORE claim "is
not a satisfactory state to publish or build on". Consequences for the routing table in
[section 7.3](#73-canonical-gate-result-to-decision-routing):

- G11 is `EVALUATED` with `state = UNRESOLVED` and `failure_mode = null`.
- `GO` is impossible, because `GO` requires every gate `EVALUATED` and `SATISFIED`.
- The route is `NEED-EVIDENCE` with `decision_rule_triggered: UNRESOLVED-EVIDENCE`, unless
  another gate is `UNSATISFIED`, in which case `PIVOT` or `KILL` applies as usual.
- Every ID listed in `uncovered_core_claim_ids` must be named in Section 16's
  `smallest_next_action`.

This closes a gap formerly recorded in
[Unspecified in the template](#unspecified-in-the-template).

## 8. Novelty status (Section 10)

### 8.1 Non-numeric rule

The novelty status is an enum, never a score:

- "Assign exactly one non-numeric novelty status per candidate using the canonical
  template." (`SKILL.md` line 136)
- "Never assign a numeric novelty score." (`references/novelty-audit.md` line 392)
- "Do not emit numeric novelty or aggregate gate scores." (`SKILL.md` line 229)

Allowed values are `PASS | CONDITIONAL | FAIL | UNKNOWN` (`idea-dossier-template.md` line 300).

### 8.2 Status semantics

The template defines the enum; the operational definitions are in
`references/novelty-audit.md` section 11 (lines 366–392):

| Status | Assigned when (source wording, condensed) |
|---|---|
| `PASS` | At least one CORE contribution survives a direct closest-neighbor comparison as substantive and not bridge-evidenced obvious; no unresolved overlap could reasonably cover it; every other originally CORE claim that is covered has been explicitly downgraded; the subject and contract have been re-frozen and affected comparisons re-run; a distinct empirical or formal consequence exists; the bounded novelty claim states what is inherited, what survives, and the search boundary |
| `CONDITIONAL` | A concrete, positive, potentially substantive delta has been identified, but an equivalent combination, terminology family, claim scope, bridge rule, or overlap that could cover it remains unresolved |
| `FAIL` | Every CORE contribution is covered, is a documented standard substitution or adaptation, lacks a distinguishing consequence, or reduces to a cosmetic or implementation-only difference after fair comparison |
| `UNKNOWN` | The audit subject, CORE claims, terminology space, primary-source access, search coverage, or closest-neighbor identification is insufficient to formulate a reliable positive delta |

"Use `CONDITIONAL` only when a specific positive delta hypothesis exists. Use `UNKNOWN`
when the audit cannot yet identify such a delta reliably."
(`references/novelty-audit.md` line 392)

Gate mapping (G8): candidate `PASS` may be `SATISFIED` when the audit is complete;
`CONDITIONAL` or `UNKNOWN` leaves G8 `UNRESOLVED`; `FAIL` with a substantive repair path
is `UNSATISFIED + REPAIRABLE`; `FAIL` with no substantive repair is
`UNSATISFIED + CONTRADICTED` (`references/novelty-audit.md` lines 413–416).

### 8.3 Section 10 fields and tables

Freeze fields (`idea-dossier-template.md` lines 277–286):
`novelty_subject_frozen`, `novelty_subject_freeze_basis`,
`assessment_subject_candidate_ids`, `assessment_subject_system_ids`,
`assessment_subject_component_ids`, `declared_contribution_claim_ids`,
`current_core_contribution_claim_ids`, `search_boundary`.

Neighbor role tokens (`idea-dossier-template.md` line 289):

```text
SAME-PROBLEM | SAME-MECHANISM | SAME-AXIS | SAME-COMBINATION | NEGATIVE-OR-BOUNDARY
```

"Use one or more comma-separated neighbor-role tokens" (`idea-dossier-template.md` line 292); "One work
may serve multiple roles. Do not force one different paper per role, and do not
substitute a weak paper merely to fill a category."
(`references/novelty-audit.md` line 186)

Comparison table columns, in order (`idea-dossier-template.md` line 294): `Candidate ID | Audit subject ID
| Contribution claim ID | Affected component IDs | Neighbor role | Closest work | Modeled
object | Information flow | Responsibility boundary | Constraint or granularity |
Inherited part | Proposed difference | Why it matters | Distinguishing consequence claim
IDs | Citation`.

Status table columns, in order (`idea-dossier-template.md` line 298): `Candidate ID | Novelty status |
Surviving core contribution claim IDs | Covered or downgraded contribution claim IDs |
Unresolved contribution claim IDs | Bounded novelty claim | Unresolved overlap |
Supporting claim IDs`.

Audit subject selection: use `CAND-*` when the candidate is used directly with
`NO-ADAPTATION-REQUIRED`; use `SYS-*` when the claimed contribution depends on an
adapted system; the status stays candidate-level even when the comparison subject is a
`SYS-*` (`idea-dossier-template.md` line 292; `references/novelty-audit.md` lines 68–73).

## 9. Falsification matrix (Section 13)

### 9.1 Columns

In order (`idea-dossier-template.md` line 374): `Experiment ID | Assessment subject IDs | Claim IDs |
Test/intervention | Status | Expected result | Falsifying result | Observed result |
Result source refs | Rival explanation claim IDs | Ablation | Fairest simple baseline |
What the result cannot prove | Decision change if falsified`.

`Assessment subject IDs` accepts `NEED-*`, `FAIL-*`, `CAND-*`, or `SYS-*` IDs
(`idea-dossier-template.md` line 376) — diagnostic experiments are identified before candidates exist.

### 9.2 `EXP-*` lifecycle

Quoted from `idea-dossier-template.md` line 369:

```text
Experiment status = PLANNED | RUNNING | COMPLETED | INVALIDATED
```

- Creation: diagnostic `EXP-*` records are created in Section 13 during Stages 2–4 when
  rivals or gates require them (`references/problem-diagnosis.md` line 206).
- Stability: "Preserve diagnostic `EXP-*` IDs created earlier" (`SKILL.md` line 161);
  "do not renumber or duplicate those experiments" (`idea-dossier-template.md` line 361); "Extend an
  existing experiment when it tests the same intervention and claims. Create a new ID
  only when the intervention, decisive contrast, or claim coverage materially differs."
  (`references/problem-diagnosis.md` lines 208–209)
- Evidence boundary: "Planned or running experiments do not support a claim. Only a
  valid observed result with source references may be linked as evidence in Section 3."
  (`idea-dossier-template.md` line 372); "Complete results and source references only for experiments that
  actually ran." (`SKILL.md` line 161)
- Unrun or invalidated rows: `Observed result` uses the `PENDING — <reason>` syntax;
  `Result source refs` accepts "refs, PENDING syntax, or N/A syntax if invalidated"
  (`idea-dossier-template.md` line 376).
- Falsification content: map every CORE claim to a plausible falsifier and include, as
  applicable, the original failure diagnostic, a mechanism-versus-rival intervention,
  invariant measurement separate from task performance, direct-versus-adapted
  comparison, component ablations, boundary tests, stability, cost, the fairest simple
  baseline, and what a null result cannot prove (`SKILL.md` lines 152–159).
- Coverage fields (`idea-dossier-template.md` lines 379–382):

```yaml
core_claim_ids: "{{REQUIRED: all CORE CLM-* IDs}}"
covered_core_claim_ids: "{{REQUIRED: CORE CLM-* IDs referenced by EXP-* rows}}"
uncovered_core_claim_ids: "{{REQUIRED: IDs or N/A syntax}}"
coverage_complete: "{{REQUIRED: YES | NO; derive from the three fields above}}"
```

## 10. Compilation sections (14–16)

### 10.1 Section 14 — Compiled Research Argument

Row labels, in order (`idea-dossier-template.md` lines 401–411): Need; Observable failure; Causal
mechanism; Preserved invariant; Selected or provisional mechanism; Direct-use
assessment; Adaptation or no-adaptation result; Mechanism-level novelty; Feasibility
basis; Theory boundary; Decisive falsifier. Each row carries `Compiled statement` and
`Source IDs`.

Rule: "Compile only from existing IDs. Do not introduce new claims or stronger wording
than the cited rows support." (`idea-dossier-template.md` line 397); "Do not introduce claims in Sections
14–16 that are absent from Sections 2–13." (`idea-dossier-template.md` line 32)

### 10.2 Section 15 — Stage-Gate Summary

See [section 7.2](#72-gate-fields-and-state-values). The table has one row per gate,
`G0` through `G11`, and no other rows.

### 10.3 Section 16 — Final Decision

Fields (`idea-dossier-template.md` lines 455–468): `decision`,
`decision_subject_type` (`DOSSIER | CANDIDATE | ADAPTED-SYSTEM`), `decision_subject_id`
(`DOS-*`, `CAND-*`, or `SYS-*`), `decisive_ledger_ids` (`CLM-*`),
`highest_risk_assumption_claim_id` (`CLM-*` or N/A), `smallest_next_action`,
`stage_to_revisit`, `reusable_observation_claim_ids`, `decision_rationale`,
`unresolved_gate_ids`, `repairable_gate_ids`, `contradicted_gate_ids`,
`decision_rule_triggered`, `decision_consistency_check` (`PASS | FAIL`).

`decision` allowed values (`idea-dossier-template.md` line 455): `GO | PIVOT | NEED-EVIDENCE | KILL`.
Decision rules are quoted in [section 7.3](#73-canonical-gate-result-to-decision-routing).

## Unspecified in the template

Each item below is a gap or ambiguity in the template. No rule has been invented to fill
it; the column on the right states only what the sources do say.

| Item | What the sources do and do not say |
|---|---|
| Claim-type semantics | The template enumerates the six claim types without defining any of them; definitions would have to come from `SKILL.md` and the stage references, which give partial operational guidance (quoted in [section 5.1](#51-allowed-values)) rather than a per-type definition |
| E-level applicability to non-empirical claim types | The template says "Interpret **empirical** evidence strength as" and defines E0–E5 for empirical evidence (lines 104–113). It does not state what `Evidence strength` must contain for a purely formal, definitional, or `ASSUMPTION` row |
| `LINK-*` relation vocabulary | The `Relation` column is specified as "one adjacent causal relation" (line 154) with no closed list of relation tokens |
| Number of ledger rows | No maximum or minimum row count is stated for Section 3; the template shows one example row |
| ID numbering start | The template's examples begin at `-001` (`DOS-001`, `NEED-001`, `CLM-001`, `LINK-001`, `RIV-001`, `INV-001`, `CAND-001`, `FAIL-001`, `FIND-001`, `EXP-001`). It does not state that numbering must restart at 001 in every dossier; the shipped eval fixtures use higher numbers (`NEED-101`, `FAIL-101`, `CAND-101`, `COMP-010`) |
| Multiple dossiers in one document | `dossier_id` is a single field (line 40); the template does not say whether more than one `DOS-*` may appear in one file. `SKILL.md` requires exactly one unified dossier (line 207) |
| `decision_rule_triggered` to `decision` mapping | The template lists the four tokens (line 467) and the four decision rules (lines 473–476) but does not state the token-to-decision pairing explicitly; the pairing in [section 7.3](#73-canonical-gate-result-to-decision-routing) is by order and by rule meaning, not by a template sentence |
| Revision of a `COMPLETE` section | The template's lifecycle text does not describe how a `COMPLETE` section may later be revised; the entry-mode rules only describe marking invalidated **downstream** sections `NOT-STARTED` under `REPAIR` (line 22) |
| Section 0 and `NOT-STARTED` | Section 0's enum excludes `NOT-STARTED` and `BLOCKED` (line 38) while `SKILL.md` line 76 says to leave unentered sections `NOT-STARTED`; the template does not state the precedence rule for Section 0 |

Two entries that appeared here before the schema 1.1.0 release are now specified and have
been removed from this table: the `coverage_complete` gate consequence (now
`idea-dossier-template.md` lines 385–387 and `SKILL.md` line 163, documented in
[section 7.4](#74-falsification-coverage-caps-the-decision)) and the schema version string
(now `idea-dossier-template.md` lines 3–4, documented in
[section 1.2](#12-schema-version-and-migration)).

## Known inconsistencies

Eight entries are recorded here. Six were found while this document was written: five
were repaired upstream in favor of the template, and one was an error in an external
description of the repository rather than a discrepancy between the files. A seventh was
found in the schema 1.1.0 revision and repaired with it, and an eighth was found and
repaired in the same revision. All eight are closed against the current revision. The
repaired entries are kept with what changed, so that a reader can see they were found and
fixed rather than silently dropped. The upstream record of the repairs is `CHANGELOG.md`
lines 91–114; this section keeps the detail and the line-level evidence.

1. **Two numbering systems share the same indices — repaired.** `SKILL.md` numbers stages
   0–12 and the template numbers sections 0–16, and the two are offset, so a reader
   entering the novelty audit for "Stage 10" could write it into Section 10. `SKILL.md`
   line 74 now states both coordinate systems, the offset (Stage 8 Novelty writes Section
   10, Stage 11 Falsification writes Section 13, Stage 12 compiles Sections 14–16), and
   that gates align with stages rather than sections. Documented in
   [section 2](#2-phase-map).
2. **Gate roster: a refuted external claim.** The template defines exactly twelve gates,
   `G0`–`G11` (`idea-dossier-template.md` lines 433–444). `SKILL.md` names `G0`–`G5`
   (lines 90, 100, 119), `G9` (line 142), and the Stage 10 and Stage 11 headings; it does
   not enumerate `G6`, `G7`, or `G8` by ID, and Stage 12 has no gate. A description that
   refers to gates "G0–G12" (thirteen gates) is therefore wrong about the sources rather
   than evidence of a discrepancy inside them: no gate `G12` is defined in any file. Kept
   here as a refuted claim; see also [section 7.1](#71-gate-roster).
3. **Feasibility contract enumeration — repaired.** `SKILL.md` Stage 9 previously listed
   nine contracts ("responsibility, data-flow, interface, tensor/state, update, constraint,
   train/inference, observability, and resource") that did not match the template's nine
   Section 11 aspect rows. `SKILL.md` line 140 now names the template's rows verbatim,
   declares the template authoritative for the row list ("The template is the authority for
   the row list; do not add, merge, or rename a row"), and keeps the intermediate and
   invariant observability requirement in `references/feasibility-audit.md` line 167.
4. **`current_phase: COMPLETE` — repaired.** The template allowed a phase value that
   `SKILL.md`'s four-phase list did not define. `SKILL.md` line 76 now states when it is
   set: "Set `current_phase: COMPLETE` once exactly one decision is compiled and no stage
   remains open"; the template keeps the enum value
   (`idea-dossier-template.md` line 45).
5. **Stage-8 reading order — repaired.** `SKILL.md`'s router assigned
   `references/personal-research-priors.md` to "Stage 0 and final decision" only, while
   `references/novelty-audit.md` line 105 requires it as a Stage-8 input. The router row now
   reads "Stage 0, Stage 8, and the final decision" (`SKILL.md` line 184), matching the
   reference.
6. **G11 satisfaction vs. permitted incomplete coverage — repaired.** `SKILL.md` required
   every CORE claim to be mapped to a falsifier while the template permitted
   `coverage_complete: NO` with no stated gate consequence. The template note
   (`idea-dossier-template.md` lines 385–387) and `SKILL.md` line 163 now fix the
   consequence: G11 is `EVALUATED` and `UNRESOLVED`, the decision is capped at
   `NEED-EVIDENCE`, and each uncovered CORE claim is named as the smallest next action.
   This is the behavioral change carried by dossier schema 1.1.0
   (`CHANGELOG.md` lines 18–21 and 46–52; `references/feasibility-audit.md` and the other
   stage references were not changed by it).
7. **Profile documentation trailed the priors load points — repaired.** `SKILL.md`'s
   reference router loads `references/personal-research-priors.md` at "Stage 0, Stage 8,
   and the final decision" (`SKILL.md` line 184), and `references/novelty-audit.md` line
   105 requires it as a Stage-8 input, while the profile documentation described the slot
   as "ideation, Stage 0 and the final decision" (`PERSONALIZE.md`) and "ideation: boundary
   stage + final decision" (`profiles/README.md`). Both now match the controller:
   `PERSONALIZE.md` line 15 reads "ideation, Stage 0, Stage 8, and the final decision", and
   `profiles/README.md` line 26 reads "ideation: Stage 0 + Stage 8 + final decision".
8. **Documentation leftovers from the personal-layer removal — repaired.** Three sentences
   still described the layer that was removed before publication. `PERSONALIZE.md` said
   "The three default cards were distilled from the maintainer's own projects"; it now
   reads "The three shipped slots are empty templates; yours should come from your own
   projects" (`PERSONALIZE.md` lines 63–64). `CHANGELOG.md` listed the shipped profiles as
   `(default, minimal)`; its Added bullet now describes "a neutral shipped `default/`
   skeleton plus a git-ignored `private/` for your own stance" (`CHANGELOG.md` lines 70–72).
   `CHANGELOG.md` also claimed "Behavior under the default profile is unchanged (the index
   lists the same three cards)"; it now states that "under the shipped neutral profile the
   index configures no route rows, so a default installation records that personal patterns
   were not consulted" (`CHANGELOG.md` lines 82–88). `CONTRIBUTING.md`'s "Adding a profile"
   section no longer tells contributors to copy the removed `profiles/minimal/`: it starts
   from `profiles/default/`, explains why the card filenames are deliberately generic, and
   adds a fifth step keeping unpublished-work profiles in `profiles/private/`
   (`CONTRIBUTING.md` lines 96–107). The passages that *record* the removal —
   "`profiles/minimal/` no longer exists", "`make use-private`" (`CHANGELOG.md` lines
   36–38) — are history and are deliberately kept.

## File inventory

Every path cited in this document, with the byte size measured by `wc -c` at
2026-09-27 14:04 CST (the dossier schema 1.1.0 revision with the neutral personal layer;
see `docs/architecture.md` for the context-budget use of these numbers). The two
`personal-*.md` rows are the **shipped neutral skeleton**; a user's own profile is
arbitrary in size and lives in the git-ignored `profiles/private/`.

| Path | Bytes |
|---|---|
| `skills/time-series-model-ideation/SKILL.md` | 13860 |
| `skills/time-series-model-ideation/assets/idea-dossier-template.md` | 27571 |
| `skills/time-series-model-ideation/references/problem-diagnosis.md` | 13109 |
| `skills/time-series-model-ideation/references/mechanism-transfer.md` | 22196 |
| `skills/time-series-model-ideation/references/novelty-audit.md` | 25470 |
| `skills/time-series-model-ideation/references/feasibility-audit.md` | 10093 |
| `skills/time-series-model-ideation/references/theory-audit.md` | 8187 |
| `skills/time-series-model-ideation/references/iclr-pattern-index.md` | 7409 |
| `skills/time-series-model-ideation/references/personal-pattern-index.md` | 2063 |
| `skills/time-series-model-ideation/references/personal-research-priors.md` | 1812 |
| `CONTRIBUTING.md` | 7186 |
| `CHANGELOG.md` | 7656 |
| `PERSONALIZE.md` | 5853 |
| `profiles/README.md` | 3090 |
