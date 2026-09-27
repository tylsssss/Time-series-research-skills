# `evals/` — runnable eval harness for the time-series research skills

The whole selling point of this repository is **no claim without evidence**. The
skill `skills/time-series-model-ideation/` ships a behavioural eval suite
(`skills/time-series-model-ideation/evals/evals.json`) of **12 cases and 99
expectations**, eight or nine per case, as of dossier schema 1.1.0. Until now
there was no way to run them. This directory adds one, in two tiers:

| Tier | What it does | Needs a key? | Deterministic? |
|---|---|---|---|
| **Tier-1 structural** (`evals/graders/structural.py`) | Checks one produced dossier against the contract in `assets/idea-dossier-template.md` | No — fully offline | Yes, byte-for-byte |
| **Tier-2 behavioural** (`evals/run.py --tier2`) | Sends a case prompt to a model and judges its 8–9 expectations | Yes | No — model judgements |

Everything is Python 3.9+ **standard library only**. No third-party imports, no
network access in Tier-1, no timestamps in Tier-1 output.

---

## 1. Commands

```bash
# list the behavioural cases: id, expectation count, fixture files
python3 evals/run.py --list
python3 evals/run.py --list --json

# Tier-1: grade one produced dossier (exit 1 if any error-severity check fails)
python3 evals/run.py --grade evals/fixtures/good-dossier.md
python3 evals/run.py --grade path/to/produced-dossier.md --json
python3 evals/run.py --grade path/to/dossier.md --skill time-series-model-ideation

# the grader on its own (same engine, no CLI wrapper)
python3 evals/graders/structural.py evals/fixtures/bad-dossier.md
python3 evals/graders/structural.py evals/fixtures/bad-dossier.md --json

# Tier-1 self-test: good fixture must pass, bad fixture must trip every defect it documents
python3 evals/run.py --self-test
python3 evals/run.py --self-test --json

# Tier-2: behaviour against a real model (skipped cleanly with exit 0 when no key)
python3 evals/run.py --tier2 --case 1
python3 evals/run.py --tier2 --case 1,7,11 --provider deepseek --model deepseek-chat
DEEPSEEK_API_KEY=... python3 evals/run.py --tier2 --case 1 --out evals/results/

# fixtures are generated from the shipped template; --check fails if they are stale
python3 evals/fixtures/make_fixtures.py
python3 evals/fixtures/make_fixtures.py --check
```

Exit codes for every mode: `0` ok, `1` grading failure, `2` usage error.

A zero-key CI job is therefore just:

```bash
python3 evals/fixtures/make_fixtures.py --check   # fixtures match the template
python3 evals/run.py --self-test                  # grader works in both directions
python3 evals/run.py --grade evals/fixtures/good-dossier.md
python3 evals/run.py --list
```

---

## 2. Tier-1 checks

Every rule below is derived from
`skills/time-series-model-ideation/assets/idea-dossier-template.md` and the
contract in `skills/time-series-model-ideation/SKILL.md`. Checks run in a fixed
order, each has a stable id, a severity, a human message and the offending line
number where one exists. `error` findings fail the grade; `warning` findings are
reported but do not change the exit code.

