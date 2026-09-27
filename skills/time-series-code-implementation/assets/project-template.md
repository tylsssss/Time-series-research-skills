# Project Template

Canonical research-repo scaffold for this skill. Load in Phase 3 of SKILL.md: copy the starter files below into the new project, fill the `{{...}}` marks, then grow the frozen method inside this shape. The template encodes the personal style at file level — every generated project starts from the same layout, so style rules from `../references/personal-code-style.md` are satisfied by construction rather than by retrofitting.

When borrowing a library's layout (e.g. TSLib's `exp/` + `data_provider/` structure), keep the library's file organization and apply the style to the code you add — this template is the default for new projects, not a mandate to restructure borrowed repos.

- [Directory tree](#directory-tree)
- [run.py — entry with boundary validation](#runpy--entry-with-boundary-validation)
- [exp/exp_method.py — one narrative per phase](#expexp_methodpy--one-narrative-per-phase)
- [model/method.py — shape-commented forward](#modelmethodpy--shape-commented-forward)
- [data_provider/data_loader.py — leakage-safe split](#data_providerdata_loaderpy--leakage-safe-split)
- [utils/metrics.py](#utilsmetricspy)

## Directory tree

```text
{{project}}/
├── run.py                    # argparse entry: boundary validation, seed, setting string
├── exp/
│   └── exp_{{method}}.py     # experiment class: train/val/test, one narrative per phase
├── model/
│   └── {{method}}.py         # the frozen method
├── data_provider/
│   └── data_loader.py        # dataset + loaders, leakage-safe split
├── utils/
│   └── metrics.py            # metric helpers
├── results/                  # <setting>/ JSON artifacts, created at runtime
└── scripts/                  # one shell launcher per dataset
```

## run.py — entry with boundary validation

The entry file is the one place that validates configuration; downstream code trusts it (style rule: guards at the entry boundary, never re-checked). Note the section banners, the `parser.error` for cross-argument consistency, the setting string, and `del exp` between repetitions.

```python
import argparse
import random
import numpy as np
import torch
from exp.exp_{{method}} import Exp_{{Method}}
from utils.print_args import print_args

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="{{Method}}")

    # Data
    parser.add_argument("--data", type=str, default="ETTh1", help="Dataset name")
    parser.add_argument("--root_path", type=str, default="./dataset/", help="Root directory for dataset files")
    parser.add_argument("--data_path", type=str, default="ETTh1.csv", help="CSV file name")
    parser.add_argument("--features", type=str, default="M", choices=["M", "MS", "S"],
                        help="'M'=multivariate, 'MS'=multivariate->single, 'S'=univariate")
    parser.add_argument("--target", type=str, default="OT", help="Target column for S/MS mode")

    # Task
    parser.add_argument("--seq_len", type=int, default=96, help="Input sequence length")
    parser.add_argument("--pred_len", type=int, default=96, help="Prediction horizon")

    # Model
    parser.add_argument("--enc_in", type=int, default=7, help="Encoder input size")
    parser.add_argument("--d_model", type=int, default=512, help="Hidden dimension")
    parser.add_argument("--dropout", type=float, default=0.1, help="Dropout rate")

    # Optimizer
    parser.add_argument("--learning_rate", type=float, default=1e-4, help="Learning rate")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--train_epochs", type=int, default=20, help="Training epochs")
    parser.add_argument("--patience", type=int, default=3, help="Early stopping patience")
    parser.add_argument("--grad_clip", type=float, default=2.0, help="Gradient clipping max norm")

    # System
    parser.add_argument("--num_workers", type=int, default=0, help="DataLoader workers")
    parser.add_argument('--use_gpu', action='store_true', default=True, help='use gpu (default: on)')
    parser.add_argument('--gpu', type=int, default=0, help='gpu id')

    # Experiments
    parser.add_argument('--itr', type=int, default=3, help='number of repetitions')
    parser.add_argument("--exp_name", type=str, default="{{method}}", help="experiment name")
    parser.add_argument("--seed", type=int, default=2021, help="Random seed")

    args = parser.parse_args()

    # Boundary validation: cross-argument consistency lives here, once.
    if args.patience >= args.train_epochs:
        parser.error(f"--patience ({args.patience}) must be < --train_epochs ({args.train_epochs})")
    if args.seq_len <= 0 or args.pred_len <= 0:
        parser.error("--seq_len and --pred_len must be positive")

    print("Args in experiment:")
    print_args(args)

    base_seed = args.seed
    for ii in range(args.itr):
        # Each repetition uses an explicit and reproducible seed.
        args.seed = base_seed + ii
        random.seed(args.seed)
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(args.seed)

        setting = (
            f"{args.exp_name}_{{method}}_{args.data}"
            f"_ft{args.features}"
            f"_sl{args.seq_len}"
            f"_pl{args.pred_len}"
            f"_dm{args.d_model}"
            f"_lr{args.learning_rate}"
            f"_seed{args.seed}"
            f"_itr{ii}"
        )

        print(">>>>>>>start experiment: {}>>>>>>>>>>>>>>>>>>>>>>>>>>".format(setting))
        exp = Exp_{{Method}}(args)
        exp.train(setting)
        exp.test(setting)

        # Release the current experiment before the next repetition.
        del exp
        if args.use_gpu and torch.cuda.is_available():
            torch.cuda.empty_cache()
```

## exp/exp_method.py — one narrative per phase

Each phase is one method written top to bottom: args unpacked into locals first, then pure logic (style rules: one whole, config plumbing out of the story). Progress is one dense `[Phase]` line per epoch; results accumulate in structured dicts and are JSON-dumped at the end.

```python
import json
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam

from data_provider.data_loader import data_provider
from model.{{method}} import Model
from utils.metrics import metric
from utils.tools import EarlyStopping


class Exp_{{Method}}:
    def __init__(self, args):
        self.args = args
        self.device = torch.device(f"cuda:{args.gpu}" if args.use_gpu and torch.cuda.is_available() else "cpu")

        self.train_set, self.train_loader = data_provider(args, "train")
        self.val_set, self.val_loader = data_provider(args, "val")
        self.test_set, self.test_loader = data_provider(args, "test")

        self.model = Model(args).float().to(self.device)
        self.criterion = nn.MSELoss()
        self.optimizer = Adam(self.model.parameters(), lr=args.learning_rate)

    def train(self, setting):
        train_epochs = self.args.train_epochs
        patience = self.args.patience
        grad_clip = self.args.grad_clip

        folder_path = f"./results/{setting}/"
        os.makedirs(folder_path, exist_ok=True)
        early_stopping = EarlyStopping(patience=patience, verbose=True)
        history = []

        for epoch in range(train_epochs):
            epoch_time = time.time()
            self.model.train()
            train_losses = []

            for batch_x, batch_y, batch_x_mark, batch_y_mark in self.train_loader:
                self.optimizer.zero_grad()
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                outputs = self.model(batch_x, batch_x_mark)
                outputs = outputs[:, -self.args.pred_len:, :]
                target = batch_y[:, -self.args.pred_len:, :]

                loss = self.criterion(outputs, target)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=grad_clip)
                self.optimizer.step()

                train_losses.append(loss.item())
            train_loss = float(np.average(train_losses))

            # Validation: accumulate raw sums, divide once at the end.
            self.model.eval()
            squared_error_list = []
            absolute_error_list = []
            element_count_list = []

            with torch.no_grad():
                for batch_x, batch_y, batch_x_mark, batch_y_mark in self.val_loader:
                    batch_x = batch_x.float().to(self.device)
                    batch_y = batch_y.float().to(self.device)
                    batch_x_mark = batch_x_mark.float().to(self.device)

                    outputs = self.model(batch_x, batch_x_mark)
                    outputs = outputs[:, -self.args.pred_len:, :]
                    target = batch_y[:, -self.args.pred_len:, :]

                    squared_error_list.append(F.mse_loss(outputs, target, reduction="sum").item())
                    absolute_error_list.append(F.l1_loss(outputs, target, reduction="sum").item())
                    element_count_list.append(target.numel())
            total_elements = sum(element_count_list)
            val_mse = sum(squared_error_list) / total_elements
            val_mae = sum(absolute_error_list) / total_elements

            history.append({"epoch": epoch + 1, "train_loss": train_loss, "val_mse": val_mse, "val_mae": val_mae})

            print(
                f"[Train {epoch + 1:3d}/{train_epochs}] "
                f"train_loss={train_loss:.6f} | "
                f"val_mse={val_mse:.6f} | "
                f"val_mae={val_mae:.6f} | "
                f"time={time.time() - epoch_time:.2f}s"
            )

            early_stopping(val_mse, self.model, folder_path + "checkpoint.pth")
            if early_stopping.early_stop:
                print(f"[Train] Early stopping at epoch {epoch + 1}.")
                break

        with open(folder_path + "train_history.json", "w") as f:
            json.dump(history, f, indent=2)
        return history

    def test(self, setting):
        folder_path = f"./results/{setting}/"
        self.model.load_state_dict(torch.load(folder_path + "checkpoint.pth", map_location=self.device, weights_only=True))
        self.model.eval()

        # Test evaluation: same accumulation pattern as the validation pass above.
        squared_error_list = []
        absolute_error_list = []
        element_count_list = []

        with torch.no_grad():
            for batch_x, batch_y, batch_x_mark, batch_y_mark in self.test_loader:
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)

                outputs = self.model(batch_x, batch_x_mark)
                outputs = outputs[:, -self.args.pred_len:, :]
                target = batch_y[:, -self.args.pred_len:, :]

                squared_error_list.append(F.mse_loss(outputs, target, reduction="sum").item())
                absolute_error_list.append(F.l1_loss(outputs, target, reduction="sum").item())
                element_count_list.append(target.numel())
        total_elements = sum(element_count_list)
        test_mse = sum(squared_error_list) / total_elements
        test_mae = sum(absolute_error_list) / total_elements

        results = {"setting": setting, "test_mse": float(test_mse), "test_mae": float(test_mae)}
        with open(folder_path + "final_results.json", "w") as f:
            json.dump(results, f, indent=2)

        print(f"[Test] mse={test_mse:.6f} | mae={test_mae:.6f}")
        return results
```

Note: the validation and test accumulation loops are deliberately inlined rather than extracted into a shared helper — evaluation is part of each phase's narrative, and repeated inline loops beat an everywhere-called method (style rule: logic is one whole).

## model/method.py — shape-commented forward

The forward pass is one linear narrative with a shape comment at every transformation (style rules: one whole, shapes as comments, no per-call guards — the constructor resolved every config once).

```python
import torch
import torch.nn as nn


class Model(nn.Module):
    """
    {{One-line role of the method.}}
    Flow: normalization -> {{embedding}} -> {{encoder}} -> projection -> de-normalization.
    """
    def __init__(self, configs):
        super().__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.use_norm = True

        # {{embedding, encoder, head layers — built here once, config resolved here once}}

    def forward(self, x_enc, x_mark_enc, x_dec=None, x_mark_dec=None):
        del x_dec, x_mark_dec

        # Instance normalization
        if self.use_norm:
            means = x_enc.mean(dim=1, keepdim=True).detach()
            x_enc = x_enc - means
            stdev = torch.sqrt(torch.var(x_enc, dim=1, keepdim=True, unbiased=False) + 1e-5)
            x_enc = x_enc / stdev

        # [B, L, C] -> [B, C, L]
        x = x_enc.permute(0, 2, 1).contiguous()

        # {{core computation; one shape comment per transformation}}

        # [B, C, L] -> [B, L, C]
        x = x.permute(0, 2, 1).contiguous()

        # De-normalization
        if self.use_norm:
            x = x * stdev[:, 0, :].unsqueeze(1) + means[:, 0, :].unsqueeze(1)
        return x[:, -self.pred_len:, :]
```

## data_provider/data_loader.py — leakage-safe split

Split by time order; fit the scaler on the train split only (see `../references/research-code-conventions.md` §3 — this is the single most common silent bug in time-series code).

```python
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset


class Dataset_{{Task}}(Dataset):
    def __init__(self, data, seq_len, pred_len, flag, scale_stats=None):
        # {{build windows here; for forecasting, split train/val/test by time order
        #   before windowing so windows never cross the split boundary}}
        self.seq_len = seq_len
        self.pred_len = pred_len
        if flag == "train":
            self.scale_mean, self.scale_std = data.mean(0), data.std(0) + 1e-5
        else:
            # Fit scalers on the train split only; val/test reuse them.
            self.scale_mean, self.scale_std = scale_stats
        # {{windowed x: [N, L, C], y: [N, H, C]}}

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index], self.x_mark[index], self.y_mark[index]


def data_provider(args, flag):
    # {{load file, time-ordered split, build dataset with train scale stats passed on}}
    data_set = Dataset_{{Task}}(..., flag=flag, scale_stats=scale_stats)
    data_loader = DataLoader(data_set, batch_size=args.batch_size, shuffle=(flag == "train"),
                             num_workers=args.num_workers, drop_last=(flag == "train"))
    return data_set, data_loader
```

## utils/metrics.py

```python
import numpy as np


def metric(pred, true):
    mae = np.mean(np.abs(pred - true))
    mse = np.mean((pred - true) ** 2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((pred - true) / (true + 1e-8))) * 100
    return mae, mse, rmse, mape
```

When replacing `{{...}}` marks: keep the style marks too — the section banners, the `[Phase]` prints, the shape comments, and the boundary-only validation. They are part of the template, not decoration.
