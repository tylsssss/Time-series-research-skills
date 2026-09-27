# Research-Code Conventions for Time-Series Deep Learning

Follow these conventions when implementing (SKILL.md Phases 2–4). They exist because time-series research code dies young from three causes: irreproducibility, silent data leakage, and results nobody can rerun. Each section explains the convention and why it matters.

`personal-code-style.md` is authoritative for all written code; where a convention here conflicts with the personal style, the personal style wins.

## 1. Seeds and determinism

- Set one master seed per run and derive everything from it: `random`, `numpy`, `torch`, dataloader worker generators, and any library with its own RNG.
- Fix `torch.manual_seed` on every device and set `torch.use_deterministic_algorithms` only if the architecture is compatible; document the flag as "best effort".
- Do not promise bitwise reproducibility across platforms. Promise statistical reproducibility: same seed, same environment → same result; different seeds → report mean ± std.
- Report every result over at least 3 seeds. Single-seed results are anecdotes in deep time-series research.

## 2. Config over hardcode

- Every hyperparameter lives in one YAML (or dataclass) per experiment: model, optimizer, scheduler, batch size, epochs, early stopping, window sizes, and seed. No magic numbers inline.
- Log the full config (and the git commit hash) next to every result file, so any output can be traced to its exact settings.
- Support CLI overrides for the fields that change between quick runs (epochs, batch size, dataset).

## 3. Splits without leakage

- For forecasting: split by time order — train, then validation, then test — never shuffle across time. Use an expanding or rolling window for small datasets.
- Fit every scaler, normalizer, and encoder on the train split only; apply to val/test. Leaking test statistics into the scaler is the single most common silent bug in time-series code.
- Check window construction: sliding windows may overlap between train and test, and targets must never include future information relative to their inputs.
- For classification: shuffle only if samples are i.i.d.; for subject/session-grouped data, split by group, not by sample.
- Reuse the benchmark's official split and evaluation protocol whenever reproducing a published result (e.g., TSLib's long-term forecasting protocol). A custom split makes comparison meaningless.

## 4. Evaluation honesty

- Fix the evaluation protocol per dataset before running: metric implementation, horizon(s), lookback(s), and normalization (raw vs. normalized error).
- Always run trivial baselines: persistence (repeat last value), global mean, and a linear model. A deep model that cannot beat these has a bug or no signal — report it rather than tuning around it.
- Report per-dataset results with mean ± std over seeds. Never average metrics across heterogeneous datasets.
- Keep evaluation code separate from training code so results can be recomputed from checkpoints.

## 5. Logging and run identity

- Print one `[Phase]`-prefixed f-string summary line per epoch, carrying every metric at once (`[Search 3/30] shared_loss=... | val_mse=... | time=...s`). Dense and scannable beats verbose; per-iteration debug spam is an anti-pattern (see `personal-code-style.md` §7).
- Append structured records (dicts) to a history list during the run; at the end, JSON-dump the config, the final results, and the history (`best_config.json`, `final_results.json`, `search_history.json`). The JSON artifacts are the source of truth; TensorBoard or wandb are optional extras.
- Name each run `<dataset>-<model>-<seed>` and store its artifacts in a corresponding directory, so parallel runs cannot overwrite each other.
- Optionally log gradient norms early in training to catch instability before it becomes NaN.

## 6. Checkpointing and resume

- Save two checkpoints: best-on-validation and last epoch, plus the config needed to reload the model.
- Make training resumable (optimizer state, epoch number, RNG state when feasible) — long runs will be interrupted.
- Provide a separate eval script that loads a checkpoint and produces the metrics table, never re-trains.

## 7. Environment reproducibility

- Pin dependencies with a `requirements.txt` or `pyproject.toml` including exact versions, and state the Python version.
- Note the hardware assumptions (GPU count/memory, expected batch size) in the README or run instructions.
- Prefer `float32` default with optional AMP/bf16 flag; never silently drop from GPU to CPU on OOM — fail loudly.

## 8. Smoke and sanity checks

Add small checks that run in under a minute and are part of the deliverable:

- `smoke`: tiny synthetic series end to end; assert output shapes and finite losses.
- `overfit`: model must fit one small batch (loss → near zero) in a few dozen steps; failure means a structural bug, not a tuning problem.
- `nan-guard`: crash or warn on NaN/Inf loss instead of silently continuing.

These three checks catch the majority of wiring bugs before they consume GPU-hours.

## 9. Code provenance

Any code adapted from an external repo carries an attribution header above the adapted block:

```python
# Adapted from <repo-url> @ <commit-hash>
# Original: <path-in-repo>, (c) <authors>, <license>
# Changes: <what changed and why>
```

Check the source license first (see `library-landscape.md`). Unlicensed code: read for understanding, reimplement from the description, never copy. Copyleft licenses (e.g., GPL): copying imposes license obligations — flag this to the user before borrowing.

## 10. Compute hygiene

- Keep batch size explicit per GPU; use gradient accumulation only when documented in the config.
- Time long runs: record steps/second and estimated time-to-finish, and tell the user before launching anything that will take more than a few minutes.
- Cache preprocessed datasets to disk keyed by preprocessing parameters, so reruns do not recompute or (worse) recompute inconsistently.
