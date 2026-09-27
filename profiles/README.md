# Profiles

A profile is a complete replacement for the six `personal-*.md` slots described in
[`../PERSONALIZE.md`](../PERSONALIZE.md). Profiles exist so that the research taste in
this project is a visible, swappable input rather than an invisible assumption baked
into the instructions.

## Shipped profiles

| Profile | Stance | Use it when |
|---|---|---|
| `default/` | Neutral skeleton. No preferences, no precedent content, no code-style overrides beyond "follow the repository conventions." Each slot states what belongs in it. | Always available as the shipped state: you get the gates and the typed dossier without inheriting anyone's taste, or you are writing your own profile. |

`private/` is not shipped. It is the git-ignored place for **your own** layer: copy the
skeleton into it, write your priors and cards there, and apply it with
`scripts/use-profile.sh private`. Nothing under `profiles/private/` is committed, so an
unpublished project's failure, mechanism, and invariant never reach a public repository.
`PERSONALIZE.md` walks through it.

## Files in a profile

Exactly six, with these names. The names are fixed because the skills' routers resolve
them by literal path.

```text
personal-research-priors.md                    # ideation: Stage 0 + Stage 8 + final decision
personal-pattern-index.md                      # ideation: Stage-5 routing
personal-pattern-card-a.md        # ideation: precedent card
personal-pattern-card-b.md           # ideation: precedent card
personal-pattern-card-c.md             # ideation: precedent card
personal-code-style.md                         # implementation: authoritative code style
```

## Applying a profile

```bash
scripts/use-profile.sh --list                  # profiles and the active one
scripts/use-profile.sh private                 # apply your own local layer
scripts/use-profile.sh default                 # restore the shipped neutral default
```

The script copies the profile's six files into the live slots, backing up the previous
contents to `profiles/.backup/<timestamp>/` and recording the applied name in
`profiles/.active` (git-ignored).

## Sync rule

`profiles/default/` must stay byte-identical to the live slots, so that "restore the
default" is always meaningful and the honest state of the repository is visible in a
diff. `scripts/lint.mjs` compares them and CI reports a mismatch as a warning — if you
changed a slot on purpose, change `profiles/default/` in the same commit; if you did
not, restore it.

## Contributing a profile

Copy `profiles/default/`, fill it in, and open a pull request. Keep the three card
filenames. Do not include identifying information, unpublished project details, or
affiliations: a profile should read as a research stance, not a biography. Add a row to
the table above describing the stance and when to use it.

If your stance comes from work that is not published yet, do not contribute it at all —
keep it in `profiles/private/`. A contributed profile is public forever, and a precedent
card is specific enough to describe an unpublished project.
