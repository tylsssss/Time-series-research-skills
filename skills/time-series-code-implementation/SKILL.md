---
name: time-series-code-implementation
description: Implement complete, runnable time-series research code from a verbal idea or a frozen method spec, researching GitHub time-series libraries for reference implementations first. Use whenever a user describes a time-series research idea (forecasting, classification, anomaly detection, imputation, representation learning) and wants working code — "implement this idea", "turn this idea into code", "根据思路完成代码", "照着这个思路写代码" — or wants to reproduce or adapt a method from a time-series library such as TSLib, darts, GluonTS, tsai, sktime, or Nixtla. Do not use for idea-level analysis and auditing (use time-series-model-ideation instead) or for general non-time-series coding.
---

# Time-Series Code Implementation

## Role and Boundary

Turn one frozen method into complete, runnable research code, using GitHub time-series libraries as the primary reference source. This skill is the downstream partner of `time-series-model-ideation`: that skill decides *whether* an idea is worth building and freezes the method; this skill builds it.

Accept input as either:

- a verbal idea described in conversation (the common case), or
- a frozen Idea Dossier or method spec produced by `time-series-model-ideation`.

Deliver: a working codebase, verification runs, and an honest results summary. Stop at research-code level — no paper prose, no polished publication figures.

## Personal Style Contract

All generated code must follow the personal style in `references/personal-code-style.md` (load it before Phase 2; it stays authoritative through delivery). The core contract:

1. **Code logic is one whole.** Write each phase of logic — a search loop, a training step, a ranking procedure — as one continuous narrative in one method. Extract a helper only for genuinely functional utilities: serialization and format conversion (e.g. JSON), I/O, or resource loading. Never extract a fragment just to shorten a method.
2. **One line over many.** Prefer single-line expressions: ternaries, comprehensions, chained tensor ops, `lambda` sorts, inline set-based dedup. Do not introduce intermediate variables or wrapper methods that a one-liner expresses as readably.
3. **Guards belong at seams, not in the flow.** Reserve `if + raise` for true boundaries: the entry boundary, construction-time invariants, external library contracts, dispatch defaults, and genuine dead-ends. Scattered defensive checks inside a flow signal wrong logic — fix the logic, and comment the invariant the flow already guarantees instead of re-checking it.
4. **Shape and intent comments.** Annotate every tensor-shape transformation inline (`# [B, L, C] -> [B, C, L]`); every other comment explains why, never restates the code.
5. **Config as data, logic as flow.** Declare search spaces, action lists, and constants as plain data at module top; dispatch over data, not if-chains.

These rules override generic conventions wherever they conflict.

## Workflow

### Phase 0 — Freeze the spec before writing code

Extract from the conversation:

- **Task**: forecasting, classification, anomaly detection, imputation, representation, or regression.
- **Data**: univariate/multivariate, frequency, history length, forecast horizon, sample count, source.
- **Method** (the frozen part): architecture, objective, training scheme, and the key design choice the user's idea centers on.
- **Evaluation**: datasets, baselines, primary metric, number of seeds.
- **Constraints**: compute budget, wall time, framework preferences, environment.

Ask clarifying questions in one batched message, ordered by what changes the architecture. Do not run the full `time-series-model-ideation` workflow here — that is for idea-level uncertainty. If the method itself is genuinely unsettled (unknown architecture, unclear mechanism, unresolved feasibility), say so and offer a lightweight frozen-spec check or a handoff to `time-series-model-ideation`.

Emit a frozen SPEC block and get explicit confirmation before coding:

```text
TASK:     forecasting | classification | anomaly | imputation | ...
DATA:     univariate/multivariate, frequency, history, horizon, size, source
METHOD:   architecture, objective, training scheme (frozen)
EVAL:     datasets, baselines, primary metric, seeds
CONSTRAINTS: compute, wall time, dependencies, environment
```

### Phase 1 — Research reference implementations before designing

1. Read `references/library-landscape.md` to map the task to candidate libraries.
2. Use web_search and GitHub search to locate the concrete repositories and the exact model and trainer files.
3. Fetch and read the actual source code — model files, data loaders, and experiment scripts — not just the README. Papers and READMEs omit normalization and windowing details that source code reveals, and those details are where reproductions usually fail.
4. Record provenance for everything consulted: repo URL, commit hash, file paths, license.
5. Choose one reuse strategy per component:
   - **dependency** — import the library as-is (preferred when its public API covers the need);
   - **borrow** — copy or adapt reference code into the project under an attribution header (source URL, commit, what changed and why);
   - **reimplement** — write from scratch, informed by the reference.

