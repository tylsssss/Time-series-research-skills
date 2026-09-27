# Eval results

Tier-2 results are written here, one file per run, so that a pass rate is a file you can
review rather than a claim in a README.

Nothing is recorded yet: no Tier-2 run has been executed against a real provider from
this repository, because that requires an API key and the maintainer's budget. That is
stated plainly rather than papered over — see the limitations section of the README.

## Running

```bash
python3 evals/run.py --tier2 --case 1 --provider anthropic --model <model>
python3 evals/run.py --tier2                       # all cases
```

The runner writes a Markdown report here by default; `--out <path>` overrides the
location. The naming convention is `<date>-<provider>-<model>.md`, with the model name
sanitized for filesystem safety.

## What a published result should contain

* The provider and exact model identifier, plus any generation settings the runner used
  (`--max-tokens`, judge model).
* The date, so a reader can tell how stale the result is — model behavior drifts.
* Per-case pass/fail against the eight or nine natural-language expectations, with the
  judge's reason for each failure. A pass rate alone is not reviewable.
* The full list of expectations the run failed, not only the count.

## Honest reporting rules

These mirror `CONTRIBUTING.md`:

* Do not publish a pass rate from a different model, a different prompt revision, or a
  partial case set without saying so in the file.
* Do not delete an unfavorable result. A failing run is evidence about the artifact; a
  results directory containing only good numbers is a marketing page.
* Keep the raw per-case reasons. If a case fails for a reason you believe is a grader
  bug, fix the grader and record both the failure and the fix — do not rerun until it
  looks better.
* Tier-1 results do not belong here. Structural grading is deterministic and runs in CI;
  its evidence is the self-test output in the `ci` workflow, not a results file.

## Privacy

A results file can contain generated dossier text, which may quote your prompts. Read a
report before committing it, and do not include one that carries project names, dataset
names, or anything under review.