| id | title | severity | what it enforces (template authority) |
|---|---|---|---|
| S01 | `sections-present` | error | Headings `## 0.` … `## 16.` all present, no heading outside 0–16 (template: "Preserve sections 0–16 and their order"). |
| S02 | `section-order` | error | Section numbers strictly ascending in document order; duplicates and inversions are reported with the offending heading line. |
| S03 | `placeholders` | error | No unreplaced `{{REQUIRED: …}}` token anywhere outside HTML comments. |
| S04 | `lifecycle-values` | error | Every section carries a `section_status` whose value is one of `NOT-STARTED \| ACTIVE \| COMPLETE \| BLOCKED`. |
| S05 | `lifecycle-body` | error | A `NOT-STARTED`/`BLOCKED` section emits its heading and lifecycle block **only** (no placeholders, no ID records, no table rows, no prose); an `ACTIVE`/`COMPLETE` section must emit at least one field beyond `section_status`/`status_reason`. Section 0 is a special case: its whole control block is one fenced YAML block, so all twelve `REQUIRED` control fields (`section_status`, `status_reason`, `dossier_id`, `dossier_schema_version`, `date`, `evidence_cutoff`, `entry_mode`, `current_phase`, `task`, `data_regime`, `evaluation_target`, `scope_exclusions`) must be present and non-blank. |
| S06 | `id-namespaces` | error | Every `AAA-123` token uses one of `DOS, NEED, CLM, FAIL, LINK, RIV, INV, CAND, FIND, SYS, COMP, EXP`. A small documented list of external identifier prefixes (`GPT`, `CIFAR`, `PEMS`, …) is ignored so real-world dataset names do not trip the check. |
| S07 | `novelty-numeric` | error | No numeric novelty score and no aggregate gate score (`novelty: 8/10`, `novelty score 0.8`, `aggregate gate score: 7`). SKILL.md: "Do not emit numeric novelty or aggregate gate scores." A negation guard keeps phrases like "does not assign a novelty score" from firing, and overlapping spans are reported once. |
| S08 | `decision-enum` | error | When section 16 is `ACTIVE`/`COMPLETE` it contains **exactly one** `decision:` field, valued `GO \| PIVOT \| NEED-EVIDENCE \| KILL`. |
| S09 | `decision-consistency` | error | Same condition: `decision_consistency_check: PASS` is declared (template: "Require `decision_consistency_check: PASS`"). |
| S10 | `gate-table` | error | Section 15 enumerates **G0–G11** with a valid `Evaluation status`, `State` and `Failure mode` per gate; a gate may not carry a failure mode unless it is `UNSATISFIED`; an `UNSATISFIED` gate must name `REPAIRABLE` or `CONTRADICTED`; a `DEFERRED` gate must be `UNRESOLVED`. |
| S11 | `evidence-levels` | error | Every `E`-level token is inside the template's scale, `E0`–`E5`. |
| S12 | `claim-ledger-typing` | error | When section 3 is entered, every `CLM-*` ledger row carries a `Claim type` from `OBSERVATION \| EXPLANATION \| MECHANISM \| HYPOTHESIS \| ASSUMPTION \| EVIDENCE` and a `Status` from `SUPPORTED \| CONTRADICTED \| UNRESOLVED \| NOT-APPLICABLE`. |
| S13 | `phase-gating` | error | If `current_phase: DIAGNOSIS`, sections 8–12 and 14–16 must be `NOT-STARTED`. Section 13 is exempt — see §4. |
| S14 | `plans-vs-evidence` | warning | A `SUPPORTED` `CLM-*` row may not rest on a plan: a `PENDING` source record, or a cited `EXP-*` that is missing from section 13, not `COMPLETED`, or still `PENDING`. SKILL.md: "Treat planned or running experiments as plans, never as supporting evidence." |
| S15 | `traceability` | warning | An ID referenced in sections 14–16 must be *defined* in sections 0–13 — either as the first cell of a record row, or as the value of a singleton `*_id` field (`dossier_id`, `need_id`, `failure_id`, `invariant_id`). Gate ids (`G0`…) are excluded because section 15 defines them itself. |
| S16 | `phase-section-consistency` | warning | *(extension)* Later sections stay `NOT-STARTED` until their phase is entered (`DIAGNOSIS` → 7, `INDEPENDENT-IDEATION` → 8–16, `AUDIT` → 14–16). Complements S13, which only covers `DIAGNOSIS`. |
| S17 | `decision-gate-agreement` | warning | *(extension)* The compiled decision must follow the section 15 gate arithmetic: contradiction → `KILL`, repairable failure → `PIVOT`, unresolved gate → `NEED-EVIDENCE`, all satisfied → `GO` (which additionally requires novelty `PASS` in section 10). `decision_rule_triggered` and the `unresolved/repairable/contradicted_gate_ids` lists must agree with the table. This is what makes declared `decision_consistency_check: PASS` (S09) mean something. |
| S18 | `coverage-gate` | error | *(dossier schema 1.1.0)* Section 13's coverage block must exist and be internally derived: `coverage_complete: YES` iff `uncovered_core_claim_ids` names no CORE claim, `NO` otherwise. When it reports `NO`: gate `G11` must not be `SATISFIED` (it is `EVALUATED` and `UNRESOLVED`, never `UNSATISFIED` either), no `decision:` field in section 16 may be `GO`, and `smallest_next_action` must name at least one uncovered CORE claim. Template section 13 note and SKILL.md Stage 11. |

