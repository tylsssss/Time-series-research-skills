# Integration Evidence Packet

This synthetic, source-validated fixture tests end-to-end research-argument compilation. It is not a real-world novelty claim and must not be reused as literature evidence outside this eval. Treat its measurements and source comparisons as independently verified input artifacts. No gate state, novelty status, candidate selection, or final decision is supplied; derive them from the records below.

## Research boundary

- Mode: `AUDIT`
- Task: causal early deterioration forecasting from irregularly sampled multivariate clinical histories
- Deployment: historical observations and timestamps only; no future covariates; one 24 GB GPU
- Evaluation target: calibrated horizon-specific risk plus sensitivity to controlled elapsed-time interventions
- Evidence cutoff: `2026-06-30`
- Claim boundary: no universal missing-data robustness, causal-discovery, or out-of-regime superiority claim

## Typed evidence records

- `CLM-001` — `OBSERVATION`, `CORE`, `DIRECT-MEASUREMENT`, `E5`, `SUPPORTED`: with values and masks matched, the inherited equal-step update gives stale observations the same retained-state influence as recent observations across three datasets and five seeds.
- `CLM-002` — `MECHANISM`, `CORE`, `INFERENCE`, `E4`, `SUPPORTED`: elapsed-time insensitivity causes stale-state persistence that changes calibrated early-risk predictions.
- `CLM-003` — `EVIDENCE`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: varying only elapsed gaps changes the oracle time-aware state and target risk; capacity-, value-, and length-matched controls do not reproduce the effect.
- `CLM-004` — `EVIDENCE`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: selectively enforcing monotone forgetting changes the predicted stale-state intermediate and improves calibration on affected horizons without changing information access.
- `CLM-005` — `HYPOTHESIS`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: under value- and mask-matched gap interventions, the constrained candidate will satisfy the monotonicity tolerance and its calibration change will track the corrected stale-state diagnostic.
- `CLM-006` — `MECHANISM`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: under the stated operator assumptions, retained-state influence is bounded and nonincreasing as elapsed time grows.
- `CLM-007` — `ASSUMPTION`, `SUPPORTING`, `DIRECT-MEASUREMENT`, `E3`, `SUPPORTED`: elapsed gaps are nonnegative and observed at both training and inference in the audited regime.
- `CLM-008` — `ASSUMPTION`, `SUPPORTING`, `INFERENCE`, `E3`, `SUPPORTED`: the parameterization of `g` is nonnegative and monotone over the bounded deployment gap range.
- `CLM-009` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: additional parameter count alone explains the gap-sensitive effect.
- `CLM-010` — `HYPOTHESIS`, `SUPPORTING`, `INFERENCE`, `E1`, `SUPPORTED`: if capacity is sufficient, a capacity-matched gap-insensitive update should reproduce the intervention response; it does not.
- `CLM-011` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: interpolation density alone explains stale-state persistence.
- `CLM-012` — `HYPOTHESIS`, `SUPPORTING`, `INFERENCE`, `E1`, `SUPPORTED`: if interpolation density is sufficient, varying density at fixed values, masks, and gaps should remove the effect; it does not.
- `CLM-013` — `EVIDENCE`, `SUPPORTING`, `DIRECT-MEASUREMENT`, `E5`, `SUPPORTED`: the diagnostic and intervention directions replicate across the stated datasets, seeds, gap bins, and sensor subsets.

## Failure, causal links, rivals, and invariant

- `FAIL-001`: the equal-step state transition is insensitive to elapsed time under irregular sampling; direct measurement is retained-state influence under value- and mask-matched gap pairs.
- `LINK-001`: `CLM-001` -> stale-state persistence in `CLM-002`.
- `LINK-002`: `CLM-002` -> calibrated horizon-risk change supported by `CLM-003`.
- `RIV-001`: explanation `CLM-009`; shared prediction is that a larger update can change risk; discriminating prediction `CLM-010`; experiment `EXP-002`; status `REJECTED` by the completed control.
- `RIV-002`: explanation `CLM-011`; shared prediction is that denser representations can change stale-state behavior; discriminating prediction `CLM-012`; experiment `EXP-003`; status `REJECTED` by the completed control.
- `INV-001`: stable causal monotone forgetting. With values and masks fixed, increasing an elapsed gap must not increase retained influence of the older state. Tolerance is `1e-4` on intervention pairs. Persistent latent conditions are the named harmful boundary.

## Completed diagnostic experiments