Prefer dependency, then borrow. Avoid reimplementing what a maintained library already provides. For unlicensed research repos, read for understanding only — treat the code as a specification, not a source to copy.

### Phase 2 — Design before typing

- Read `references/research-code-conventions.md` and follow it throughout implementation (seeds, config, logging, leakage-safe splits, checkpoints).
- Read `references/personal-code-style.md`; it is authoritative over generic conventions wherever they conflict. The style contract binds every line written in Phases 3–4.
- Decide **reproduce vs. extend** explicitly: is the goal an exact reproduction of a published or library result, or an adaptation to the user's task? This choice changes evaluation and what "done" means.
- Lay out a standard research layout: config → data pipeline → model → trainer → evaluation → one entry point. Keep files small enough to review, but keep each phase's logic whole inside its method (see the style contract).

### Phase 3 — Implement: thin end-to-end slice first

- Start from `assets/project-template.md`: copy its starter files (run.py, exp, model, data loader, metrics) into the project and fill the `{{...}}` marks. The template encodes the file-level style once, so every project starts from the same shape. When borrowing a library's layout, keep the library's structure and apply the style to the code you add.
- Build a minimal skeleton that runs end to end on tiny synthetic data (data → model → one train step → eval) and get it green before adding the real method.
- Write in the personal style from the first line: linear narratives, one-liners, boundary-only guards, shape comments (see the style contract). Retrofitting style after the logic works is harder than writing it correctly once.
- Add the frozen method component by component, borrowing code with provenance headers.
- Track components with a todo list; keep every step reviewable and runnable.

### Phase 4 — Verify; do not assume correctness

Run these checks in order, and fix problems as they appear:

1. **Smoke test**: tiny synthetic run — tensor shapes correct, loss decreases, no NaN/Inf.
2. **Overfit test**: the model should fit a single small batch or a near-trivial series quickly; if it cannot, something is structurally broken.
3. **Baseline sanity**: on real data the method should at least be comparable to a trivial baseline (persistence, global mean, linear model). A result far below trivial usually means a pipeline bug, not a bad idea.
4. **Reference comparison**: when reproducing, compare against the library's published numbers. Small gaps are expected; large gaps demand an explanation in the report.
5. **Real run**: execute the agreed experiment plan with the agreed seeds and report dataset × method × metric ± std.

### Phase 5 — Deliver and hand back

Structure the report exactly per `assets/report-template.md` (sole authority for its headings and order). Report in chat:

- what was built and how to run it (exact commands),
- verification status for every check in Phase 4,
- provenance of borrowed code (repo, commit, license),
- results table with mean ± std and baseline comparisons,
- any deviations from the frozen SPEC and why they happened.

If results contradict the original idea, say so plainly. Do not hide negative results or quietly change the method to make numbers look better.

## Reference Router

- Phase 1: `references/library-landscape.md`
- Phases 2–4: `references/personal-code-style.md` (authoritative for all written code)
- Phases 2–4: `references/research-code-conventions.md`
- Phase 3: `assets/project-template.md` (project scaffold and starter files)
- Phase 5: `assets/report-template.md` (delivery report structure)

Load only what the current phase needs. Where generic conventions conflict with the personal style, the personal style wins.

## Anti-Patterns

- Do not write code before the method is frozen and confirmed.
- Do not copy GitHub code without an attribution header and license check.
- Do not treat README benchmark tables as results you reproduced — rerun them.
- Do not add abstractions or scale up before the thin slice and smoke test pass.
- Do not silently change the frozen method when implementation gets hard; propose the change and get confirmation first.
- Do not claim results you did not run, and do not smooth over poor results.
- Do not average metrics across heterogeneous datasets; report per dataset.
- Do not fragment one coherent phase of logic into many small private methods just to shorten methods.
- Do not sprinkle defensive `if + raise` checks through the logic flow; place them only at true boundaries and comment the invariants the flow already guarantees.
- Do not stretch a one-liner into multiple statements, or invent wrapper methods around single calls.