### Machine-readable output

`--json` returns the same report for every mode:

```json
{
  "grader_version": "1.0.0",
  "path": "evals/fixtures/bad-dossier.md",
  "skill": "time-series-model-ideation",
  "ok": false,
  "error_count": 30,
  "warning_count": 5,
  "checks": [
    {"check_id": "S01", "title": "sections-present", "severity": "error",
     "applicable": true, "status": "fail", "note": "16/17 canonical sections present",
     "findings": [{"check_id": "S01", "severity": "error", "message": "…", "line": null, "section": 12}]}
  ]
}
```

`status` is one of `pass`, `fail` (error findings), `warn` (warning findings) or
`skip` (the check does not apply at this lifecycle state, e.g. S10 when section 15
is `NOT-STARTED`). A `skip` never fails the grade.

---

## 3. Fixtures

`evals/fixtures/good-dossier.md` and `evals/fixtures/bad-dossier.md` are both
**synthetic**: invented prose, no real research claims, no real citations, no
real measurements. They exist to pin the grader's behaviour in both directions.

* `good-dossier.md` — generated from the shipped template by resolving every
  `{{REQUIRED: A | B | C}}` to its first alternative and filling the remaining
  fields with sample prose. It declares `dossier_schema_version: "1.1.0"` and
  full falsification coverage (`uncovered_core_claim_ids` N/A,
  `coverage_complete: YES`). Its lifecycle is coherent for a dossier that entered
  `COMPILATION` early: sections 0–6, 13, 14, 15, 16 are `COMPLETE`, sections
  7–12 are `NOT-STARTED`, `current_phase: COMPILATION`, and the decision is
  `NEED-EVIDENCE` with G0/G1 satisfied, G2–G4 evaluated-but-unresolved and
  G5–G11 deferred. It must produce **zero errors and zero warnings**.
* `bad-dossier.md` — the same dossier with the defects listed in the HTML
  comment at the top of the file. Each line has the form

  ```text
  DEFECT: <check id> :: <what was broken>
  ```

  `--self-test` parses those lines and fails if any listed check does not fire.

`make_fixtures.py` walks the template: section order and titles, field names,
table columns and enum alternatives all come from the template, and only values
come from its `CONTENT` table. If the template grows a field in a materialised
section, generation fails loudly with the field name instead of silently
drifting. `--check` compares the checked-in `.md` files against a fresh
generation so CI can detect a template change that was not regenerated.

Current defect coverage (16 documented defects): S01–S15 and S18 all fire on
`bad-dossier.md`; S18 trips on `coverage_complete: NO` with `G11` `SATISFIED`, a
`GO` decision, and an uncovered CORE claim that the smallest next action never
names. S17 also fires there as a warning (the same broken decision block); S16
does not, because at `DIAGNOSIS` phase its rule for sections 8–16 is already
carried by the S13 error, and section 7 is left `NOT-STARTED` by the fixture.

---

## 4. Deliberate deviations from the task brief

The brief for this harness said the template is the authority and that any
conflict must be recorded here. Five conflicts were found, plus four further
decisions — three added checks or required fields and one whitelist relaxation —
which are recorded in the same table.