- `EXP-001` — subject `FAIL-001`; claims `CLM-001, CLM-002`; intervention: compare equal-step retained influence across value- and mask-matched pairs differing only in elapsed gap; status `COMPLETED`; expected under failure: no influence decrease; falsifier: influence already decreases with gap; observed: mean absolute influence difference remains below `2e-5` across gap bins; source `measurement-log-D1`; rivals `CLM-009, CLM-011`; ablation: replace timestamps with a constant; fairest baseline: inherited equal-step update; cannot prove candidate efficacy or novelty; a null result would revisit Stage 2.
- `EXP-002` — subject `FAIL-001`; claims `CLM-003, CLM-009, CLM-010`; intervention: vary elapsed gaps only and compare an oracle time-aware update with a capacity-matched gap-insensitive update; status `COMPLETED`; expected: only the oracle changes stale-state influence and affected-horizon calibration; falsifier: capacity-matched control reproduces both; observed: oracle changes both while the control does not; source `intervention-log-D2`; rival `CLM-009`; ablation: remove gap input; fairest baseline: equal-parameter gap-insensitive update; cannot prove the proposed candidate is necessary; a falsifier would revisit Stage 3.
- `EXP-003` — subject `FAIL-001`; claims `CLM-003, CLM-011, CLM-012`; intervention: vary interpolation density while holding observed values, masks, and elapsed gaps fixed; status `COMPLETED`; expected: density alone does not remove stale-state persistence; falsifier: density removes the diagnostic and task effect; observed: direction and magnitude remain within the preregistered equivalence margin; source `control-log-D3`; rival `CLM-011`; ablation: three interpolation densities; fairest baseline: matched interpolation pipeline; cannot prove arbitrary-sampling robustness; a falsifier would revisit Stage 3.
- `EXP-004` — subject `FAIL-001`; claims `CLM-004, CLM-013`; intervention: selectively enforce the invariant in an oracle state update across datasets, seeds, gap bins, and sensor subsets; status `COMPLETED`; expected: invariant violations fall and affected-horizon calibration changes; falsifier: diagnostic changes without the predicted task behavior; observed: violations fall below tolerance and calibration changes in the predicted direction across the preregistered scope; source `replication-log-D4`; rivals `CLM-009, CLM-011`; ablation: invariant enforcement on/off; fairest baseline: matched unconstrained oracle; cannot prove benefit outside the scope or identify a deployable method; a falsifier would revisit Stage 4.

## Frozen candidate set and reference use

- `CAND-001` — `IN-DOMAIN`, `PRIMARY`: compute `a_t = exp(-g(delta_t))` with a monotone nonnegative time-gap network and update retained state using `a_t` plus a causal innovation from the current value and mask.
- `CAND-002` — `BASELINE`, `NULL-BASELINE`: retain the inherited equal-step update with no elapsed-gap input, under the same state size and downstream head.
- Both candidates address `LINK-001`; `CAND-001` also targets `LINK-002`; both are evaluated against `INV-001`; `CLM-005` is the distinguishing candidate prediction.
- The set was derived from `FAIL-001`, `LINK-001`, `LINK-002`, and `INV-001`, then frozen before reference use.
- Post-freeze pattern inspection found that monotone forgetting can be harmful when a persistent latent condition should remain influential. The claim was bounded to the diagnosed regime without changing the candidate set.

## Direct-use measurements and contracts for CAND-001

- Inputs are `X, M in R^(B x T x N)` and nonnegative elapsed gaps `Delta` of the same shape; state is `H in R^(B x N x d)`; output is `Y in R^(B x H_out x 1)`.
- `g` is differentiable and monotone with nonnegative parameters enforced by softplus; `a_t` is in `(0,1]`.
- Training and inference use the same historical values, masks, gaps, update, and reset rule; missingness is an input and no future value is imputed.
- Long-rollout, noise, mixed-variable, gap-range, and regime-boundary stress tests show no amplification, undefined state, identifiability failure, or unsupported information access inside the stated scope.
- A closed gradient path is observed in the dry run. Peak memory is 7.2 GB and measured latency is within the stated budget.
- The persistent-latent-condition boundary remains explicit; it bounds the claim rather than requiring a new component.

`CAND-002` is the null comparator and is not proposed as a non-null research mechanism.

## Bounded primary-source comparison facts

The dated audit searched time-gap conditioning, decay, irregular-time state updates, monotonic constraints, missingness handling, invariant preservation, and elapsed-gap interventions; it traversed backward and forward citations and negative-result terminology.

