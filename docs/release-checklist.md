# Release checklist

This is the pre-public checklist. Items marked **BLOCKING** must be resolved before the
repository is made public; the rest are improvements that can follow.

The list is ordered by the cost of getting it wrong, not by effort.

---

## 1. Provenance and licensing — BLOCKING

- [ ] **Confirm the repository contains no redistributed third-party content.** The
      working copy this was extracted from was a downloaded copy of another project's
      skill collection (its `.claude-plugin/marketplace.json` named a different owner and
      listed skills this project does not use). None of that was copied here, but verify
      by inspection before publishing:
      ```bash
      node scripts/lint.mjs          # L09 fails on known vendor attribution strings
      git log --stat                 # confirm the first commit contains only this project
      ```
- [ ] **Confirm authorship.** Every file under `skills/` is your own work. If any
      paragraph was adapted from a specification, blog post, or another repository, add
      an attribution note to `NOTICE`.
- [ ] **Decide the copyright holder string.** `LICENSE` currently reads
      `Copyright 2026 The Time-series-research-skills Authors`. Replace it with your legal
      name or entity if you prefer a named holder.
- [ ] **Verify the vendor-compatibility language.** `NOTICE` and the READMEs state that
      the project follows public Agent Skills conventions and is not affiliated with
      Anthropic or OpenAI. Keep that accurate and keep it visible.

## 2. Disclosure risk in the personal layer — RESOLVED, keep it that way

This is the one item that cannot be undone: a push is permanent and forks survive
deletion. It was reviewed, and it failed the review.

- [x] **Reviewed, and the layer was removed.** The maintainer's `profiles/default/` held a
      research constitution and three precedent cards distilled from their own projects,
      one of which is under review. That is a disclosure of research direction, so the
      content was removed from everything the repository ships: `profiles/default/` is now
      a neutral skeleton, the live `personal-*.md` slots match it byte for byte, and the
      maintainer's own layer lives in the git-ignored `profiles/private/`.
- [x] **`profiles/minimal/` was removed** as redundant, and the Makefile target is
      `make use-private`.
- [x] **Verified mechanically:** `scripts/lint.mjs` L04b fails when the live slots differ
      from `profiles/default`, and `scripts/use-profile.sh --check` reports the same. A
      private profile cannot be committed silently.

If you are publishing a fork, treat this section as a hard gate rather than history:

- [ ] Re-read `profiles/default/` as a competitor would. A precedent card names the
      failure, mechanism, and invariant of a real project — that is specific enough to
      describe unpublished work even without names or datasets.
- [ ] For each card, ask whether the underlying work is published. If it is under review,
      keep the card in `profiles/private/` and change nothing else.
- [ ] Never "temporarily" set a default profile to your own layer to make a demo work.
      Apply it with `scripts/use-profile.sh private` and leave `default` neutral.

## 3. Fixtures and citations — BLOCKING

- [ ] **Verify the citation in the novelty fixture.**
      `skills/time-series-model-ideation/evals/files/timekan-primary-source-excerpt.md`
      cites an ICLR paper with an OpenReview id. Open the link, confirm the paper exists
      and is the one described, and confirm every technical statement in the fixture
      matches the primary source. A fixture that misdescribes a real paper is a
      credibility problem in a repository whose thesis is citation discipline.
      *Verification status (this checkout):* **the paper's identity and the fixture's
      technical description are verified against the primary source metadata.** The
      arXiv record for 2502.06910 gives the title, the venue (ICLR 2025), the authors
      (Huang, Zhao, Li, Bai) and an official code repository, and its abstract names
      exactly the three components the fixture describes: Cascaded Frequency
      Decomposition blocks, Multi-order KAN Representation Learning blocks per frequency
      band, and Frequency Mixing blocks that recombine the bands. The **ICLR proceedings
      URL in the fixture is also confirmed correct** — its content hash resolves to the
      2025 TimeKAN paper.
      *Still needing a human:* the OpenReview forum id in the fixture cannot be checked
      from a script — the OpenReview API answers this environment with a browser
      challenge (HTTP 403), so the id needs one click-through. The fixture's numeric
      claims (for example the horizons 96–720) are not in the abstract and should be
      checked against the paper body. Neither gap invalidates the fixture, which is
      labelled synthetic and explicitly says it must not be reused as literature
      evidence, but both should be closed before publishing.
- [ ] **Decide what to do with the `2026-06-30` evidence cutoffs** in the fixtures. They
      are synthetic but read as real dates. Either keep them (they exercise the
      stale-upstream logic) with a comment stating they are synthetic, or shift them.
- [ ] **Confirm the fixtures quote no source text.** They are paraphrases today; keep
      them that way. Long verbatim excerpts from papers do not belong in this repository.
- [ ] **Confirm the fixtures carry no real evaluation data** from a real project.

## 4. Repository identity and metadata

- [x] **Owner path and repository name — verified against the live remote.** The
      repository exists at `https://github.com/tylsssss/Time-series-research-skills`, and
      both names are declared once, in `.claude-plugin/marketplace.json` (`owner.name` and
      `name`). They appear in ~20 places across 10 files, including extensionless files
      (`LICENSE`, `NOTICE`, `Makefile`). Never hand-edit them — a partial rename leaves 404
      links and a wrong attribution:
      ```bash
      scripts/set-owner.sh --show                  # owner handle and every occurrence
      scripts/set-owner.sh --slug --show            # repository name and every occurrence
      scripts/set-owner.sh --slug <new-repo-name>   # atomic rename, then re-runs lint
      ```
      `scripts/lint.mjs` L15 checks the owner, and **L18 compares the repository name in
      self-references against the git remote**, so this class of drift is caught by
      `make lint` rather than by a reader clicking a dead link. L18 warns rather than
      fails, because a fork legitimately keeps pointing at upstream.
