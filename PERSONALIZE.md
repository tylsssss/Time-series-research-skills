# Personalize this project

These skills carry a **personal layer**: six Markdown files that encode research taste
rather than method. They are the reason the output feels opinionated instead of generic
— and the reason you should replace them with your own before you rely on the results.

The layer is a fixed set of six **slots**. A *profile* is a complete replacement for all
six. Partial replacement is not supported: a half-swapped layer produces contradictions
between the priors file and the pattern cards.

## The six slots

| Slot | Feeds | What it decides |
|---|---|---|
| `references/personal-research-priors.md` | ideation, Stage 0, Stage 8, and the final decision | Which alternatives you prefer when evidence permits, and your rejection list |
| `references/personal-pattern-index.md` | ideation, Stage 5 | Which of your precedent cards a frozen candidate may consult |
| `references/personal-pattern-card-a.md` | ideation, Stage 5 | Precedent card slot A: one structural precedent from your own work |
| `references/personal-pattern-card-b.md` | ideation, Stage 5 | Precedent card slot B: one structural precedent from your own work |
| `references/personal-pattern-card-c.md` | ideation, Stage 5 | Precedent card slot C: one structural precedent from your own work |
| `references/personal-code-style.md` | implementation, Phases 2–4 | The coding style every generated line must follow |

## What ships

`profiles/default/` is a **neutral skeleton**: the same six files, no preferences, no
precedent content, and a note in each about what belongs there. It is the honest starting
point — you get the gates and the typed dossier without inheriting anyone's research
taste, and no file in this repository describes an unpublished project.

A **`private` profile is the intended way to keep your own layer locally.** It is
git-ignored, so it never reaches the public repository:

```bash
mkdir -p profiles/private
cp profiles/default/*.md profiles/private/    # start from the skeleton
$EDITOR profiles/private/*.md                 # write your own priors and cards
scripts/use-profile.sh private                # apply it to the live slots
scripts/use-profile.sh --list                 # show profiles and the active one
scripts/use-profile.sh --check                # compare live slots with profiles/default
scripts/use-profile.sh default                # restore the shipped neutral default
```

Keep your real stance in `profiles/private/`, never in `profiles/default/`. A default
profile is published, indexed, and permanent, and a precedent card states the failure,
mechanism, and invariant of a project that may still be under review. That is a
disclosure, not a preference.

Applying a profile backs up the previous slot contents to
`profiles/.backup/<timestamp>/`, so a swap is reversible. `profiles/.active` records
the applied profile name and is git-ignored.

## What to write in your own profile

**Priors.** Read `profiles/default/personal-research-priors.md` for the shape, then
write yours. Keep the five-section structure, because three moments load it: the boundary
stage, the novelty audit at Stage 8, and the moment before the final decision. Add a preference
only when you can state it as a rule that selects between evidence-compatible
alternatives, and record each addition with the update block the file defines
(`Prior / Type / Source / Scope / Rationale / Exceptions / Conflicts / Last confirmed`).
A prior that can override evidence is a bug, not a preference.

**Pattern cards.** A card is a *conditional precedent*, not advice: a structural
signature, the failure it explains, the invariant it preserves, its direct-use risks,
its theory boundary, and the test that would kill it. The three shipped slots are empty
templates; yours should come from your own projects. Two rules matter more than the
prose:

* a card is a stress-test instrument used **after** the candidate set is frozen — never
  evidence, never a candidate generator, never a novelty source;
* the routing must be able to fail. If every candidate matches a card, your index is a
  horoscope, not a router.

**Code style.** `personal-code-style.md` is authoritative over generic conventions for
all generated code. The implementation skill also summarizes the default profile's
contract inline in its `SKILL.md`. That summary belongs to
`profiles/default/personal-code-style.md`; if you write a neutral or different style
file, the file wins and the inline summary becomes a historical default. If your style
differs materially, say so at the top of your `personal-code-style.md` — the
implementation skill reads the file, not the summary, when the two disagree.

## The one structural constraint

The three card filenames are fixed, and they are deliberately generic
(`personal-pattern-card-a/b/c.md`). A descriptive name would disclose your research
directions in a filename alone, to anyone who lists the repository — the same leak the
content would cause, just quieter. The Stage-5 router loads at most one card through the
index, and the controller's router table names the card family rather than individual
files, so you can rewrite the card *contents* freely and you can add a fourth card by
adding a row to `personal-pattern-index.md` and a file beside them — but do not rename
the existing three, or the index's route map will point at nothing and CI
(`scripts/lint.mjs`) will fail the build.

## Do not commit your profile

Your priors and precedent cards describe your research direction and are usually
unpublished. `scripts/lint.mjs` and CI warn when the live slots differ from
`profiles/default/` — that warning is the tripwire for an accidental
`git add -A` after a swap. If you intend to publish a profile, contribute it as a
directory under `profiles/` (see `CONTRIBUTING.md`), not as an edit to the slots.
