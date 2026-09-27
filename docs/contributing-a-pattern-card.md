# Contributing a pattern card

A pattern card is a short structural instrument, not an essay and not a method
recommendation. Cards are consulted only after the candidate set is frozen, and they are
used to stress test a frozen candidate: to surface rivals, risks, boundary conditions,
and falsifiers.

This page covers both card families, what routing does, what disqualifies a card, the
submission checklist (including the eval-expectation rule), and a copy-paste skeleton.
Repository-level rules live in [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## 1. The eligibility rule

Cards are **stress-test instruments used after candidate freeze**. They are never
evidence, never candidate generators, and never novelty sources.

> Use pattern references only after candidate freeze and only for structural stress
> testing; never use them as evidence, candidate generators, or novelty sources.
> — `skills/time-series-model-ideation/SKILL.md` line 52

The same boundary is stated at the top of both indexes and enforced through the
Stage-5 controller:

| Rule | Source |
|---|---|
| Do not use the index to generate candidates, predict venue acceptance, establish novelty, or select modules | `references/iclr-pattern-index.md` line 3 |
| The patterns are "not official pattern definitions, acceptance rules, or a venue-success predictor" | `references/iclr-pattern-index.md` line 5 |
| Personal cards are "conditional precedents for adversarial testing, not evidence, default solutions, or candidate generators" | `references/personal-pattern-index.md` lines 5–7 |
| Use a card first to generate rivals, risks, and falsifiers; refine the mechanism only when the causal structure matches | `references/personal-pattern-index.md` lines 17–18 |
| Never cite a personal card as external evidence; cite project evidence and literature independently | `references/personal-pattern-index.md` lines 19–20 |
| Do not use the personal or ICLR pattern indexes and cards as novelty evidence; read and cite the primary record instead | `references/novelty-audit.md` line 229 |
| A card is a conditional precedent (`PERSONALIZE.md` lines 61–63), and "the routing must be able to fail. If every candidate matches a card, your index is a horoscope, not a router." (`PERSONALIZE.md` lines 69–70) | `PERSONALIZE.md` lines 61–63 and 69–70 |

Two ordering consequences follow, and both are load-bearing:

1. **Freeze first.** "Derive candidates before reading any pattern source"
   (`SKILL.md` line 104); the template's phase list says "freeze candidates before
   consulting pattern or method references" (`idea-dossier-template.md` line 17).
2. **A card may change the candidate, but only through a re-freeze.** "Do not
   pattern-shop, add a post-search candidate, or promote a simple baseline into a
   contribution without re-freezing" (`SKILL.md` line 117). If inspection changes
   candidate identity, causal links, the invariant, or the CORE prediction, return to
   Stage 5 (`references/iclr-pattern-index.md` line 125).

## 2. The two card families

| | `iclr-pattern-*` | `personal-pattern-*` |
|---|---|---|
| Nature | Public argument-structure catalogue | Profile-specific precedent: "one structural precedent from your own work" (`PERSONALIZE.md` lines 17–19); the shipped default configures none |
| Where it lives | `skills/time-series-model-ideation/references/` | A profile's slot set; the shipped default lives in `profiles/default/` |
| Index | `references/iclr-pattern-index.md` | `references/personal-pattern-index.md` |
| Index row columns | `Candidate structure \| Primary card \| Do not route when` | `Structural signature \| Card \| Exclusion` |
| Path style in its index | Bare filename, e.g. `iclr-pattern-a-mechanism.md` | Prefixed path, e.g. `references/personal-pattern-card-a.md` |
| Also listed in | The card manifest in `references/iclr-pattern-index.md` section 8 and the card list in `SKILL.md` lines 194–203 | The three fixed slot filenames (`personal-pattern-card-a.md`, `personal-pattern-card-b.md`, `personal-pattern-card-c.md`) in the profile manifest (`profiles/README.md` lines 28–30) and in `PERSONALIZE.md` lines 17–19 |
| Load cap per candidate | At most two cards: one primary, plus one supporting card only when the core operation necessarily changes a second research axis | At most one card |
| Who should add one | Anyone; this is the public catalogue | A profile author, deliberately: personal cards "belong in a profile, not in the shipped default unless you are the profile's author" (`CONTRIBUTING.md` lines 85–88). Never submit a card from an unpublished project — keep it in the git-ignored `profiles/private/` (`profiles/README.md` lines 61–63) |
| Shipped sizes | 1431–1607 bytes each (8 cards) | 1137 bytes each as shipped: three empty slots. A filled card is whatever its author writes |

Both families route only research candidates: "Do not route `SIMPLE-BASELINE` or
`NULL-BASELINE` candidates. They are experimental contrasts, not contribution shapes."
(`references/iclr-pattern-index.md` line 34)

## 3. Card anatomy

### 3.1 Personal card: six sections

All three shipped card slots — `personal-pattern-card-a.md`, `personal-pattern-card-b.md`,
and `personal-pattern-card-c.md` — use exactly these headings, in this order (headings at
lines 10, 14, 22, 26, 30, and 34 in each file). As shipped their bodies are `_(empty)_`;
the three filenames are fixed by the router and generic on purpose, because "a descriptive
name would disclose your research directions in a filename alone" (`PERSONALIZE.md` lines
82–84). The example column below quotes what each slot tells you to put there, not a
filled-in card, since the repository ships none:

| Section | Obligation | What the slot says to put there |
|---|---|---|
| `## Conditional Precedent` | One or two sentences stating the only condition under which the card may be used. This is the scope gate, not a summary. | "Replace the sections above with one card, following the anatomy used by the shipped public catalogue in `references/iclr-pattern-*.md`." (`personal-pattern-card-a.md` lines 42–43) |
| `## Structural Trace` | Five bold-labelled bullets — `Need`, `Failure`, `Suspected cause`, `Invariant`, `Mechanism` — that must line up with the frozen candidate's own `NEED-*`, `FAIL-*`, `LINK-*`, and `INV-*` records. Never define the invariant as downstream performance. | The five labels ship empty for you to fill (`personal-pattern-card-a.md` lines 16–20) |
| `## Direct-Use Risks` | The concrete checks the target regime must pass (sampling, locality, stationarity, interfaces, gradients, cost, invalid cases) and which violations may be adapted. | "The candidate claim it supports must still be evidenced independently — a matched precedent is a stress test, never support." (`personal-pattern-card-a.md` lines 45–46) |
| `## Theory Boundary` | What may be bounded or formalized under explicit assumptions, and what must not be inferred from it. | The slot requires the boundary and the non-guarantee; the anatomy is the one in `PERSONALIZE.md` lines 61–63 |
| `## Rival and Killing Test` | The rival explanations and matched comparisons that could explain the same result, plus the observations that kill or pivot the claim. | "A card that cannot name the observation that would kill it is not a card; it is a preference wearing a card's clothes." (`personal-pattern-card-a.md` lines 43–45) |
| `## Do Not Generalize To` | Explicit exclusions: the adjacent settings where this precedent is invalid. | The exclusion is also the third column of your route-map row (`personal-pattern-index.md` lines 31–36) |

### 3.2 ICLR card: five sections

All eight shipped ICLR cards use exactly these headings, in this order (headings at lines
3, 14, 22, 26, and 30 in `iclr-pattern-a` through `iclr-pattern-g`; `iclr-pattern-h`
differs by one line because its `Route When` block has four steps instead of five):