- [x] **Commit identity — decided.** The published identity is
      **`sazhang@bjtu.edu.cn`**, and it is already wired into `CITATION.cff` (author
      email), `.claude-plugin/marketplace.json` (owner email), `CODE_OF_CONDUCT.md` and
      `SECURITY.md`. `scripts/lint.mjs` L08 allows exactly that one declared address and
      still fails on any other email in shipped content, so the decision is enforced
      rather than remembered. Set it repository-locally before the first commit:
      ```bash
      git init
      git config user.email "sazhang@bjtu.edu.cn"
      git config user.name "<the name you want in the commit log>"
      ```
      Note the tradeoff you accepted: an institutional address is permanent in public
      commit history and easy to harvest. GitHub's `<id>+<handle>@users.noreply.github.com`
      remains available if you change your mind — it is one `git config` and one edit to
      the four files above, but it cannot be changed retroactively for commits already
      pushed.
- [ ] **Confirm the GitHub handle.** `CITATION.cff`, both READMEs, the issue-template
      config, the code of conduct and this checklist reference `tylsssss` in 19 places.
      The contact address is now decided but the handle has not been verified against the
      account that will own the repository. `scripts/set-owner.sh <handle>` renames all 19
      atomically and L15 fails if they disagree.
- [ ] **Fill in `CITATION.cff`.** Add `given-names`/`family-names` (and optionally an
      ORCID) if the citation should carry the legal name, and set `date-released`. The
      author email is already set.
- [ ] **Repository description and topics.** Suggested description: *"Two Agent Skills
      that make an AI agent argue about a time-series research idea before it writes a
      model — typed claims, evidence levels, stage gates, and an explicit
      GO/PIVOT/NEED-EVIDENCE/KILL decision."* Suggested topics: `agent-skills`,
      `claude-skills`, `llm-agents`, `time-series`, `research-agents`,
      `research-methodology`, `reproducibility`, `forecasting`, `ai-for-science`.
- [ ] **Social preview image (1280×630).** `skills/*/assets/icon.svg` is a 24×24 icon,
      not a preview card. Render a preview from it rather than scaling it up.

## 5. Verification before the first push

- [ ] `node scripts/lint.mjs` — expect zero errors. The `default-profile-sync` warning
      should be absent.
- [ ] `python3 evals/run.py --self-test` — the structural grader must pass a conforming
      dossier and catch every defect in the broken one.
- [ ] `node scripts/build-bundle.mjs` — bundles build, no unresolved references.
- [ ] `bash scripts/install.sh --dry-run` — read the output; confirm the paths are the
      ones you want and that nothing is deleted.
- [ ] `bash scripts/use-profile.sh --list` and `--check`.
- [ ] Run the skill yourself once, end to end, on a real idea, and keep the dossier. It
      becomes `examples/` (sanitized) and is the single most convincing artifact for a
      skeptical reader.
- [ ] Optionally: `python3 evals/run.py --tier2 --case 1` with a key, and record the
      result in `evals/results/`. Publishing a real pass rate is on-brand.

## 6. Repository settings

- [ ] Enable **Security → Private vulnerability reporting** (referenced by
      `SECURITY.md` and `CODE_OF_CONDUCT.md`).
- [ ] Enable **Discussions** if you want a place for methodology arguments that are not
      bug reports.
- [ ] Protect `main`: require the `ci` workflow to pass, and require a pull request for
      non-maintainer changes.
- [ ] Add the CI badge to both READMEs **after** the first successful run, so the badge
      is never broken.
- [ ] Confirm Actions are enabled; `evals.yml` needs at least one provider secret to do
      anything, and skips cleanly without one.

## 7. Release mechanics

- [ ] Move the `[Unreleased]` section of `CHANGELOG.md` under `## [0.1.0] - <date>` and
      set the same date in `CITATION.cff`.
- [ ] Tag `v0.1.0` and create a GitHub release; attach `dist/*.bundle.md` from the CI
      artifacts so users without a skills mechanism can download a single file.
- [ ] Optionally archive the release with Zenodo to mint a DOI, then add it to
      `CITATION.cff` and both READMEs.
- [ ] Decide the fate of the previously installed local copy at
      `~/.agents/skills/time-series-model-ideation`, which predates this repository.
      This repository is now the source of truth: `bash scripts/install.sh --target all
      --scope user` refreshes it and backs up the old one.

## 8. Launch notes

- [ ] Lead with the failure mode, not the feature list: an agent that designs a
      Diffusion+GNN+LLM architecture on request versus one that returns `NEED-EVIDENCE`
      with the smallest diagnostic that would change the decision.
- [ ] Publish the eval table and the honest limitations section verbatim. Overclaiming in
      the announcement would contradict the artifact's own rules, which is the fastest way
      to lose the audience this is written for.
- [ ] Ask for behavioral failures specifically; they are the contribution this project
      needs most and the hardest to write.
