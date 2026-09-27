# Primary-Source Comparison Fixture: TimeKAN

Use this fixture only for behavioral evaluation of the novelty-audit workflow. Treat the cited ICLR paper as the primary source for the technical facts below; do not generalize beyond them.

## Canonical upstream snapshot

Preserve this supplied Stage-7 subject while auditing novelty:

- `DOS-010`; mode `AUDIT`; evidence cutoff `2026-06-30`; task: causal long-horizon forecasting from regular multivariate histories; horizons 96–720; one 24 GB GPU.
- `NEED-001`: represent separable temporal frequency behavior under a fixed causal compute budget. The need is solution independent and does not imply KANs or a particular band count.
- `CLM-001` — `OBSERVATION`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: a single shared nonlinear map underfits controlled mixtures whose bands require different functional orders.
- `CLM-002` — `MECHANISM`, `CORE`, `INFERENCE`, `E4`, `SUPPORTED`: order-invariant representation creates band-specific approximation error.
- `CLM-003` — `EVIDENCE`, `CORE`, `DIRECT-MEASUREMENT`, `E4`, `SUPPORTED`: an oracle using band-specific function order changes the band error and forecast error under matched parameter count.
- `CLM-004` — `EXPLANATION`, `SUPPORTING`, `INFERENCE`, `E1`, `CONTRADICTED`: added capacity alone explains the result.
- `CLM-020` — `MECHANISM`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: the frozen candidate contributes a frequency-band Decomposition-Learning-Mixing architecture with order-specific KAN encoders.
- `CLM-021` — `HYPOTHESIS`, `CORE`, `INFERENCE`, `E1`, `UNRESOLVED`: band-order interventions should change band-specific approximation error before aggregate forecasting error.
- `FAIL-001`: shared-order representation produces measurable band-specific approximation error. `LINK-001` connects shared order to band error; `LINK-002` connects band error to task error.
- `RIV-001` uses explanation `CLM-004`, distinguishing prediction `CLM-005`, completed experiment `EXP-1002`, and status `REJECTED`. A second optimization-budget rival is recorded as `CLM-006` and rejected by `EXP-1003`.
- `INV-001`: preserve causal band identity and output alignment across decomposition and mixing; exact signal reconstruction is not claimed.
- `CAND-010` — `SUPPLIED`, `IN-DOMAIN`, `PRIMARY`, `PROVISIONALLY-SELECTED`: four learned frequency bands, order-specific KAN encoders, upsampling, and learned recombination; addresses `LINK-001, LINK-002`; preserves `INV-001`; contribution `CLM-020`; consequence `CLM-021`.
- `CAND-011` — `SUPPLIED`, `BASELINE`, `NULL-BASELINE`, `ACTIVE`: the inherited single shared nonlinear map with no band-specific order.
- The candidate set was frozen from the diagnosed links and invariant before pattern use. ICLR patterns were consulted after freeze to inspect modeled-object and responsibility structure; risk: decomposition and order-specific encoding may duplicate the source architecture; effect `bounded`.
- Direct-use assessment for `CAND-010` found no causality, leakage, sampling, shape, differentiability, stability, training/inference, multivariate, or 24 GB resource incompatibility in the stated regime. `FIND-001` is `NONE / NO-ADAPTATION-REQUIRED`. Section 9 contains no `SYS-*` or `COMP-*` entity.
- `EXP-1001` completed the band-error diagnostic; `EXP-1002` completed the capacity control; `EXP-1003` completed the optimization-budget control. Each has sourced results and non-guarantees. `EXP-1004` is a planned band-order intervention with `PENDING` result and supports no claim.
- G0 through G7 are `EVALUATED / SATISFIED / null`. G8 through G11 are `DEFERRED / UNRESOLVED / null`. No final decision is precomputed.

## Source

- **Paper:** *TimeKAN: KAN-based Frequency Decomposition Learning Architecture for Long-term Time Series Forecasting*
- **Venue:** ICLR 2025
- **Official proceedings:** https://proceedings.iclr.cc/paper_files/paper/2025/hash/46362971bfc3a97e6a271f2eb90fba17-Abstract-Conference.html
- **OpenReview:** https://openreview.net/forum?id=wTLc79YNbh

## Technical facts for comparison

The paper presents a Decomposition-Learning-Mixing architecture for time-series forecasting. Its disclosed system:

1. uses cascaded frequency decomposition to separate an input series into multiple frequency bands;
2. applies frequency-specific, multi-order KAN representation-learning blocks to those bands;
3. upsamples frequency representations as needed for recombination; and
4. mixes the learned frequency representations before producing the forecast.

The paper motivates these operations as a way to model complex mixtures of temporal frequency components. These facts support comparison only. They do not establish that every multiband KAN system is identical, that an unlisted semantic constraint is absent, or that a different candidate lacks a substantive distinguishing consequence.

## Frozen candidate facts

The candidate under evaluation:

- splits the input into four learned frequency bands rather than the source paper's illustrated three-band configuration;
- applies order-specific KAN encoders to the bands;
- upsamples and recombines the band representations through a learned mixer;
- changes hidden width and names the splitter a `semantic band module`; and
- provides no operational definition, constraint, intervention, or new prediction for the word `semantic` beyond the band construction above.

Audit the smallest positive technical delta. Do not treat wording or hidden width as automatically cosmetic or substantive; determine their research role from the supplied facts.