| Section | Obligation | Example |
|---|---|---|
| `## Route When` | The structural condition, followed by a short ASCII trace of the argument shape. | Pattern A: `failures F1 ... Fk -> independently measurable intermediate Z -> an intervention on Z changes the failures as predicted -> the repair targets Z rather than each surface symptom` |
| `## Structural Contract` | The properties the candidate must actually have for the card to apply, including the mismatch rule. | "Treat a new name or retrospective story without a differential prediction as a mismatch." |
| `## Minimum Contrast` | The smallest experiment that could distinguish the pattern from its rivals. | "Measure `Z` in at least two exposing conditions. Compare one targeted intervention with a matched negative control and a symptom-specific or simple repair." |
| `## Reject or Return When` | The observations that mean the diagnosis is wrong and the candidate must be revisited. | "Reject or revisit the diagnosis when `Z` is absent, the failures do not vary as predicted, ... or the repair works without affecting `Z`." |
| `## Time-Series Hazards` | The domain-specific traps for this pattern. | Pattern A: "Localize horizon, scale, variable, phase, regime, state, or optimization effects without renaming aggregate forecast error as a mechanism." |

### 3.3 What makes a card usable

- **A falsifiable scope.** `Conditional Precedent` / `Route When` must be narrow enough
  that some frozen candidates do not match. A card that matches everything fails the
  "routing must be able to fail" test (`PERSONALIZE.md` lines 69–70).
- **An exclusion.** Every route-map row needs an exclusion cell; "if you cannot state the
  exclusion, the row is a horoscope: it will 'match' everything and constrain nothing"
  (`personal-pattern-index.md` lines 34–36). The shipped skeleton has one placeholder row
  with `—` cells because it routes nothing.
- **A killing test.** Every shipped card states the observation that would reject or
  pivot the claim, not only the observation that would support it.
- **A theory boundary.** Every shipped card states what its properties do not imply;
  notably none of them licenses a task-benefit inference.
- **Brevity.** The shipped ICLR cards are 1.4–1.6 KB and the empty personal slots about
  1.1 KB. Structure, not prose, carries the content.

## 4. How routing works

### 4.1 Stage-5 entry contract (ICLR index)

Before routing, the candidate set must satisfy the index's entry contract
(`references/iclr-pattern-index.md` lines 22–32): a solution-independent `NEED-*`; a
localized `FAIL-*` with adjacent `LINK-*` records; at least two rivals with
discriminating predictions; a measurable `INV-*`; a frozen research candidate with a core
operation and a candidate-specific prediction; a fair simple or null attribution
baseline; and a recorded pre-pattern freeze basis in Section 7.2. "Return to the earliest
missing stage instead of using a pattern to fill a gap."

The router then compiles a fingerprint without architecture-family or paper names —
`Candidate ID`, target `FAIL-*` and addressed `LINK-*`, preserved `INV-*`, core
operation, primary changed axis, new prediction `CLM-*`, fair attribution contrast — and
chooses **exactly one primary axis** from:

```text
MECHANISM | MODELED-OBJECT | REPRESENTATION | GRANULARITY
| RESPONSIBILITY | INFORMATION-FLOW | CONSTRAINT | OBJECTIVE
| COMPUTATION | OPTIMIZATION | THEORETICAL-PROPERTY
| MEASUREMENT-FRAMEWORK | OTHER
```

"Use `OTHER` when the candidate is coherent but no listed axis fits. Do not distort the
candidate to obtain a catalog match." (`references/iclr-pattern-index.md` line 59)

### 4.2 Bounded loading

For each `PRIMARY` or `MINIMAL` candidate (`references/iclr-pattern-index.md` lines
76–83):

1. route from the fingerprint to one primary card;
2. load and test that card's structural contract;
3. on a mismatch, check at most one reasoned substitute chosen from the diagnosed failure
   or changed axis;
4. if a card matches, load one supporting card only when the core operation necessarily
   changes a second axis and the interaction has its own prediction;
5. stop after at most two loaded cards per candidate;
6. record one concrete mismatch, unsupported assumption, or transfer risk even for a
   useful match.

The result is exactly one internal token: `MATCHED` or `NO-STRUCTURAL-MATCH`.
"Use `NO-STRUCTURAL-MATCH` when neither the primary nor the one justified substitute
satisfies the causal structure. Catalog absence is not evidence for or against the
candidate." (`references/iclr-pattern-index.md` line 91)

