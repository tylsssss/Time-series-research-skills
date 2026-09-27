# FAQ

Twelve questions about what this repository is, what it does not do, and where its
limits are. Answers cite the file that states the rule; where the honest answer is "the
repository does not say" or "this is not implemented yet", the answer says so.

## 1. How is this different from a well-written prompt?

A prompt is text you rewrite per task. This is a stage controller with a frozen output
contract, an evidence discipline, and a decision procedure.

| Dimension | A well-written prompt | This repository |
|---|---|---|
| Output shape | Whatever the model decides | One Idea Dossier: Sections 0–16 in fixed order, fixed fields, fixed enums (`SKILL.md` line 31 makes the template the sole authority for them) |
| Checkability | Reviewer judges the prose | A reviewer can state which gate passed without evidence, because gate states, evidence levels, and ID links are explicit fields |
| Ordering | Implicit | Candidates must be frozen before any pattern source is read (`SKILL.md` line 104); no repair design while G2, G3, or G4 is unresolved (`SKILL.md` line 100) |
| Evidence | Usually untyped | Planned experiments are plans, never evidence (`SKILL.md` line 46); missing decision-relevant evidence is recorded as `UNRESOLVED` with `E0`, not omitted (`SKILL.md` line 47) |
| Failure mode | Gives you an architecture anyway | Refuses: eval case 1 expects "a progressive Idea Dossier that refuses premature architecture generation" |

What it does not buy you: it is not a guarantee of quality, novelty, or correctness, it
is not a literature database, and it does not replace domain expertise. It makes the
reasoning auditable; it does not make the reasoning right.

## 2. Why is the output so heavy — do I need all 17 sections?

You need all 17 *headings*, not all 17 bodies. Section lifecycle is the mechanism:

- `ACTIVE` or `COMPLETE`: full body, no blank cells, no unreplaced placeholders.
- `NOT-STARTED` or `BLOCKED`: "emit only the heading and lifecycle block. Do not
  instantiate the remaining fields or tables for that section."
  (`assets/idea-dossier-template.md` line 9)

