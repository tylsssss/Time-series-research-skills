# Examples

Worked examples belong here. The directory is intentionally almost empty at `0.1.0`: a
good example is a sanitized dossier produced by a real run, and none has been published
yet. Fabricating one would be exactly the kind of unearned artifact this project exists
to prevent.

## What belongs here

| Kind | Purpose |
|---|---|
| A complete dossier from a real run | The single most convincing artifact for a skeptical reader: it shows the typed ledger, the gate table, and the decision as they actually look, not as they look in a summary. |
| A `NEED-EVIDENCE` dossier | The most counterintuitive outcome, and the hardest to believe without seeing it. Eval case 1 specifies this shape. |
| A `KILL` dossier | Proves the workflow can reject its user's idea, which is the claim people doubt most. |
| A before/after pair | The same prompt with and without the skill, so the difference is inspectable rather than asserted. |

## Required sanitization

An example is published to the whole internet and indexed by search engines. Before
adding one:

- [ ] Remove project names, dataset names, internal metrics, and anything under embargo
      or review. Replace them with neutral descriptions that preserve the argument's
      structure — the structure is the point, not the specifics.
- [ ] Remove personal names, affiliations, collaborators, and correspondence.
- [ ] Remove any claim you would not defend in public.
- [ ] Re-run `python3 evals/run.py --grade <file>` on the sanitized version: it must still
      pass Tier 1. If sanitization broke the contract, the example is teaching the wrong
      shape.
- [ ] State in the file's header that it is a sanitized real run, and what was changed.
      An example that hides its own redactions is a bad example in this repository.

## How examples are used

Examples are **illustrations, not ground truth**. They are deliberately excluded from the
eval suite: grading a model's dossier against another dossier's prose would reward mimicry
over reasoning, and the suite's expectations are written against the contract in
`assets/idea-dossier-template.md` instead. Tier 2 judges the 96 expectations, never
similarity to an example.

Add examples through a pull request using the pattern above. Behavioral failures are
still more valuable than examples — see
[`../.github/ISSUE_TEMPLATE/behavioral_failure.md`](../.github/ISSUE_TEMPLATE/behavioral_failure.md).
