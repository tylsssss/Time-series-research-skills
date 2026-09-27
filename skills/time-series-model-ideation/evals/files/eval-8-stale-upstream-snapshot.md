# Eval 8 Stale Upstream Dossier Snapshot

This supplied snapshot records the dossier state before newly discovered feasibility and theory contradictions. Preserve its IDs and valid upstream evidence, but do not preserve stale gate conclusions when the new prompt contradicts them.

## Control and research basis

- `DOS-008`; mode `AUDIT`; evidence cutoff `2026-06-30`; task: causal multivariate forecasting with a regime-conditioned update-rule switch from regular histories; no future covariates; 24 GB GPU.
- Need `NEED-001`: apply the causal update rule whose effective receptive field matches the current regime under a fixed inference budget.
- `CLM-001` — `OBSERVATION`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: one fixed update rule underperforms in two diagnosed regimes with different receptive-field needs.
- `CLM-002` — `MECHANISM`, `CORE`, `INFERENCE`, `E4`, `SUPPORTED`: regime-insensitive switching applies a rule with an incompatible receptive field.
- `CLM-003` — `EVIDENCE`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: an oracle regime-conditioned switch changes the intermediate receptive-field diagnostic and forecast error under matched capacity.
- `CLM-004` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: parameter count alone explains the result.
- `CLM-005` — `HYPOTHESIS`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: a learned legal gate will reproduce the oracle's regime-conditioned diagnostic without future access.
- `CLM-040` — `MECHANISM`, `CORE`, `PRIMARY-LITERATURE`, `E1`, `UNRESOLVED`: `SYS-002` has globally stable state dynamics by inheritance from a fixed linear source operator.
- `CLM-041` — `ASSUMPTION`, `SUPPORTING`, `PRIMARY-LITERATURE`, `E1`, `UNRESOLVED`: the target operator is fixed and linear.
- `CLM-042` — `ASSUMPTION`, `SUPPORTING`, `PRIMARY-LITERATURE`, `E1`, `UNRESOLVED`: the source norm bound applies unchanged to every regime-conditioned update.
- `FAIL-001`: fixed update-rule selection yields a measurable receptive-field mismatch. Links `LINK-001` and `LINK-002` connect selection, mismatch, and task error.
- Rivals: capacity (`RIV-001`) and training budget (`RIV-002`), rejected by completed matched interventions `EXP-801` and `EXP-802`.
- `INV-001`: preserve causal access and the output contract while switching update rules.

## Frozen candidates and stale adaptation record

- `CAND-002` — `SUPPLIED`, `IN-DOMAIN`, `PRIMARY`, `PROVISIONALLY-SELECTED`: use a regime-conditioned hard top-1 switch between two shape-matched causal update rules, a fixed-step rule and a variable-step rule; addresses `LINK-001, LINK-002`; preserves `INV-001`; predicts `CLM-005`.
- `CAND-003` — `SUPPLIED`, `BASELINE`, `SIMPLE-BASELINE`, `ACTIVE`: fixed best-on-validation update rule under the same backbone and budget.
- The set was frozen before reference use. Pattern inspection found that the gate's decision responsibility must remain separate from temporal prediction; effect `bounded`.
- `FIND-001` for `CAND-002` — stale record: `BROKEN-ASSUMPTION / ADAPT`, claiming a dedicated gate is required to make legal discrete choices.
- `SYS-002` adapts `CAND-002` with `COMP-010` and claims to repair `FIND-001`.
- `COMP-010` primary responsibility: output one legal top-1 update-rule choice. Recorded operation: encode regime context, score the two candidate rules, take hard argmax. Recorded input/output: context vector -> one-hot choice. Recorded risk: collapse. Recorded mitigation: entropy monitoring. Ablation: `EXP-803`.
- Recorded system input/output: `X in R^(B x T x N)` -> `Y in R^(B x H x N)` through the selected causal update rule.
- Recorded training path: form a context embedding, choose one update rule, apply forecast loss. Recorded inference path: form an available context embedding, choose one update rule, run the same rule. The snapshot did not expose that the two embeddings differ.
- Recorded state and constraints: one-hot legal choice; both update rules share output shape.

## Completed novelty snapshot

- Novelty subject was `SYS-002` with `COMP-010`; declared contribution claim `CLM-006` states a regime-conditioned update-switch interface.
- A dated primary-source comparison covered same-problem switching, same-mechanism hard selection, same-axis interface structure, and negative collapse results. Its recorded positive delta was the diagnosed receptive-field contract plus a legal discrete switch; novelty status was `PASS` before the newly discovered subject-definition contradiction.
- The comparison and citations are stable, but any change to the actual gate input, update path, or constraint invalidates this frozen novelty subject and requires re-audit.

## Stable experiments and old gate snapshot

- `EXP-801` completed the oracle regime-choice diagnostic; `EXP-802` completed capacity and budget controls. Both have sourced observed results and non-guarantees.
- `EXP-803` is a planned gate ablation with `PENDING` results and supports no claim.
- Old Section 15 marked G0 through G8 `EVALUATED / SATISFIED / null`; G9 through G11 were `DEFERRED / UNRESOLVED / null`. The new audit must correct any row contradicted by newly disclosed information.