| # | Brief said | Template / SKILL.md says | What the grader does |
|---|---|---|---|
| 1 | S10: gates **G0–G12** | Section 15 defines exactly **G0–G11** (12 rows), and every eval expectation speaks of "G0 through G11" | Requires G0–G11. A stray `G12` row is not an error, it is simply not required. |
| 2 | S11: evidence levels in **E0–E4** | Template: `Evidence strength = E0 \| E1 \| E2 \| E3 \| E4 \| E5` (`E5 = REPLICATED-ROBUST`) | Accepts E0–E5 and rejects `E6`+. Rejecting `E5` would fail dossiers that use the top level the template defines. |
| 3 | S12: status from `SUPPORTED \| UNRESOLVED \| CONTRADICTED`, "extend only if the template names more" | Template: `Status = SUPPORTED \| CONTRADICTED \| UNRESOLVED \| NOT-APPLICABLE` | Accepts all four. |
| 4 | S13: `DIAGNOSIS` ⇒ sections **8–16** `NOT-STARTED` | Section 13's own note: "Preserve diagnostic `EXP-*` IDs created during **Stages 2–4**" — Stages 2–4 are inside `DIAGNOSIS`, and the eval expectations for case 1 require a recorded diagnostic `EXP-*` with expected/falsifying outcomes | Gates 8–12 and 14–16 as errors; **section 13 is exempt** when the phase is `DIAGNOSIS` and the exemption is stated in the check note. Gating 13 would fail the skill's own canonical `NEED-EVIDENCE` dossier. Section 7 is covered by the S16 warning instead, because SKILL.md places it in `INDEPENDENT-IDEATION`. |
| 5 | S07: "no numeric novelty score or aggregate gate score" | SKILL.md forbids them; template requires a non-numeric novelty status | Implemented with a negation guard ("no numeric novelty score is reported" is compliant) and with contained-span de-duplication, so one phrase yields one finding. |
| +1 | — | — | **S16** and **S17** were added as *warning*-severity extensions because S13 alone cannot see an `AUDIT`- or `INDEPENDENT-IDEATION`-phase dossier entering later sections early, and because a declared `decision_consistency_check: PASS` is worth cross-checking against the gate table it claims to follow. Both are documented above and neither can fail a grade. |
| +2 | S06 namespace whitelist | — | A documented ignore-list of external identifier prefixes (`GPT`, `LLM`, `CIFAR`, `IMAGENET`, `PEMS`, `METR`, `SMD`, `SWAT`, `WADI`, `TSB`, `ETT`, `M3`–`M5`, `NN5`, `ILI`, `LOSLOOP`, `MIMIC`) keeps real dataset names from being read as invented dossier namespaces. |
| +3 | "enforce the new gate rule … decide whether this belongs as an extension of S10 or as a new error-severity check `S18 coverage-gate`" | Template section 13 note and SKILL.md Stage 11 (dossier schema 1.1.0): `coverage_complete: NO` leaves G11 `EVALUATED`/`UNRESOLVED`, caps the decision at `NEED-EVIDENCE`, and requires each uncovered CORE claim to be named as the smallest next action | **New check `S18 coverage-gate`, error severity.** S10 validates the shape of one gate row (enum values, `failure_mode` vs `state`); the coverage rule is a cross-section derivation — section 13 coverage fields → G11 state → section 16 decision → smallest next action — so folding it into S10 would make the gate-table check fire when the table itself is well formed and would blur what each id means. S18 also covers the schema-1.1.0 requirement that the coverage block exists and that `coverage_complete` is derived from the three coverage fields (`YES` iff nothing is uncovered). |
| +4 | "S05 section-0 required keys … must now include `dossier_schema_version`" | Template section 0 marks twelve control fields `REQUIRED` and the header comment states the current schema version is 1.1.0, with pre-1.1.0 dossiers implicitly 1.0.0 | Section 0 must carry all twelve keys, `dossier_schema_version` included. Consequence worth stating plainly: a legacy 1.0.0 dossier that omits the field now fails S05 even though the template says such a dossier is *implicitly* 1.0.0 — the field is `REQUIRED` in the current template, and the implicit-version note tells a reader how to interpret an old dossier, not how to satisfy the current schema. |

---

## 5. Adding a check

1. Write a function in `evals/graders/structural.py` that takes a `Dossier` and
   returns a `CheckOutcome(applicable, note, findings)`. Build findings with
   `Finding(check_id, severity, message, line=None, section=None)`.