Composition rule: keep one primary pattern; add one supporting pattern only when the
primary operation cannot be instantiated without the second structural move, the second
move has a distinct responsibility, the interaction yields a testable prediction, and
individual and joint ablations can distinguish their effects. "Treat three or more
primary-looking moves as a system-bundle warning."
(`references/iclr-pattern-index.md` lines 118–125)

### 4.3 Personal routing

Personal routing compares the frozen candidate's failure location, causal link,
invariant, and broken assumptions against the route-map signatures
(`references/personal-pattern-index.md` lines 11–20). At most one card is loaded per
candidate; "Require at least one structural mismatch or boundary before retaining an
analogy"; and if no row matches, "record that personal patterns were not consulted. Do not
broaden the candidate set to create a match."

The shipped default configures **no rows**: its route map holds a single
`_(none configured)_` placeholder (`personal-pattern-index.md` lines 24–29), so the shipped
state always records that personal patterns were not consulted. An index whose route map
matches nothing is a valid state (`SKILL.md` line 205), not an incomplete profile.

### 4.4 What the audit must leave behind

Routing is only complete when its result is recorded in the dossier's existing fields —
cards never create new sections (`references/iclr-pattern-index.md` lines 129–137):

| Record | Where it goes |
|---|---|
| Consulted card ID, consulted after freeze, purpose, mismatch or transfer risk found, effect | Section 7.2 Reference-Use Log row (`idea-dossier-template.md` line 221) |
| Effect value, one of exactly `retained`, `bounded`, `rejected` | Section 7.2, `Effect on candidate set` |
| A real assumption or bounded prediction the card exposed | An existing or updated `CLM-*` row in Section 3 |
| A new decisive contrast | One reserved `EXP-*` row in Section 13 |
| Gate result | G5 in Section 15 |

The personal index's Reference-Use Record uses the same content in a compact form:
`Card loaded`, `Structural match`, `Concrete mismatch or boundary`, `Risk or falsifier
learned`, `Effect on candidate: retained | bounded | rejected`
(`references/personal-pattern-index.md` lines 43–53).

## 5. What disqualifies a card (and a route)

A card must not be routed, and a proposed card must not be accepted, when the match is
cosmetic or when the card cannot reject anything.

**Disqualifying match types**, quoted from the indexes:

| Disqualifier | Source |
|---|---|
| "Load no card when only terminology, module type, diagram shape, or application area matches" | `references/personal-pattern-index.md` lines 15–16 |
| "load none when only terminology or module shape matches" | `SKILL.md` line 114 |
| Transfer by "method name, metaphor, diagram shape, or venue prestige" | `SKILL.md` line 223 |
| Routing to a `SIMPLE-BASELINE` or `NULL-BASELINE` candidate | `references/iclr-pattern-index.md` line 34 |
| A card whose route map matches every candidate ("a horoscope, not a router") | `PERSONALIZE.md` lines 69–70 |

**Per-card "do not route when" conditions** already enumerated in the ICLR index
(`references/iclr-pattern-index.md` lines 63–72), which any new row must imitate in
spirit:

| Card | Do not route when |
|---|---|
| `iclr-pattern-a-mechanism.md` | The candidate only renames or groups symptoms |
| `iclr-pattern-b-modeled-object.md` | The change only reshapes a tensor or adds an embedding |
| `iclr-pattern-c-granularity.md` | More options are added without preserving interfaces |
| `iclr-pattern-d-responsibility.md` | Separation is only architectural tidiness |
| `iclr-pattern-e-information-flow.md` | A new edge only adds capacity or shortens gradients |
| `iclr-pattern-f-invariant.md` | The alleged invariant is downstream performance itself |
| `iclr-pattern-g-objective-computation.md` | The change is routine code optimization with the same estimand |
| `iclr-pattern-h-operational-framework.md` | A new metric or theorem changes no scientific conclusion |

Two structural disqualifiers for a *proposed* card:

- **Unrouted.** "A card that no index routes to is dead weight."
  (`CONTRIBUTING.md` lines 31–32)
