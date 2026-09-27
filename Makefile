# Time-series-research-skills — developer entry points.
#
# Everything here uses only python3 (3.9+) and node (18+) from the standard
# toolchain. No package installation is required or wanted.

SHELL := /bin/bash
REPO  := $(shell pwd)

.PHONY: help lint self-test grade bundle install-user install-project use-default use-private backup-profile owner clean

help:
	@echo "make lint             frontmatter, reference paths, profile sync, fixtures, assets, owner"
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
