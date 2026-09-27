# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Two version numbers exist and they move independently:

* **Project version** (`0.x.y`) — the packaging of this repository.
* **Dossier schema version** — the field/enum/gate contract of
  `skills/time-series-model-ideation/assets/idea-dossier-template.md`. Any change to
  section count, section order, ID namespaces, enum values, or gate semantics is a
  schema change and must be called out explicitly here with a migration note.

## Dossier schema versions

| Schema | Introduced | Change | Migration |
|---|---|---|---|
| 1.0.0 | pre-release (implicit) | Original contract. Dossiers written before the version field existed are implicitly 1.0.0. | None. |
| 1.1.0 | this release | Section 0 gains the required `dossier_schema_version` field. Gate semantics: `coverage_complete: NO` in Section 13 makes G11 `EVALUATED` and `UNRESOLVED` — never satisfied — capping the decision at `NEED-EVIDENCE`. | Add `dossier_schema_version: "1.0.0"` to an old dossier, or regenerate it. No section was renumbered, no ID namespace or enum value changed, so an old dossier stays readable apart from the new field and the stricter G11 route. |

## [Unreleased]

### Removed before publication

* **The maintainer's personal layer.** `profiles/default/` and the six live
  `personal-*.md` slots carried the maintainer's research priors and three precedent
  cards distilled from their own projects — one of which is under review. Publishing them
  would have disclosed an unpublished research direction, so they were removed from
  everything this repository ships: `profiles/default/` is now a neutral skeleton and the
  live slots match it byte for byte. The maintainer's own layer is kept locally in the
  git-ignored `profiles/private/`, which is the pattern `PERSONALIZE.md` now recommends
  to every user. `scripts/lint.mjs` warns when the live slots differ from
  `profiles/default`; that warning is the tripwire against committing a private profile.
* `profiles/minimal/` no longer exists. With the maintainer's stance gone the neutral
  skeleton *is* the default, so a second identical profile would be noise. The Makefile
  target is `make use-private` instead of `make use-minimal`.
* The published contact address is `sazhang@bjtu.edu.cn`: `CITATION.cff` (author email),
  `.claude-plugin/marketplace.json` (owner email), `CODE_OF_CONDUCT.md` and
  `SECURITY.md`. `scripts/lint.mjs` L08 allows exactly that one declared address, read
  from `CITATION.cff`, and still fails on any other email address in shipped content.

### Dossier schema 1.1.0 — gate semantics

* **`coverage_complete: NO` now has a defined gate consequence.** Previously the template
  permitted incomplete falsification coverage while stating no consequence for G11, so a
  dossier could report an uncovered CORE claim and still claim a satisfied falsification
  gate. Section 13's note and `SKILL.md` Stage 11 now state: G11 is `EVALUATED` and
  `UNRESOLVED`, the decision is capped at `NEED-EVIDENCE`, and each uncovered CORE claim
  must be named as the smallest next action. This is the one behavioral change in this
  release; the eval suite covers it.
* **Added `dossier_schema_version` to Section 0.** The versioning rule in this file
  referred to schema versions that a dossier could not name. The field makes migration
  actionable and unblocks the roadmap item for a dossier migration tool.

### Added

* Repository scaffolding: Apache-2.0 license, NOTICE, CITATION.cff, CONTRIBUTING,
  CODE_OF_CONDUCT, SECURITY, .editorconfig, issue and pull-request templates.
* `README.md` and `README.zh-CN.md`.
* `docs/schema.md` — normative dossier-format reference (sections, lifecycle, entry
  modes, ID namespaces, claim typing, evidence levels, gates, decision routing).
* `docs/architecture.md` — stage chain, progressive reference-loading router, the
  two-skill pipeline handoff, and a measured context-budget table.
* `docs/faq.md` and `docs/contributing-a-pattern-card.md`.
* `evals/` — a dependency-free runner with deterministic structural grading (Tier 1,
  offline, CI-safe) and an opt-in model-judged tier (Tier 2), plus regenerable
  good/bad dossier fixtures and a self-test.
* `profiles/` — the personal-layer slots extracted into a swappable profile layer: a
  neutral shipped `default/` skeleton plus a git-ignored `private/` for your own stance,
  with `PERSONALIZE.md` and `scripts/use-profile.sh`.
* `scripts/install.sh` for Claude Code, Codex / `~/.agents/skills`, and project-local
  installs, with `--dry-run` and backup-on-overwrite.
* `scripts/build-bundle.mjs` — flattens a skill plus the references it needs into a
  single Markdown bundle for agents without a skills mechanism.
* `scripts/lint.mjs` — frontmatter, reference-path, profile-sync, fixture-path, and
  asset checks, wired into `.github/workflows/ci.yml`.

### Changed

* `skills/time-series-model-ideation/SKILL.md`: the Stage-5 personal-card list is now
  data-driven. The three hardcoded card filenames were replaced by a rule that defers
  to the route map in `references/personal-pattern-index.md`. Under the shipped neutral
  profile the index configures no route rows, so a default installation records that
  personal patterns were not consulted; the change makes the profile layer extensible
  without editing the controller. This is a controller change only — the dossier schema
  is untouched.
* Both skills now carry an `agents/openai.yaml` adapter and an `assets/icon.svg`.

### Consistency repairs

Five discrepancies between `SKILL.md` and `assets/idea-dossier-template.md` were found
while documenting the format, and repaired in favor of the template (the declared
authority). The first is behavioral; the other four are contract or documentation
alignments that change no rule's meaning.

* **Stage 8 reads the personal priors (behavioral).** `references/novelty-audit.md`
  requires `references/personal-research-priors.md` as a Stage-8 input, but the router
  assigned that file to Stage 0 and the final decision only. The router row now reads
  "Stage 0, Stage 8, and the final decision", so the user's innovation and attribution
  rules are available where novelty is judged. Covered by an eval expectation.
* **Stage 9's contract list now matches the template.** `SKILL.md` listed nine
  feasibility contracts including "observability" and omitted numerical/optimization
  dynamics, while Section 11 defines nine different aspect rows. `SKILL.md` now names
  the template's nine rows verbatim and defers to the template for the row list;
  observability is stated as the requirement it actually is, in
  `references/feasibility-audit.md`.
* **Stage and section numbering are now explicit.** `SKILL.md` numbers stages 0–12 while
  the template numbers sections 0–16 and the two are offset; neither file said so. The
  phase block now records the offset and that gates align with stages, not sections.
* **`current_phase: COMPLETE` is now reachable.** The template allowed the terminal
  phase value, `SKILL.md` did not mention it. `SKILL.md` now states when to set it.
* **Stage 0 records the schema version.** See the schema 1.1.0 entry above.

### Provenance notes

* Extracted from the author's working skill installation. This repository is the
  source of truth going forward; the previously installed copy is no longer updated.
* No third-party skill content is redistributed. See NOTICE.
