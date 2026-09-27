# ICLR-Informed Research Pattern Index

Use this index only after freezing the target-derived candidate set at Stage 5. Route a frozen research candidate to one primary structural card and, only when necessary, one supporting card. Do not use the index to generate candidates, predict venue acceptance, establish novelty, or select modules.

The patterns are internal research heuristics aligned with the ICLR reviewer emphasis on specific problems, motivated approaches, supported claims, and significant knowledge. They are not official pattern definitions, acceptance rules, or a venue-success predictor.

The boundary was reviewed on `2026-08-17` against the [ICLR 2026 Reviewer Guide](https://iclr.cc/Conferences/2026/ReviewerGuide). Re-check current official guidance separately for submission-specific work.

## Contents

1. Entry Contract
2. Candidate Fingerprint
3. Routing Table
4. Bounded Loading Protocol
5. Common Three-Principle Audit
6. Composition Rule
7. Dossier Compilation
8. Pattern Card Manifest

## 1. Entry Contract

Before routing, require:

- a solution-independent `NEED-*`;
- a localized `FAIL-*` and adjacent `LINK-*` records;
- at least two rivals with discriminating predictions;
- a measurable `INV-*`;
- a frozen research candidate with a core operation and candidate-specific prediction;
- a fair simple or null attribution baseline; and
- a recorded pre-pattern freeze basis in Section 7.2.

Return to the earliest missing stage instead of using a pattern to fill a gap.

Do not route `SIMPLE-BASELINE` or `NULL-BASELINE` candidates. They are experimental contrasts, not contribution shapes.

## 2. Candidate Fingerprint

Compile this internal routing record without architecture-family or paper names:

```text
Candidate ID:
Target FAIL-* and addressed LINK-*:
Preserved INV-*:
Core operation:
Primary changed axis:
New prediction CLM-*:
Fair attribution contrast:
```

Choose exactly one primary axis:

```text
MECHANISM | MODELED-OBJECT | REPRESENTATION | GRANULARITY
| RESPONSIBILITY | INFORMATION-FLOW | CONSTRAINT | OBJECTIVE
| COMPUTATION | OPTIMIZATION | THEORETICAL-PROPERTY
| MEASUREMENT-FRAMEWORK | OTHER
```

Use `OTHER` when the candidate is coherent but no listed axis fits. Do not distort the candidate to obtain a catalog match.

## 3. Routing Table

| Candidate structure | Primary card | Do not route when |
|---|---|---|
| Several failures may share one measurable intermediate cause | `iclr-pattern-a-mechanism.md` | The candidate only renames or groups symptoms |
| The current semantic unit hides the entity required by the task | `iclr-pattern-b-modeled-object.md` | The change only reshapes a tensor or adds an embedding |
| A coarse choice changes several responsibilities at once | `iclr-pattern-c-granularity.md` | More options are added without preserving interfaces |
| Responsibilities are conflicting, duplicated, missing, or untestable | `iclr-pattern-d-responsibility.md` | Separation is only architectural tidiness |
| Required information or computation follows the wrong path, direction, or time | `iclr-pattern-e-information-flow.md` | A new edge only adds capacity or shortens gradients |
| A useful change damages a separately measurable property | `iclr-pattern-f-invariant.md` | The alleged invariant is downstream performance itself |
| An objective, estimator, or repeated computation targets the wrong unit or scale | `iclr-pattern-g-objective-computation.md` | The change is routine code optimization with the same estimand |
| A coarse proxy cannot express a needed comparison or boundary | `iclr-pattern-h-operational-framework.md` | A new metric or theorem changes no scientific conclusion |

## 4. Bounded Loading Protocol

For each `PRIMARY` or `MINIMAL` candidate:

1. Route from the fingerprint to one primary card.
2. Load and test that card's structural contract.
3. If it mismatches, check at most one reasoned substitute selected from the diagnosed failure or changed axis.
4. If a card matches, load one supporting card only when the core operation necessarily changes a second axis and the interaction has its own prediction.
5. Stop after at most two loaded cards per candidate.
6. Record one concrete mismatch, unsupported assumption, or transfer risk even for a useful match.

Use exactly one internal result:

```text
MATCHED | NO-STRUCTURAL-MATCH
```

Use `NO-STRUCTURAL-MATCH` when neither the primary nor the one justified substitute satisfies the causal structure. Catalog absence is not evidence for or against the candidate. Continue with the common audit below without loading more cards.

## 5. Common Three-Principle Audit

Apply this audit after bounded routing. Do not let strength on one axis compensate for failure on another.

### Logic

- Verify that the core operation acts on the named causal link rather than only the task metric.
- Preserve the invariant and name what remains unexplained.
- Require a candidate-specific prediction that differs from a rival.

### Contribution shape

- State the inherited object, mechanism, responsibility, or process.
- State the smallest positive technical delta and one primary changed axis.
- Connect the delta to the solution-independent need and a distinguishing consequence.
- Bound cosmetic substitutions before literature search; assign no novelty status here.

### Early implementability

- Close the core input, output, state, information-access, and update path in principle.
- Name an observable intermediate, minimum decisive contrast, and fallback that preserves the claim.
- Defer exact shapes, full resource measurement, optimization health, and G9 to Stage 9 unless the core operation is already contradictory.

## 6. Composition Rule

Keep one primary pattern. Add one supporting pattern only when:

- the primary operation cannot be instantiated without the second structural move;
- the second move has a distinct responsibility;
- the interaction yields a testable prediction; and
- individual and joint ablations can distinguish their effects.

Treat three or more primary-looking moves as a system-bundle warning. Return to Stage 5 when pattern inspection changes candidate identity, causal links, the invariant, or the CORE prediction.

## 7. Dossier Compilation

Compile pattern use into existing fields only:

- update candidate-level `CLM-*` rows when inspection exposes a real assumption or bounded prediction;
- keep the Section 7 candidate row focused on core operation, addressed links, invariant, and prediction IDs;
- write the consulted card IDs and at least one mismatch or risk in Section 7.2;
- reserve an `EXP-*` only for a new decisive contrast;
- set the Reference-Use effect to exactly `retained`, `bounded`, or `rejected`.

For `NO-STRUCTURAL-MATCH`, use effect `retained` unless the separate three-principle audit establishes an actual defect. Return control to the Stage-5 controller; do not assign novelty, feasibility, theory, or final-decision status here.

## 8. Pattern Card Manifest

- `references/iclr-pattern-a-mechanism.md`
- `references/iclr-pattern-b-modeled-object.md`
- `references/iclr-pattern-c-granularity.md`
- `references/iclr-pattern-d-responsibility.md`
- `references/iclr-pattern-e-information-flow.md`
- `references/iclr-pattern-f-invariant.md`
- `references/iclr-pattern-g-objective-computation.md`
- `references/iclr-pattern-h-operational-framework.md`

Do not load the manifest as a batch.
