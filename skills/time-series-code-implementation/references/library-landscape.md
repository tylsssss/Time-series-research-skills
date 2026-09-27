# Time-Series Library Landscape

Map of GitHub repositories to consult as reference implementations. Load this in Phase 1 of SKILL.md. Verify the LICENSE file of each repo at read time — licenses can change, and an unlicensed repo is for reading only, not copying.

## 1. Model zoos and general deep learning

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [thuml/Time-Series-Library (TSLib)](https://github.com/thuml/Time-Series-Library) | MIT | Unified config-driven codebase for iTransformer, PatchTST, TimesNet, Autoformer, Informer, DLinear, and many others; covers forecasting, classification, anomaly detection, and imputation with consistent evaluation protocols | You need a state-of-the-art architecture, a reference training loop, or a fair evaluation protocol. Usually the first repo to read for deep models |
| [thuml/Autoformer](https://github.com/thuml/Autoformer) | MIT | Original Autoformer code (mostly subsumed by TSLib) | You need the original experiment scripts for Autoformer-family papers |
| [awslabs/gluonts](https://github.com/awslabs/gluonts) | Apache-2.0 | Probabilistic forecasting models (DeepAR, N-BEATS, PatchTST, TFT), robust data transforms, mature maintenance | Probabilistic outputs (quantiles, distributions) matter, or you want production-grade data handling |
| [unit8co/darts](https://github.com/unit8co/darts) | Apache-2.0 | High-level sklearn-like API over many models; forecasting, anomaly detection, covariates, backtesting | Quick experimentation across many models or anomaly detection with a unified API |

## 2. Forecasting-focused

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [jdb78/pytorch-forecasting](https://github.com/jdb78/pytorch-forecasting) | MIT | Temporal Fusion Transformer, DeepAR, N-BEATS on PyTorch Lightning | You want Lightning-based training with covariates and grouped time series |
| [Nixtla/neuralforecast](https://github.com/Nixtla/neuralforecast) | Apache-2.0 | Fast implementations (NHITS, PatchTST, TiDE, TimesNet) with scale-friendly training | You need fast SOTA baselines or large datasets |
| [zhouhaoyi/Informer](https://github.com/zhouhaoyi/Informer) | MIT | Original Informer for long-sequence forecasting | You are reproducing the Informer paper specifically |

## 3. Classification, regression, representation

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [timeseriesAI/tsai](https://github.com/timeseriesAI/tsai) | Apache-2.0 | InceptionTime, MiniRocket, TST, xresnet on fastai | Deep time-series classification/regression with strong defaults |
| [sktime/sktime](https://github.com/sktime/sktime) | BSD-3-Clause | sklearn-compatible API for classification, forecasting, transformations | You want a unified API and reproducibility conventions |
| [aeon-toolkit/aeon](https://github.com/aeon-toolkit/aeon) | BSD-3-Clause | Modern sklearn-compatible algorithms, well-maintained | Classification/regression baselines beyond deep models |
| [tslearn/tslearn](https://github.com/tslearn/tslearn) | BSD-2-Clause | DTW, kNN, shapelets, barycenters | Distance-based methods (DTW/kNN) as baselines |
| [gzerveas/mvts_transformer](https://github.com/gzerveas/mvts_transformer) | MIT | Influential multivariate transformer for regression/classification | Reference for transformer design details (positional encoding, pretraining tasks) |

## 4. Anomaly detection

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library) | MIT | Anomaly Transformer, TimesNet anomaly variants with standard evaluation | Deep anomaly detection on standard benchmarks |
| [unit8co/darts](https://github.com/unit8co/darts) | Apache-2.0 | PyOD-integrated detectors, forecasting-based scorers | Quick anomaly baselines |
| [salesforce/Merlion](https://github.com/salesforce/Merlion) | BSD-3-Clause | Ensemble anomaly + forecasting | Note: archived/less maintained; read for reference, prefer the above for dependencies |

## 5. Imputation

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [thuml/Time-Series-Library](https://github.com/thuml/Time-Series-Library) | MIT | TimesNet and friends for imputation benchmarks | Deep imputation models |
| [WenjieDu/PyPOTS](https://github.com/WenjieDu/PyPOTS) | GPL-3.0 | SAITS, Transformer imputation, unified benchmarking | **Caution**: GPL-3.0 is copyleft. Read for algorithm details; do not copy code into a non-GPL project. Reimplement from the paper instead |

## 6. Statistical baselines

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [Nixtla/statsforecast](https://github.com/Nixtla/statsforecast) | Apache-2.0 | Fast AutoARIMA, ETS, Theta, seasonal naive | Always useful: every deep-model paper needs strong statistical baselines |
| [sktime/sktime](https://github.com/sktime/sktime) | BSD-3-Clause | Broad statistical model collection | Statistical baselines within a unified API |

## 7. Pretrained foundation models

| Repo | License | Strengths | Use when |
|---|---|---|---|
| [google-research/timesfm](https://github.com/google-research/timesfm) | Apache-2.0 | Pretrained decoder-only foundation model, strong zero-shot forecaster | You need a strong zero-shot baseline, or want to compare against foundation models. Use as a black box; not a source for architecture borrowing |

## 8. Indexes for method discovery

- [qingsongedu/awesome-AI-for-time-series-papers](https://github.com/qingsongedu/awesome-AI-for-time-series-papers) — curated papers and official repos by task; use to find the original repository for a method mentioned in conversation.
- GitHub code search with the paper title or method name — the official repo usually lives in the first author's account (e.g., `thuml` hosts many time-series papers).

## 9. Reading a repo for implementation details

When borrowing or reproducing, read in this order — the details that matter most for reproduction are at the bottom:

1. `README.md` — task scope, benchmark table, quickstart.
2. `models/` — the architecture: layer composition, embedding, normalization placement.
3. Data loader and preprocessing — windowing, train/val/test split, scaling (which data the scaler was fit on), alignment of inputs and targets. These are the most common sources of silent evaluation leakage and irreproducibility.
4. Experiment scripts and configs — exact hyperparameters per dataset, optimizer, scheduler, early stopping.
5. Evaluation code — the exact metric implementation (e.g., MAE vs. normalized MAE) and whether results are averaged over seeds.

Record for every consulted file: repo URL, commit hash, path, license, and the specific decisions you adopt.