So a run that stops at Stage 5 emits Sections 0–7 with full bodies and Sections 8–16 as
headings only. Two shipped eval cases test exactly this boundary: case 2 ("Work only
through Stage 5 and stop before direct-use assessment") and case 12 ("Stop at the Stage-5
boundary").

Why the weight is still the point: every downstream claim has to point at the exact row
that supports or contradicts it (`CLM-*`, `LINK-*`, `FIND-*`, `EXP-*`), so a later audit
can say "G3 rests on `CLM-004`, which is `E2`" instead of re-reading prose. If you want a
quick opinion about an idea, this is the wrong tool: it will refuse to design first and
ask questions later.

## 3. Can I use it without an API key or outside Claude?

Yes for the instructions themselves. The skills are Markdown plus one JSON eval file.
There is no executable code in `skills/`, no dependency to install, and no network call
required by the skill text. The development tooling that does exist requires only
`python3` (3.9+) and `node` (18+): "No package installation is needed — the runner and
the linters use only the standard library" (`CONTRIBUTING.md` lines 44–45).

Three honest caveats:

1. **The novelty audit needs real literature access.** Without primary sources, the
   correct outcome is `UNKNOWN` or `CONDITIONAL`, not `PASS`
   (`references/novelty-audit.md` lines 388–392). An agent with no search capability can
   still produce the dossier, but Section 10 will be unresolved and the final decision
   will be `NEED-EVIDENCE`.
2. **Nothing verifies your evidence levels.** The skill records `E0`–`E5`; it does not
   check that a claimed `E4` was a matched comparison.
3. **The optional Tier-2 eval tier needs an API key.** Tier-1 structural grading is
   fully offline; Tier-2 is the model-in-the-loop tier and "is skipped cleanly (exit 0)
   when none is present" (`evals/run.py` lines 11–12). See
   [question 10](#10-how-do-i-run-the-evals).

## 4. Which agent platforms does it work on?

The portable core is the Agent Skills convention: each skill is a directory with a
`SKILL.md` carrying YAML frontmatter (`name`, `description`) plus references and assets.
Everything else is plain Markdown, so any runtime that can read files and follow
instructions can use it.

Platform-specific metadata that does ship:

| Artifact | What it declares |
|---|---|
| `skills/time-series-model-ideation/agents/openai.yaml` | `products: chatgpt, codex, api, atlas` and `allow_implicit_invocation: true` |
| `skills/time-series-code-implementation/agents/openai.yaml` | Same product list and policy |
| `.claude-plugin/marketplace.json` | A plugin named `time-series-research` listing both skill directories as sources |
| `scripts/install.sh` | Installer for "Claude Code, Codex / `~/.agents/skills`, and project-local installs" (`CHANGELOG.md` line 73), driven by `make install-user` / `make install-project` |

For a runtime with no skills mechanism, `CHANGELOG.md` line 75 describes
`scripts/build-bundle.mjs`: "flattens a skill plus the references it needs into a single
Markdown bundle for agents without a skills mechanism."

Two cautions. First, both `agents/openai.yaml` files were present at measurement time;
`scripts/build-bundle.mjs` and the install targets it drives were referenced by
`Makefile` and `CHANGELOG.md` but the bundle script itself was not yet in the tree.
Second, the repository README (maintained separately) is the place for the supported
platform matrix — do not infer support from the presence of a single adapter file.

## 5. What does it explicitly NOT do?

| Not done | Source |
|---|---|
| Implement or debug a frozen method | Ideation skill description: "Do not use for implementing or debugging a frozen method" |
| Write paper prose or figures | "Stop after the dossier without code, polished paper prose, or final figures" (`SKILL.md` line 217) |
| Produce literature-only summaries or polish papers | Same description line |
| Predict venue acceptance | The pattern index is "not official pattern definitions, acceptance rules, or a venue-success predictor" (`references/iclr-pattern-index.md` line 5) |
| Score novelty or aggregate gates | "Do not emit numeric novelty or aggregate gate scores" (`SKILL.md` line 229) |
| Require every component to be novel | "Do not require every component to be novel. Require every claimed CORE contribution to survive the audit." (`references/novelty-audit.md` line 333) |
| Infer task benefit from a structural property | "Do not infer task benefit from reconstruction, invertibility, stability, legality, expressivity, or information preservation alone" (`SKILL.md` line 54) |
| Use pattern cards as evidence, candidate generators, or novelty sources | `SKILL.md` line 52 |
| Treat execution as feasibility | "Do not call a method feasible because a dry run executes" (`references/feasibility-audit.md` line 206) |
| Re-open an unsettled method in the implementation skill | It offers "a lightweight frozen-spec check or a handoff to `time-series-model-ideation`" instead (`skills/time-series-code-implementation/SKILL.md` line 43) |

The implementation skill has its own ceiling: "Stop at research-code level — no paper
prose, no polished publication figures" (`skills/time-series-code-implementation/SKILL.md`
line 17).

## 6. How do I use my own research priors and pattern cards instead of the shipped neutral layer?

You do not replace anyone's layer: the repository ships a **neutral skeleton** and you
supply your own stance. The personal layer is six **slots**, and a profile is a complete
replacement for all six: "Partial replacement is not supported: a half-swapped layer
produces contradictions between the priors file and the pattern cards"
(`PERSONALIZE.md` lines 8–9).

The six slots (`PERSONALIZE.md` lines 13–20):

| Slot | Feeds |
|---|---|
| `references/personal-research-priors.md` | Ideation, Stage 0, Stage 8, and the final decision |
| `references/personal-pattern-index.md` | Ideation, Stage 5 routing |
| `references/personal-pattern-card-a.md` | Ideation, Stage 5 — precedent card slot A |
| `references/personal-pattern-card-b.md` | Ideation, Stage 5 — precedent card slot B |
| `references/personal-pattern-card-c.md` | Ideation, Stage 5 — precedent card slot C |
| `references/personal-code-style.md` | Implementation, Phases 2–4 |

Each card slot holds "one structural precedent from your own work" (`PERSONALIZE.md` lines
17–19), and all three ship empty.

What ships (`PERSONALIZE.md` lines 22–27): `profiles/default/` is "a neutral skeleton: the
same six files, no preferences, no precedent content, and a note in each about what belongs
there. It is the honest starting point — you get the gates and the typed dossier without
inheriting anyone's research taste, and no file in this repository describes an unpublished
project."

Practical procedure:

1. Keep your own layer local. "A `private` profile is the intended way to keep your own
   layer locally. It is git-ignored, so it never reaches the public repository"
   (`PERSONALIZE.md` lines 29–30): copy the skeleton with
   `cp profiles/default/*.md profiles/private/` and write your own files there
   (`PERSONALIZE.md` lines 32–35).
2. Apply it with `scripts/use-profile.sh private`; inspect with `--list`, compare the live
   slots with the shipped default using `--check`, and restore the default with
   `scripts/use-profile.sh default` (`PERSONALIZE.md` lines 36–39). Applying backs up the
   previous slot contents to `profiles/.backup/<timestamp>/` (`PERSONALIZE.md` lines 47–49).
3. Write priors as selection rules, not vetoes: "A prior that can override evidence is a
   bug, not a preference" (`PERSONALIZE.md` line 59). Keep the five-section structure,
   because three moments load the file — "the boundary stage, the novelty audit at Stage 8,
   and the moment before the final decision" (`PERSONALIZE.md` lines 53–55) — and record
   each addition with the file's own update block: `Prior / Type / Source / Scope /
   Rationale / Exceptions / Conflicts / Last confirmed`
   (`references/personal-research-priors.md` lines 39–48). The shipped skeleton records the
   absence of a preference rather than inventing one: resolve choices "by evidence, task
   constraints, and the canonical gates alone, and record the tie-break as
   `NO-PERSONAL-PREFERENCE`" (`references/personal-research-priors.md` lines 19–21).
4. Write cards as conditional precedents: "a structural signature, the failure it explains,
   the invariant it preserves, its direct-use risks, its theory boundary, and the test that
   would kill it" (`PERSONALIZE.md` lines 61–63). "A card is a stress-test instrument used
   **after** the candidate set is frozen — never evidence, never a candidate generator,
   never a novelty source", and "the routing must be able to fail"
   (`PERSONALIZE.md` lines 67–70).
5. Do not rename the card slots. Their filenames are fixed and "deliberately generic
   (`personal-pattern-card-a/b/c.md`)", because "a descriptive name would disclose your
   research directions in a filename alone" (`PERSONALIZE.md` lines 82–85). Rewrite the
   contents freely, and add a fourth card "by adding a row to `personal-pattern-index.md`
   and a file beside them" (`PERSONALIZE.md` lines 87–89).
6. Never put your real stance in the shipped default, and do not commit your private
   profile: "Your priors and precedent cards describe your research direction and are
   usually unpublished" (`PERSONALIZE.md` lines 94–95). To publish a stance deliberately,
   contribute it as a directory under `profiles/` (`CONTRIBUTING.md` lines 90–107); if your
   stance comes from unpublished work, the fifth step says not to contribute it at all and
   to keep it in `profiles/private/` (`CONTRIBUTING.md` lines 104–107).

If you do change the shipped slots in place, update `profiles/default/` in the same
commit: "`profiles/default/` must stay byte-identical to the live slots"
(`profiles/README.md` lines 46–52).

## 7. How do I add a domain pattern card?

Add the card file, add a row to the matching index, keep every router in sync, and ship
at least one eval expectation. The detailed anatomy and checklist are in
[`docs/contributing-a-pattern-card.md`](contributing-a-pattern-card.md); the repository
rules that bind the change are:

- **Card families.** `iclr-pattern-*` is the public argument-structure catalogue;
  `personal-pattern-*` is profile-specific precedent and "belongs in a profile, not in
  the shipped default unless you are the profile's author" (`CONTRIBUTING.md` lines
  85–88).
- **Routers stay in sync.** "A new pattern card must be added to the matching index (and,
  for ICLR cards, to the router table in `SKILL.md`). A card that no index routes to is
  dead weight." (`CONTRIBUTING.md` lines 30–32)
- **Eval expectation required.** "Any change to a `SKILL.md`, a reference file that a
  stage loads, or the dossier template must add or update at least one expectation in
  `skills/time-series-model-ideation/evals/evals.json`." (`CONTRIBUTING.md` lines 9–13) A
  card is a reference file a stage loads, so this applies.
- **Reference paths must resolve.** `scripts/lint.mjs` "fails the build on a dangling
  path" (`CONTRIBUTING.md` lines 27–29).
- **No third-party text.** Paraphrase and cite; do not copy text from papers, blogs, or
  other repositories (`CONTRIBUTING.md` lines 33–37).

## 8. Does passing the novelty audit mean my idea is novel?

No. `PASS` is a bounded, per-candidate, non-numeric status meaning: within the recorded
search boundary and for the frozen subject, at least one CORE contribution survived a
direct closest-neighbor comparison, no unresolved overlap could reasonably cover it, a
distinguishing empirical or formal consequence exists, and the novelty claim states what
is inherited and what survives (`references/novelty-audit.md` lines 366–378).

What it does not mean:

- **Search absence is not novelty.** It supports "not found within the stated boundary"
  and nothing more (`references/novelty-audit.md` line 267).
- **Novelty is not mechanism evidence.** "Do not treat a planned or observed consequence
  as evidence that the contribution is novel; novelty evidence comes from the technical
  contrast with prior work" (`references/novelty-audit.md` line 360). Stage 11 still has
  to falsify the mechanism.
- **The audit can be wrong in either direction.** It can only compare against neighbors
  the search found; the protocol demands the strongest available neighbor, adjacent-field
  search, and negative results, but it cannot prove none was missed
  (`references/novelty-audit.md` lines 214–229).
- **`CONDITIONAL` and `UNKNOWN` are legitimate outcomes**, and an unresolved audit routes
  to `NEED-EVIDENCE` rather than being rounded up (`SKILL.md` line 136).

## 9. Can I use it for non-time-series research?

Not as shipped. Both skills are scoped to time-series models by their own descriptions,
and the time-series commitment is structural, not cosmetic:

- Section 9 is "Time-Series Adaptation and Component Contracts", and Section 0 requires
  a `data_regime` of "data, sampling, horizon, and deployment regime".
- Every ICLR card ends with a `Time-Series Hazards` section (for example
  `references/iclr-pattern-a-mechanism.md` lines 30–32).
- `references/mechanism-transfer.md` audits transfer **into** the target time-series
  regime; it is not a domain-general transfer procedure.
- The three shipped personal cards are time-series precedents, and the priors file
  encodes time-series preferences (temporal semantics, forecasting causality, causal
  access at inference).

What does transfer: the argument skeleton (need → observable failure → causal mechanism
→ preserved invariant → candidates → direct use → adaptation → novelty → feasibility →
theory → falsification → decision) and the evidence discipline are field-agnostic. So a
careful port is possible — but it means authoring your own cards and priors, translating
Section 9, and accepting that several fields and enums will be awkward. Nothing in this
repository claims or tests non-time-series use; do not expect the shipped profile to be
relevant.

## 10. How do I run the evals?

**What exists now.** A declarative suite at
`skills/time-series-model-ideation/evals/evals.json`: twelve cases, each with `id`,
`prompt`, `expected_output`, `files`, and a list of prose `expectations`. Expectation
counts per case are maintained in that file, not here. Cases 7, 8, 10, and 11 attach
fixtures from `skills/time-series-model-ideation/evals/files/`:

| Case | Focus (from its prompt and expected output) | Fixture |
|---|---|---|
| 1 | `GENERATE`: refuses a requested Diffusion + GNN + LLM stack, issues `NEED-EVIDENCE` | — |
| 2 | `GENERATE`: stops at Stage 5 with a frozen candidate set | — |
| 3 | `AUDIT`: preserves a supplied candidate, `NO-ADAPTATION-REQUIRED`, stops before novelty | — |
| 4 | `AUDIT`: cross-domain transfer audited through Stages 5–7 | — |
| 5 | `REPAIR`: rejects retrospective justification, returns to the earliest failed gate, `PIVOT` | — |
| 6 | `COMPARE`: exactly three research candidates, extra comparator in the experiment matrix | — |
| 7 | `AUDIT`: novelty audit returns `UNKNOWN`, decision `NEED-EVIDENCE` | `evals/files/eval-7-upstream-snapshot.md` |
| 8 | `AUDIT`: feasibility and theory repair after new evidence, inherited theorem invalidated | `evals/files/eval-8-stale-upstream-snapshot.md` |
| 9 | `AUDIT`: contradicted failure and mechanism, candidate rejected, `KILL` | — |
| 10 | `AUDIT`: primary-source coverage forces novelty `FAIL`, decision `PIVOT` | `evals/files/timekan-primary-source-excerpt.md` |
| 11 | `AUDIT`: complete dossier compiled from a source-validated fixture | `evals/files/integration-evidence-packet.md` |
| 12 | `AUDIT`: Stage-5 boundary, `NO-STRUCTURAL-MATCH` without penalizing the candidate | — |

**Runner.** `evals/run.py` takes exactly one mode (`evals/run.py` lines 4–14 and
798–800):

| Command | What it does |
|---|---|
| `python3 evals/run.py --list` | List the behavioural eval cases shipped by a skill |
| `python3 evals/run.py --grade <dossier.md>` | Run the Tier-1 structural grader on one dossier |
| `python3 evals/run.py --self-test` | Grade both fixtures and check the documented defects |
| `python3 evals/run.py --tier2` | Run the behavioural (model-in-the-loop) Tier-2 eval |

Tier-1 is "fully offline and deterministic"; Tier-2 "needs an API key and is skipped
cleanly (exit 0) when none is present". Exit codes: 0 ok, 1 grading failure, 2 usage
error. Tier-2 accepts `--provider`, `--model`, `--judge-model`, `--case`, `--out`
(default `evals/results/`), `--max-tokens`, `--timeout`, and `--no-skill-context`.
`--json` emits machine-readable output. Make targets wrap the same entry points:
`make lint`, `make self-test`, `make grade F=<dossier.md>` (`Makefile` lines 24–32;
`CONTRIBUTING.md` lines 47–54 and 115–116).

**Fixtures and grader.** The deterministic grader is `evals/graders/structural.py`; the
regenerable fixtures are `evals/fixtures/good-dossier.md`,
`evals/fixtures/bad-dossier.md`, and `evals/fixtures/make_fixtures.py`. `CHANGELOG.md`
lines 28–30 states the design: "a dependency-free runner with deterministic structural
grading (Tier 1, offline, CI-safe) and an opt-in model-judged tier (Tier 2), plus
regenerable good/bad dossier fixtures and a self-test."

**State (checked 2026-09-27 13:54 CST).** `evals/run.py`,
`evals/graders/structural.py`, `evals/README.md`, and the fixtures are present, and
`node scripts/lint.mjs` passes with no errors. The suite is still
listed under `[Unreleased]` in `CHANGELOG.md`, so treat this page's "how to run" commands
as the interface the runner documents in its own `--help` and re-check your checkout
before promising a green `make self-test`.

**If a runner is missing in your checkout**, the suite is still usable as a manual
rubric: give an agent one `prompt` (plus its fixture, when the case has one) and check the
`expectations` list line by line. The expectations are prose assertions, which is why the
Tier-1 structural grader checks dossier structure rather than judging every sentence.

## 11. What happens if my evidence is all E0?

`E0` means "UNKNOWN; no relevant evidence" (`idea-dossier-template.md` line 107), and a planned measurement
counts as `E1` at most (`references/problem-diagnosis.md` line 198). With no evidence:

1. **G2, G3, and G4 cannot be `SATISFIED`.** They stay `UNRESOLVED`, with `state`
   unresolved and `failure_mode: null`.
2. **The canonical route is `NEED-EVIDENCE`** — "Decision-relevant gate unresolved; no
   gate unsatisfied" (`SKILL.md` line 172) — and Section 16 must name "the smallest
   decisive test or search" (`idea-dossier-template.md` line 474).
3. **`GO` is impossible**, because `GO` requires every gate `EVALUATED` and `SATISFIED`
   (`idea-dossier-template.md` line 473).
4. **That is not a kill.** `KILL` requires a decisive gate `UNSATISFIED + CONTRADICTED`
   with no substantive repair (`idea-dossier-template.md` line 476). The shipped skeleton
   also refuses to read an empty preference file as a verdict: until a section is filled
   in, resolve choices "by evidence, task constraints, and the canonical gates alone, and
   record the tie-break as `NO-PERSONAL-PREFERENCE`"
   (`references/personal-research-priors.md` lines 19–21).
5. **The dossier is still valuable**: Section 13 holds the experiments that would change
   the decision, and Section 16 names the smallest next action.

This is the designed behavior, not a degenerate case: eval case 1 supplies no
measurement, ablation, or causal evidence and expects a refusal plus the smallest
diagnostic that would change the decision.

## 12. What stops the model from writing a plausible-sounding dossier?

Structural devices, none of which verify facts:

| Device | Effect |
|---|---|
| Typed claims with provenance and `E0`–`E5` | An unsupported assertion is visible as a claim with weak evidence instead of hiding in prose (`idea-dossier-template.md` lines 97–113) |
| `DERIVED-ONLY` compilation sections | Sections 14–16 cannot introduce new claims: "Do not introduce claims in Sections 14–16 that are absent from Sections 2–13" (`idea-dossier-template.md` line 32) |
| ID cross-references | Every gate cites "Decisive ledger IDs"; every component cites the `FIND-*` it repairs; every `EXP-*` cites the claims it tests |
| Lifecycle honesty | Missing evidence must be an `UNRESOLVED` claim with `E0`, never a blank cell or `N/A` (`idea-dossier-template.md` line 13) |
| Gate states and failure modes | A gate that was never evaluated must say `DEFERRED`; "do not pretend the gate was evaluated" (`idea-dossier-template.md` line 429) |
| `decision_consistency_check` | "Set `decision_consistency_check: PASS` only when the stated decision follows the matching rule and all listed gate IDs agree with Section 15" (`idea-dossier-template.md` line 477) |
| Falsification coverage | `core_claim_ids` / `covered_core_claim_ids` / `uncovered_core_claim_ids` / `coverage_complete` make an untested CORE claim explicit (`idea-dossier-template.md` lines 379–382) |
| The eval suite | Twelve cases, several of them adversarial: they expect refusals, `PIVOT`, `KILL`, and `UNKNOWN` rather than a confident answer (`skills/time-series-model-ideation/evals/evals.json`) |

The honest limit: these devices make unsupported claims *legible*; they do not make them
*impossible*, and nothing checks your `E`-levels, your search coverage, or whether your
`LINK-*` chain is real. That is why `CONTRIBUTING.md` asks for behavioral failure reports
— "a reproducible behavioral failure is the most valuable contribution to this
repository" (`CONTRIBUTING.md` line 116).