1. Che et al., *Recurrent Neural Networks for Multivariate Time Series with Missing Values* (GRU-D), Scientific Reports 2018, https://www.nature.com/articles/s41598-018-24271-9. The source uses learned decay for missing multivariate series. Its disclosed contribution does not define the fixture's intervention-measured monotone influence invariant or the associated gap-only distinguishing prediction.
2. Kidger et al., *Neural Controlled Differential Equations for Irregular Time Series*, NeurIPS 2020, https://arxiv.org/abs/2005.08926. The source models irregular series in continuous time. Its disclosed contribution does not use the fixture's constrained forgetting operator or value-and-mask-matched gap intervention.

Inherited elements are time-gap conditioning, decay, and irregular-time modeling. The smallest positive delta is to diagnose stale-state persistence, enforce the independently measured monotone forgetting invariant by construction, and predict a specific intermediate response under gap-only interventions. No reviewed bridge supplies that mechanism-plus-invariant-plus-prediction contract as a routine substitution. This is a positive comparison result within the dated boundary, not an absence-only argument.

## Feasibility measurements and contracts

- Forward update: `a_t = exp(-g(Delta_t))`; `H_t = a_t * H_(t-1) + phi(X_t, M_t)`; a causal head maps queried state to `Y`.
- `g`, `phi`, and the head are trainable; softplus parameterization enforces the sign constraint.
- Loss combines calibrated risk loss with a monotonicity-violation penalty on training-only paired interventions; inference needs no paired intervention.
- Shapes broadcast explicitly over `B x N x d`; resets, padding masks, and output constraints are defined.
- Complexity is `O(B*T*N*d)` time and `O(B*N*d)` recurrent state memory.
- A completed dry run records finite losses, nonzero finite gradients for every trainable group, legal outputs, identical train/inference information access, 7.2 GB peak memory, and budget-compliant latency in `execution-log-F1`.
- Minimum executable experiment is `EXP-005`; the fallback replaces `g` with a one-parameter monotone decay without changing the invariant contract.

## Theory derivation facts

- `CLM-006` is assessed for `CAND-001` under assumptions `CLM-007` and `CLM-008`.
- Because `g(delta) >= 0`, `exp(-g(delta))` lies in `(0,1]`; because `g` is nondecreasing, retained influence is nonincreasing in `delta`.
- The derivation establishes only bounded monotone retained influence in the audited gap range. It establishes no accuracy, calibration, causal-identification, arbitrary-missingness, or optimization guarantee.
- `CLM-005` is the empirical counterpart. No formal theorem is declared.

## Candidate-level falsification experiments

- `EXP-005` — subjects `CAND-001, CAND-002`; claims `CLM-005, CLM-006`; compare the constrained candidate, equal-step null, fixed exponential decay, and an unconstrained time-gap network under matched state size and compute; status `PLANNED`; expected: only the constrained candidate consistently satisfies the invariant and its calibration change tracks stale-state correction; falsifier: the constraint violates monotonicity, the intermediate does not change, or a fair simpler comparator matches all mechanism-specific behavior; observed result `PENDING`; source `PENDING`; rivals `CLM-009, CLM-011`; ablation: constraint and gap input; fairest baseline `CAND-002`; cannot prove novelty or out-of-regime utility; a falsifier revisits Stage 5.
- `EXP-006` — subject `CAND-001`; claims `CLM-005`; intervene only on elapsed gaps while fixing values and masks; status `PLANNED`; expected: retained influence changes monotonically before calibration; falsifier: no intermediate change or reversed order; observed result `PENDING`; source `PENDING`; rivals `CLM-009, CLM-011`; ablation: shuffle gaps; fairest baseline: unconstrained time-gap network; cannot prove broad accuracy; a falsifier rejects the mechanism claim.
- `EXP-007` — subject `CAND-001`; claims `CLM-005, CLM-006`; test persistent-latent-condition regimes; status `PLANNED`; expected: the named boundary can reduce utility despite valid monotonicity; falsifier for the bounded claim: unexplained failure inside the claimed regime; observed result `PENDING`; source `PENDING`; rivals `CLM-009, CLM-011`; ablation: persistence duration; fairest baseline: fixed decay; cannot prove safety outside tested regimes; failure narrows or rejects the candidate.

Derive the canonical dossier, gate rows, candidate status, and one final decision from these artifacts.