- **Unfalsifiable routing.** If a reviewer cannot construct a frozen candidate that must
  *not* match the card, the card is advice rather than a router
  (`PERSONALIZE.md` lines 69–70).
- **Disclosing.** A card from a project that is not published yet must not be submitted at
  all: "keep it in `profiles/private/`. A contributed profile is public forever, and a
  precedent card is specific enough to describe an unpublished project."
  (`profiles/README.md` lines 61–63)

## 6. Submission checklist

1. **Pick the family and slot.** `iclr-pattern-*` for the public catalogue;
   `personal-pattern-card-a.md`, `personal-pattern-card-b.md`, or
   `personal-pattern-card-c.md` for profile precedent. Do not rename an existing slot:
   the filenames are fixed, and "deliberately generic", because "a descriptive name would
   disclose your research directions in a filename alone" (`PERSONALIZE.md` lines 82–85).
   Adding a fourth card is done by adding an index row and a file beside the others
   (`PERSONALIZE.md` lines 87–89). A card from an unpublished project is never submitted —
   it stays in `profiles/private/` (`profiles/README.md` lines 61–63).
2. **Write the card** with the anatomy for its family ([section 3](#3-card-anatomy)) and
   keep it short. It must state scope, structural trace or contract, the minimum
   contrast, the killing test, and the do-not-generalize boundary.
3. **Add the index row.** Personal: a `Structural signature | Card | Exclusion` row in
   `references/personal-pattern-index.md`. ICLR: a
   `Candidate structure | Primary card | Do not route when` row in
   `references/iclr-pattern-index.md`, plus the card in that file's section-8 manifest and
   in the card list in `SKILL.md` lines 194–203. "A new pattern card must be added to the
   matching index (and, for ICLR cards, to the router table in `SKILL.md`)."
   (`CONTRIBUTING.md` lines 30–32)
4. **Ship at least one eval expectation.** This is a repository rule, not a suggestion:
   "Any change to a `SKILL.md`, a reference file that a stage loads, or the dossier
   template must add or update at least one expectation in
   `skills/time-series-model-ideation/evals/evals.json`. A prompt change without a test is
   an unverified claim, which is exactly what this project exists to prevent."
   (`CONTRIBUTING.md` lines 9–13) A card is a reference file that Stage 5 loads, so this
   applies. See [section 7](#7-the-eval-expectation) for what to write.
5. **Keep paths resolvable.** Every reference path must resolve; `scripts/lint.mjs`
   "fails the build on a dangling path" (`CONTRIBUTING.md` lines 27–29).
6. **Keep profiles in sync.** If you changed a live `personal-*.md` slot, update
   `profiles/default/` in the same pull request; CI compares them
   (`CONTRIBUTING.md` lines 38–40). If you are publishing your own stance, contribute a
   complete six-file profile instead (`CONTRIBUTING.md` lines 90–107).
7. **Run the checks.** "Before opening a pull request, run `make lint && make self-test`.
   Both also run in CI." (`CONTRIBUTING.md` line 54)
8. **Hygiene.** No personal data, names, affiliations, or unpublished project details; no
   copied text from papers, blogs, or other repositories — paraphrase and cite
   (`CONTRIBUTING.md` lines 33–35); no vendored third-party content (lines 36–37); one
   concern per pull request; explain why and state what you ran (lines 120–121); do not
   commit your own applied profile (line 122).
9. **If the change touches gate semantics**, say so in the pull request body and preserve
   the semantics table verbatim otherwise (`CONTRIBUTING.md` lines 74–75).

## 7. The eval expectation

The suite is `skills/time-series-model-ideation/evals/evals.json`: one JSON object with
`skill_name` and an `evals` array holding twelve cases. Each case has `id`, `prompt`,
`expected_output`, `files`, and a list of prose `expectations`; the per-case expectation
counts live in that file and are not repeated here, because they change as the suite
grows. Cases 7, 8, 10, and 11 attach fixtures from
`skills/time-series-model-ideation/evals/files/`.

What a card change needs is an expectation that would **fail before the change and pass
after it**. Two shapes work:

- **Route to the new card.** A Stage-5 case (the existing Stage-5 cases are 2 and 12)
  whose candidate matches the new signature, with an expectation such as "the dossier
  records the new card ID in the Section 7.2 Reference-Use Log with a concrete structural
  mismatch." Without the index row, the routing would not happen and the expectation
  fails.
- **Do not route to the new card.** A case built on the card's exclusion cell, with an
  expectation that the candidate is retained without a card or routed to a different
  card. This is the expectation that guards the "routing must be able to fail" rule.

Practical notes:

- Adding a case means adding an object to the `evals` array; updating an expectation
  means editing an existing case's `expectations` list. Both satisfy the rule as written
  ("add or update at least one expectation"), but a new case also changes the case count
  quoted in documentation, so update the number wherever it is stated.
- Expectations are prose assertions, so the runner cannot check them by string match
  alone. `CHANGELOG.md` lines 67–69 describe the intended split: a deterministic offline
  structural tier and an opt-in model-judged tier. Write the expectation so a structural
  grader has something to check (a card ID, an effect value, a gate state) instead of
  only an impression.
- Check that your new expectation does not contradict an existing one, especially on the
  Stage-5 cases: "if you make a rule stricter, check that no existing eval expectation now
  contradicts it, and update the expectation deliberately rather than silently"
  (`CONTRIBUTING.md` lines 79–80).

## 8. Copy-paste skeleton

### 8.1 Personal card

```markdown
# Personal Pattern — <short structural name>

## Conditional Precedent

Use only when <the one diagnosed structure that licenses this card>.

## Structural Trace

- **Need:** <the need this precedent serves, without a method name>
- **Failure:** <the localized failure it addresses>
- **Suspected cause:** <the causal link that explains the failure>
- **Invariant:** <the measurable property to preserve; never forecast accuracy itself>
- **Mechanism:** <the operative principle to transfer, not a module name>

## Direct-Use Risks

Check <the target-regime conditions that could break the precedent: sampling, locality,
stationarity, interfaces, gradients, cost, invalid cases, ...>.

<The rule for adapting only supported violations, and the separate test that keeps the
mechanism connected to task relevance.>

## Theory Boundary

Bound <the properties that may be stated under explicit assumptions>. Do not infer
<the task-level conclusion that these properties do not license>.

## Rival and Killing Test

Treat <rival explanations and matched comparisons> as rivals. Reject or pivot the claim
when <the observations that would falsify it>.

## Do Not Generalize To

Do not apply this precedent to <the adjacent settings where it is invalid>.
```

### 8.2 ICLR card

```markdown
# Pattern <X> — <imperative one-line claim>

## Route When

Use when <the structural condition>.

```text
<step 1, e.g. a coarse operation>
-> <step 2, e.g. the measurable intermediate it hides>
-> <step 3, e.g. the required distinction or repair>
-> <step 4, e.g. the observable consequence>
```

## Structural Contract

- <Required property 1>
- <Required property 2>
- <Required property 3>
- <The mismatch rule: what must be treated as a non-match.>

## Minimum Contrast

<The smallest experiment that distinguishes the pattern from its rivals, including the
matched control and the measurement taken separately from task performance.>

## Reject or Return When

Reject or revisit the diagnosis when <condition 1>, <condition 2>, or <condition 3>.

## Time-Series Hazards

<The domain-specific traps: what must be localized or checked before the pattern's
language is applied to time series.>
```

### 8.3 Index rows

Personal — append to the Route Map in `references/personal-pattern-index.md`:

```markdown
| <structural signature: failure + causal link + invariant> | `references/personal-pattern-<name>.md` | <the exclusion: when this row must not match> |
```

ICLR — append to the Routing Table in `references/iclr-pattern-index.md`:

```markdown
| <candidate structure> | `iclr-pattern-<x>-<name>.md` | <do not route when: the cosmetic or non-structural lookalike> |
```

Then add the new ICLR card to the section-8 manifest in the same index file and to the
card list in `SKILL.md` lines 194–203.
