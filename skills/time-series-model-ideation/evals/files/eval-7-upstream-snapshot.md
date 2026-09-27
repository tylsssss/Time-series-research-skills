# Eval 7 Upstream Dossier Snapshot

Preserve this supplied Stage-7 snapshot while auditing novelty. Values below fill the canonical Sections 0–9, diagnostic experiment records in Section 13, and G0–G7 rows in Section 15.

## Control and boundary

- `dossier_id`: `DOS-007`; date and evidence cutoff: `2026-06-30`; entry mode: `AUDIT`; current phase: `AUDIT`.
- Task: causal nowcasting of river discharge at a downstream gauge from upstream telemetry with variable reporting delays and later quality-control revisions; issue times every 6 hours; lead times 6 to 48 hours; no future covariates; 24 GB GPU.
- Evaluation target: nowcast error at the affected issue times under arrival-time interventions, reported separately from aggregate error.
- Intended contribution: arrival-time-conditioned causal encoding of telemetered series.
- Supplied evidence: `EXP-701`–`EXP-703`; unknowns: primary-source overlap only.
- Scope excludes implementation, paper prose, and claims outside the evaluated gauges, lead times, and delay regime.

## Need, claims, failure, rivals, and invariant

- `NEED-001`: keep nowcasts issued at operational deadlines usable when upstream readings arrive late, without consuming any value before its arrival timestamp. Method-names-removed check: `PASS`.
- `CLM-001` — `OBSERVATION`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: the shared encoder maps the same hydrologic state differently whenever arrival delays differ, and the affected issue times show inflated nowcast error.
- `CLM-002` — `MECHANISM`, `CORE`, `INFERENCE`, `E4`, `SUPPORTED`: an encoder that ignores arrival timing mixes readings that had not arrived at the issue time into the nowcast state.
- `CLM-003` — `EVIDENCE`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: changing only the arrival-time attribute changes nowcast error at the affected issue times before aggregate error.
- `CLM-004` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: added parameter count is sufficient.
- `CLM-005` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: the quality-control revision cycle alone is sufficient.
- `CLM-020` — `MECHANISM`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: `SYS-001` contributes arrival-time-conditioned causal encoding with an explicit unavailable state for readings that have not arrived.
- `CLM-021` — `HYPOTHESIS`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: interventions on `COMP-001` change nowcast error at the affected issue times before aggregate error.
- `FAIL-001`: an arrival-time-invariant encoder produces measurable issue-time-specific error inflation once reported arrival delays exceed one issue interval.
- `LINK-001`: arrival-time-invariant encoding -> mixing of not-yet-arrived readings; `LINK-002`: that mixing -> contaminated nowcast state at the issue time; `LINK-003`: contamination -> affected-issue-time error.
- `RIV-001`: `CLM-005`, discriminated by `EXP-703`, `REJECTED`; `RIV-002`: `CLM-004`, discriminated by `EXP-702`, `REJECTED`.
- `INV-001`: causal access preserved exactly, so no reading enters a nowcast before its arrival timestamp, with evaluation on the natural reporting-delay distribution; a bounded arrival lag is acceptable and unbounded revision-driven backfill is a harmful boundary.

## Candidates and freeze

- `CAND-001` — `SUPPLIED`, `IN-DOMAIN`, `PRIMARY`, `PROVISIONALLY-SELECTED`: condition the causal state on each series' arrival-time attribute and keep not-yet-arrived slots in an explicit unavailable state; addresses `LINK-001, LINK-002`; preserves `INV-001`; predicts `CLM-021`.
- `CAND-002` — `SUPPLIED`, `BASELINE`, `SIMPLE-BASELINE`, `ACTIVE`: last-observation-carried-forward with no arrival-time input; addresses no arrival-time link; prediction is that imputation alone will not change the affected-issue-time diagnostic.
- Candidate set was frozen from `FAIL-001`, `LINK-001`–`LINK-003`, and `INV-001` before pattern use.
- ICLR patterns were consulted after freeze to inspect information-flow and responsibility structure. Risk: the encoder and the unavailable-state handler could duplicate responsibility. Effect: `bounded`.
- Cross-domain transfer is structurally not applicable.

## Direct-use findings and adapted system

- `FIND-001` for `CAND-001` — `BROKEN-ASSUMPTION`, `ADAPT`: an arrival-time input alone changes the representation but has no owner for the not-yet-arrived state; evidence `CLM-003`.
- `FIND-002` for `CAND-002` — `NONE`, `NO-ADAPTATION-REQUIRED`: the baseline is executable but does not address `LINK-001`; evidence is its supplied interface dry run.
- `SYS-001` adapts `CAND-001` with `COMP-001` and `COMP-002` and repairs `FIND-001`.
- System input: per-series windows `B x C x T x d` with an arrival-time attribute `B x C x T`. Output: causal state `B x d` for the nowcast head.
- Connections: `COMP-001` encodes each series together with its arrival-time attribute; `COMP-002` replaces not-yet-arrived slots with a learned unavailable state; their outputs are concatenated before the causal head.
- Training: nowcast loss over historical issue times, with arrival timestamps replayed per issue time. Inference: the identical path, using only readings whose arrival timestamp precedes the issue time. State: no persistent cross-issue state; the unavailable mask is deterministic.
- `COMP-001`: primary responsibility is arrival-time-conditioned encoding; operation is an attribute-conditioned causal convolution; input/output is `B x C x T x (d + 1) -> B x C x T x d`; risk is overfitting the delay attribute; mitigation is delay-stratified validation; ablation `EXP-704`.
- `COMP-002`: primary responsibility is the explicit unavailable state; operation is a deterministic mask plus a learned embedding for masked slots; input/output preserves `B x C x T x d`; risk is acting as a generic capacity path; mitigation is a matched imputation control; ablation `EXP-705`.

## Stable diagnostic experiments

- `EXP-701` completed the arrival-time-stratified pre/post diagnostic supporting `CLM-001`; matched issue-time sampling; cannot prove candidate efficacy.
- `EXP-702` completed a parameter-matched control contradicting `CLM-004`; cannot prove novelty.
- `EXP-703` completed a revision-cycle control contradicting `CLM-005`; cannot prove system efficacy.
- `EXP-704` and `EXP-705` are planned candidate ablations with `PENDING` results and do not support ledger claims.

## Gate snapshot

G0 through G7 are `EVALUATED / SATISFIED / null` with their decisive IDs above. G8 through G11 are `DEFERRED / UNRESOLVED / null`; the blocker is unentered novelty and downstream audits. No final decision has been compiled.
