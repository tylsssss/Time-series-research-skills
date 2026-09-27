<!--
Keep this checklist short. A pull request that cannot answer these should be
split or explained.
-->

## What changed

<!-- One paragraph. What behavior or document changed, and why. -->

## Type

- [ ] Behavioral change to a skill (controller, reference, or template)
- [ ] New or updated eval expectation
- [ ] New pattern card or routing rule
- [ ] Documentation or repository plumbing only
- [ ] Profile (default/minimal, or a new profile)

## Contract checks

- [ ] I ran `make ci` locally and it passes (`make lint` and `make self-test` are part of it).
- [ ] If I changed a skill's behavior, I added or updated at least one expectation in
      `skills/time-series-model-ideation/evals/evals.json`.
- [ ] If I changed the dossier schema (section count or order, ID namespace, enum value,
      gate semantics), I updated `assets/idea-dossier-template.md`, added a migration note
      in `CHANGELOG.md`, and updated `docs/schema.md`. Section numbers were not renumbered.
- [ ] If I renamed or added a reference file, every router table that names it is updated
      and the path resolves.
- [ ] If I touched a `personal-*.md` slot, `profiles/default/` is updated in the same
      commit (or the change is my own profile and is **not** in this pull request).

## Honesty checks

- [ ] No personal data, affiliation, unpublished project detail, or third-party text was
      added.
- [ ] No claim in this pull request is stronger than what I actually ran or read.
- [ ] Any negative result, unresolved gate, or rejected candidate that this change
      produces is reported rather than smoothed over.

## Notes for the reviewer

<!-- Anything you tried that did not work, anything you are unsure about, and what you
     could not verify. This section is read. -->