2. Register it in the `CHECKS` tuple, in numeric order, with a **stable id**.
   Ids are never reused or renumbered: they appear in fixture defect lines,
   self-test output and downstream CI logs. To amend a rule, change the body of
   the existing check; to add a rule, take the next free id.
3. Decide the lifecycle condition explicitly. If the check only makes sense once
   a section is entered, return `CheckOutcome(False, "<reason>", [])` so the
   report shows `SKIP` rather than a vacuous `PASS`.
4. If it is an `error` check, make `bad-dossier.md` trip it: add a `Defect(...)`
   entry to `DEFECTS` in `evals/fixtures/make_fixtures.py` together with an
   injection function, regenerate the fixtures, and add a row to the table in §2.
   `--self-test` fails if a documented defect does not fire.
5. Prove the positive direction too: make sure `good-dossier.md` still yields
   zero errors and zero warnings. If the new check cannot pass there, extend the
   fixture content in the generator's `CONTENT` table rather than weakening the
   check.
6. Run: `python3 evals/fixtures/make_fixtures.py && python3 evals/run.py --self-test`.

Determinism rules for new checks: no clock, no randomness, no environment
reads, no network, and stable ordering of findings (sort by line, then by the
order in which they were derived).

---

## 6. Adding a behavioural case

Cases live with the skill, not with the harness:
`skills/time-series-model-ideation/evals/evals.json`. Each entry has

```json
{
  "id": 13,
  "prompt": "Mode: GENERATE. …",
  "expected_output": "one-paragraph description of the required artefact",
  "files": ["evals/files/some-attached-fixture.md"],
  "expectations": ["eight or nine independently judgeable statements"]
}
```

* `files` are resolved **relative to the skill root**
  (`skills/<skill>/`), so `evals/files/x.md` means
  `skills/time-series-model-ideation/evals/files/x.md`.
* Keep `id` unique and stable — `--case N` selects by it and Tier-2 reports key
  off it. Do not renumber existing cases; append new ones.
* `--list` (and `--list --json`) picks the new case up with no code change.
* Adding a case adds two Tier-2 model calls to a full run; see §7 for cost.

---

## 7. Tier-2: what it does and what it costs

```bash
python3 evals/run.py --tier2 --case 1                       # one case
python3 evals/run.py --tier2                                # all 12 cases
python3 evals/run.py --tier2 --provider openai --model gpt-4o-mini --judge-model gpt-4o-mini
python3 evals/run.py --tier2 --out evals/results/
python3 evals/run.py --tier2 --no-skill-context             # bare model, no SKILL.md/template
```

How it works, per case, using only `urllib.request`:

1. **Generation call.** The case prompt is sent together with `SKILL.md` and
   `assets/idea-dossier-template.md` (skip with `--no-skill-context`) plus the
   case's attached fixture files. The model must return one dossier.
2. **Judgement call.** A strict judge prompt receives the original prompt, the
   `expected_output` summary, the numbered expectations and the produced
   dossier, and must return JSON verdicts with quoted evidence. Unparseable
   judge output is recorded as `UNJUDGED` rather than crashing the run.

Wiring and keys:

* Providers: `anthropic` (`/v1/messages`, `x-api-key`), `openai` and `deepseek`
  (OpenAI-compatible `/chat/completions`, `Authorization: Bearer`). With no
  `--provider`, the first provider whose key is present wins.
* Keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`.
* Base URLs: `ANTHROPIC_BASE_URL`, `OPENAI_BASE_URL`, `DEEPSEEK_BASE_URL`. A
  bare host is completed with `/v1`, so both `https://api.openai.com/v1` and
  `http://localhost:8000` work. This also makes a local mock server usable for
  testing the harness itself.
* Models: `--model` / `--judge-model`, else `ANTHROPIC_MODEL` / `OPENAI_MODEL` /
  `DEEPSEEK_MODEL`, else the documented default in `PROVIDER_SPECS`. If a
  provider renames its models, pass `--model` explicitly.
* **No key** ⇒ `skipped: no API key — tier-2 not run` and exit `0`. It never
  crashes and never hangs: every request has `--timeout` (default 180 s), and an
  upstream error is recorded per case, written into the report, and returns
  exit `1` after the report is written.
