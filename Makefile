# Time-series-research-skills — developer entry points.
#
# Everything here uses only python3 (3.9+) and node (18+) from the standard
# toolchain. No package installation is required or wanted.

SHELL := /bin/bash
REPO  := $(shell pwd)

.PHONY: help ci lint self-test grade bundle install-user install-project use-default use-private backup-profile owner clean

help:
	@echo "make ci               everything CI runs: lint, self-test, bundle, installer, profile swap"
	@echo "make lint             frontmatter, reference paths, profile sync, fixtures, assets, identity"
	@echo "make self-test        prove the structural grader passes a good dossier and fails a bad one"
	@echo "make grade F=file.md  structurally grade one dossier"
	@echo "make bundle           build dist/*.bundle.md for agents without a skills mechanism"
	@echo "make install-user     install both skills for the current user (Claude Code + ~/.agents/skills)"
	@echo "make install-project  install both skills into ./.claude/skills and ./.agents/skills"
	@echo "make use-default      restore the shipped default profile"
	@echo "make use-private      apply your own local (git-ignored) profile"
	@echo "make backup-profile   snapshot the current personal layer"
	@echo "make owner            show the publishing handle and every place it appears"
	@echo "make clean            remove dist/ and local eval scratch output"

lint:
	@node scripts/lint.mjs

# Everything CI runs, runnable locally before pushing. The workflow calls these
# same targets so the two definitions of "green" cannot drift apart — which is
# exactly how a stale probe profile name survived in the workflow once already.
ci: lint self-test bundle ci-installer ci-profiles ci-identity
	@echo ""
	@echo "make ci: all green"

ci-installer:
	@echo "== installer against a throwaway HOME =="
	@fake=$$(mktemp -d); \
	  HOME="$$fake" bash scripts/install.sh --target all --scope user --quiet; \
	  test -f "$$fake/.claude/skills/time-series-model-ideation/SKILL.md"; \
	  test -f "$$fake/.agents/skills/time-series-code-implementation/SKILL.md"; \
	  HOME="$$fake" bash scripts/install.sh --target agents --scope user --quiet; \
	  ls "$$fake/.agents/skills" | grep -q 'time-series-model-ideation.bak-'; \
	  rm -rf "$$fake"; \
	  echo "  installed to both roots, re-install backed up the old copy, nothing deleted"

ci-profiles:
	@echo "== profile swap round-trip =="
	@bash scripts/use-profile.sh --check >/dev/null || { \
	  echo "  make ci requires the shipped default profile; run: bash scripts/use-profile.sh default"; exit 1; }
	@rm -rf profiles/ci-probe profiles/ci-broken
	@mkdir -p profiles/ci-probe && cp profiles/default/*.md profiles/ci-probe/ \
	  && printf 'probe\n' >> profiles/ci-probe/personal-research-priors.md
	@bash scripts/use-profile.sh ci-probe >/dev/null
	@if bash scripts/use-profile.sh --check >/dev/null 2>&1; then echo "  drift was not detected"; exit 1; fi
	@bash scripts/use-profile.sh default >/dev/null
	@mkdir -p profiles/ci-broken && cp profiles/default/personal-research-priors.md profiles/ci-broken/
	@if bash scripts/use-profile.sh ci-broken >/dev/null 2>&1; then echo "  an incomplete profile was accepted"; exit 1; fi
	@rm -rf profiles/ci-probe profiles/ci-broken profiles/.active profiles/.backup
	@bash scripts/use-profile.sh --check >/dev/null
	@echo "  swap detected as drift, restored, and an incomplete profile refused"

ci-identity:
	@echo "== identity renames are no-ops on the current values =="
	@owner=$$(python3 -c 'import json;print(json.load(open(".claude-plugin/marketplace.json"))["owner"]["name"])'); \
	  slug=$$(python3 -c 'import json;print(json.load(open(".claude-plugin/marketplace.json"))["name"])'); \
	  before=$$(git status --porcelain 2>/dev/null | sort); \
	  bash scripts/set-owner.sh "$$owner" >/dev/null; \
	  bash scripts/set-owner.sh --slug "$$slug" >/dev/null; \
	  after=$$(git status --porcelain 2>/dev/null | sort); \
	  if [ "$$before" != "$$after" ]; then echo "  a no-op rename changed the working tree"; exit 1; fi; \
	  echo "  owner and repository name already correct (nothing written)"

self-test:
	@python3 evals/run.py --self-test

grade:
	@test -n "$(F)" || { echo "usage: make grade F=path/to/dossier.md"; exit 2; }
	@python3 evals/run.py --grade "$(F)"

bundle:
	@node scripts/build-bundle.mjs

install-user:
	@bash scripts/install.sh --target all --scope user

install-project:
	@bash scripts/install.sh --target all --scope project

use-default:
	@bash scripts/use-profile.sh default

use-private:
	@bash scripts/use-profile.sh private

backup-profile:
	@bash scripts/use-profile.sh --backup

owner:
	@bash scripts/set-owner.sh --show

clean:
	@rm -rf dist evals/results/*.tmp
	@echo "cleaned dist/ and eval scratch files"
