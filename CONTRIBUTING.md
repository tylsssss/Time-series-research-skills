# Contributing

Thanks for considering a contribution. This project has an unusual constraint: it is a
set of instructions for language models, so a change that reads better can still make
the artifact behave worse. The rules below exist to keep behavior auditable.

## Ground rules

1. **Behavior changes ship with an eval expectation.** Any change to a `SKILL.md`,
   a reference file that a stage loads, or the dossier template that could change what
   a run produces must add or update at least one expectation in
   `skills/time-series-model-ideation/evals/evals.json`. A prompt change without a test
   is an unverified claim, which is exactly what this project exists to prevent.
   Changes that provably cannot alter behavior — fixing a path, correcting a cross
   reference, recording a mapping the files already implied, or making an existing rule
   explicit without changing its meaning — instead need a `CHANGELOG.md` entry under
   *Consistency repairs* that says why the change is non-behavioral. If you cannot argue
   that case in one sentence, it is a behavior change: write the expectation. Loosening
   a rule is always a behavior change, and "the tests were inconvenient" is not an
   argument that a rule was unclear.
2. **The dossier schema is frozen except by explicit migration.** Section count,
   section order, ID namespaces, enum values, and gate semantics are a public
   contract: users have dossiers written against them. A schema change requires:
   updating `assets/idea-dossier-template.md`, adding a `CHANGELOG.md` entry with a
   migration note under a new schema version, and updating `docs/schema.md`. Never
   renumber an existing section to make room.
3. **Reference paths must resolve.** `SKILL.md` routes to reference files by literal
   relative path. If you rename or add a reference, update every router table that
   names it. `scripts/lint.mjs` fails the build on a dangling path.
4. **Keep the routers in sync.** A new pattern card must be added to the matching
   index (and, for ICLR cards, to the router table in `SKILL.md`). A card that no
   index routes to is dead weight.
5. **No personal data, no third-party text.** Contributions must not contain real
   names, affiliations, email addresses, unpublished project details, or copied text
   from papers, blogs, or other repositories. Paraphrase and cite instead.
6. **No vendor content.** Do not vendor another project's skills, prompts, or
   documentation into this repository, even with attribution. Link to it.
7. **Profiles stay in sync.** `profiles/default/` is a byte-identical copy of the live
   `personal-*.md` slots. If you change a slot file in place, update the profile copy
   in the same pull request; CI compares them.

## Development workflow

Requirements: `python3` (3.9+) and `node` (18+). No package installation is needed —
the runner and the linters use only the standard library.

```bash
make ci            # everything CI runs: lint, self-test, bundle, installer, profile swap
make lint          # frontmatter, reference paths, profile sync, fixtures, assets, identity
make self-test     # structural grader proves it can pass a good dossier and fail a bad one
make bundle        # build dist/*.bundle.md
make install-user  # install both skills for the current user (Claude Code + ~/.agents/skills)
```

**Run `make ci` before pushing.** It is the same set of steps the `ci` workflow runs —
the workflow calls these targets rather than restating them, because a workflow that
duplicates its checks drifts from them. This repository shipped a CI step naming a probe
profile that had been deleted, and only CI noticed, after the push. Running it locally
would have caught it.

`make ci` requires the shipped default profile; if you have applied your own, run
`scripts/use-profile.sh default` first.

## Documentation discipline

`docs/schema.md` and `docs/architecture.md` cite the file and line of every rule they
restate, because a rule you cannot locate is a rule you cannot check. That makes them
sensitive to edits elsewhere: changing `SKILL.md` or the dossier template can leave a
citation pointing at the wrong line.

`make lint` fails when a citation runs past the end of its target file, but it cannot
detect a citation that is merely off by a few lines. When you edit a file that `docs/`
quotes — `SKILL.md`, the template, or a reference — re-read the citations you touched and
fix the line numbers. Adding or removing lines near the top of a heavily cited file is
the common case.

## Changing the ideation controller

The controller is `skills/time-series-model-ideation/SKILL.md`. It is a state machine:
stages, gates, entry modes, and the reference router. When you edit it:

* preserve the gate semantics table and the decision routing table verbatim unless the
  change is itself about gate semantics, in which case say so in the pull request body;
* do not weaken a rule into a suggestion — the value of this artifact is that its rules
  are checkable;
* if you change what a stage must read, update both the stage text and the router table;
* if you make a rule stricter, check that no existing eval expectation now contradicts
  it, and update the expectation deliberately rather than silently.

## Adding a pattern card

See [`docs/contributing-a-pattern-card.md`](docs/contributing-a-pattern-card.md) for the
card anatomy, the routing rules, and the checklist. Cards come in two families:
`iclr-pattern-*` (public argument-structure catalogue) and `personal-pattern-*`
(profile-specific precedent, which belongs in a profile, not in the shipped default
unless you are the profile's author).

## Adding a profile

A profile is a complete replacement for the six `personal-*.md` slots; partial profiles
are not supported because a half-swapped layer produces contradictions between the
priors file and the cards. To contribute a profile:

1. create `profiles/<name>/` with exactly the six slot files (copy `profiles/default/`
   as the starting point);
2. keep the three card filenames unchanged — the controller's router and the index
   route map assume them, and they are deliberately generic (`personal-pattern-card-a/b/c.md`)
   so a filename never discloses a research direction;
3. describe the profile's stance in `profiles/README.md`;
4. do not include identifying information; a profile should read as a research stance,
   not a biography; and
5. if your stance comes from work that is not published yet, do not contribute it at all.
   Keep it in the git-ignored `profiles/private/` — a precedent card names the failure,
   mechanism, and invariant of a real project, which is enough to describe unpublished
   work.

## Reporting a behavioral failure

If the skill produces a dossier that violates its own contract — a gate passed with
unresolved evidence, a numeric novelty score, a plan cited as evidence, a fabricated
`SYS-*` in a `NOT-STARTED` section — open a bug report using the *Behavioral failure*
template. Include the prompt, the offending dossier excerpt, and, if you can, the
Tier-1 report from `python3 evals/run.py --grade <dossier.md>`. A reproducible
behavioral failure is the most valuable contribution to this repository.

## Commit and pull-request hygiene

* One concern per pull request; keep unrelated reformatting out of a semantic change.
* Explain *why* in the pull request body, and state what you ran to verify the change.
* Do not add generated files (`dist/`) or your own applied profile to a pull request.
* By contributing you agree your contribution is licensed under Apache-2.0.

## Code of conduct

Participation is governed by [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