* The Markdown report (run date, provider, generator and judge model, token cap,
  base URL, a failed-expectation index, then per case: prompt, expectations with
  PASS/FAIL and reasons, produced output, run errors) is written to
  `evals/results/` by default, or to `--out PATH` (a file, or a directory if the
  path looks like one). The default file name is
  `<date>-<provider>-<model>.md` with the model name sanitised for the
  filesystem, and a `-2`, `-3`, … suffix is added rather than overwriting an
  earlier run — see `evals/results/README.md` for the reporting rules.
  `--json` prints the same result as JSON.

Cost: **two model calls per case**, so a full 12-case run is 24 calls. The
generation call carries `SKILL.md` plus the 470-line template as input (roughly
9–10k input tokens with the attached fixtures) and may emit a full dossier; the
judgement call carries that dossier back plus the expectations. Expect roughly
**20–35k input and 4–10k output tokens per case** (≈ 300–500k input tokens for
all twelve), with wide variance from dossier length and judge verbosity. Check
current provider pricing before running the full suite; `--case 1` is the cheap
smoke test. Results are non-deterministic and judge verdicts are model
judgements, not ground truth — treat them as evidence about behaviour, not as a
certificate.

---

## 8. Limitations — what this harness cannot tell you

This section is the honest part, and the reason the two tiers are separate.

* **Tier-1 grades shape, not sense.** It can prove that a dossier is canonically
  structured, typed, phase-consistent, traceable and free of numeric novelty
  scoring. It cannot prove that the need is genuinely solution-independent, that
  the rivals are plausible, that the alleged failure is real, that the invariant
  is task-relevant, that the novelty search covered the right sources, or that
  the gate reasoning is honest. A well-formed, scientifically empty dossier
  passes Tier-1 — `evals/fixtures/good-dossier.md` is exactly that: it scores
  18/18 while containing no research contribution whatsoever.
* **Well-typed evidence can still be fabricated.** S12 checks that a claim is
  *labelled* `OBSERVATION` or `EVIDENCE` with a legal status; it cannot check
  that the measurement happened. Only Tier-2 and human review can notice.
* **S14 and S15 are warnings, not proofs.** They catch the cheap form of
  plans-as-evidence (a `SUPPORTED` row pointing at a `PENDING` experiment) and
  fabricated IDs in the compiled sections. A dossier that carefully keeps its
  unsupported claims `UNRESOLVED` is not thereby correct.
* **S17 checks arithmetic, not judgement.** It verifies that the decision
  follows the states in the gate table; it cannot tell whether the states were
  assigned honestly.
* **S18 checks the coverage/gate contract, not the coverage itself.** It proves
  that `coverage_complete: NO` cannot coexist with a satisfied G11, a `GO`
  decision or an unnamed uncovered CORE claim, and that the flag is derived from
  the three coverage fields. It cannot tell whether the `EXP-*` row that
  "covers" a CORE claim is a plausible falsifier — a dossier can mark every claim
  covered with a worthless experiment and still pass.
* **S10 checks the shape of a gate row, not the blocker behind it.** It does not
  judge whether the named blocking item is the right one, nor whether a gate
  marked `SATISFIED` deserved to be.
* **Field-level completeness is audited in two places only.** Section 0's twelve
  control keys (S05) and section 13's coverage block (S18) must be present and
  non-blank; a missing field anywhere else inside an entered section is not
  detected, because the template's other `REQUIRED` marks are not audited
  field-by-field.
* **No source verification.** Nothing here fetches a paper, resolves a citation,
  or checks that a quoted source exists. Tier-1 is offline by design.
* **No semantic deduplication or contradiction analysis.** Two structurally
  identical claims with opposite meanings both pass.
* **Tier-2 is not reproducible.** Same case, same model, different day — often a
  different verdict. It is a sampling tool for expectations that only a reader
  (or a judge model) can evaluate, and its verdicts should be spot-checked
  against the produced output, which the report includes for exactly that
  reason.

In short: Tier-1 tells you the dossier obeys its own evidence discipline
mechanically; it cannot tell you the research idea is any good.
