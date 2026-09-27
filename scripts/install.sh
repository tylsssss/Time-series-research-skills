#!/usr/bin/env bash
# Install the skills in this repository into an agent's skill directory.
#
# Safe by default: nothing is deleted, an existing installation is moved aside
# with a timestamped suffix before it is replaced, and --dry-run prints every
# action without touching the filesystem.
#
# Usage:
#   scripts/install.sh [--target claude|agents|all] [--scope user|project]
#                      [--skill NAME] [--dry-run] [--force] [--quiet]
#
# Examples:
#   scripts/install.sh --dry-run
#   scripts/install.sh --target all --scope user
#   scripts/install.sh --target claude --scope project
#   scripts/install.sh --skill time-series-model-ideation

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"

TARGET="all"
SCOPE="user"
ONLY_SKILL=""
DRY_RUN=0
FORCE=0
QUIET=0

die() { printf 'error: %s\n' "$1" >&2; exit 2; }
note() { [ "$QUIET" -eq 1 ] || printf '%s\n' "$1"; }
run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '  [dry-run] %s\n' "$*"
  else
    "$@"
  fi
}

while [ $# -gt 0 ]; do
  case "$1" in
    --target)  TARGET="${2:-}"; shift 2 ;;
    --scope)   SCOPE="${2:-}"; shift 2 ;;
    --skill)   ONLY_SKILL="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --force)   FORCE=1; shift ;;
    --quiet)   QUIET=1; shift ;;
    -h|--help) sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown argument: $1 (try --help)" ;;
  esac
done

case "$TARGET" in claude|agents|all) ;; *) die "--target must be claude, agents, or all" ;; esac
case "$SCOPE"  in user|project)       ;; *) die "--scope must be user or project" ;; esac
[ -d "$SKILLS_DIR" ] || die "no skills/ directory at $SKILLS_DIR"

# Resolve the destination roots for the requested scope.
case "$SCOPE" in
  user)
    CLAUDE_ROOT="${HOME:?}/.claude/skills"
    AGENTS_ROOT="${HOME:?}/.agents/skills"
    ;;
  project)
    CLAUDE_ROOT="$PWD/.claude/skills"
    AGENTS_ROOT="$PWD/.agents/skills"
    ;;
esac

# Collect the skills to install.
SKILLS=()
for d in "$SKILLS_DIR"/*/; do
  [ -f "$d/SKILL.md" ] || continue
  name="$(basename "$d")"
  if [ -n "$ONLY_SKILL" ] && [ "$name" != "$ONLY_SKILL" ]; then continue; fi
  SKILLS+=("$name")
done
[ "${#SKILLS[@]}" -gt 0 ] || die "no installable skill found${ONLY_SKILL:+ matching '$ONLY_SKILL'}"

STAMP="$(date +%Y%m%d-%H%M%S)"
INSTALLED=0

install_into() { # $1 = destination root, $2 = skill name
  local root="$1" name="$2" src="$SKILLS_DIR/$2" dest="$1/$2"
  note "  -> $dest"
  if [ -e "$dest" ]; then
    if [ "$FORCE" -eq 1 ]; then
      run rm -rf "$dest"
    else
      note "     existing installation found; moving to $(basename "$dest").bak-$STAMP"
      run mv "$dest" "$dest.bak-$STAMP"
    fi
  fi
  run mkdir -p "$root"
  run cp -R "$src" "$dest"
  INSTALLED=$((INSTALLED + 1))
}

note "repository: $REPO_ROOT"
note "target:     $TARGET   scope: $SCOPE$([ "$DRY_RUN" -eq 1 ] && echo '   (dry run)')"
note "skills:     ${SKILLS[*]}"
note ""

if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
  note "Claude Code skills -> $CLAUDE_ROOT"
  for name in "${SKILLS[@]}"; do install_into "$CLAUDE_ROOT" "$name"; done
  note ""
fi

if [ "$TARGET" = "agents" ] || [ "$TARGET" = "all" ]; then
  note "Agent Skills (~/.agents/skills, Codex and compatible clients) -> $AGENTS_ROOT"
  for name in "${SKILLS[@]}"; do install_into "$AGENTS_ROOT" "$name"; done
  note ""
fi

if [ "$DRY_RUN" -eq 1 ]; then
  note "dry run complete: $INSTALLED installation(s) would be performed. Nothing was written."
  exit 0
fi

note "installed $INSTALLED skill cop(y|ies)."
note ""
note "Next steps"
if [ "$TARGET" = "claude" ] || [ "$TARGET" = "all" ]; then
  note "  Claude Code: restart the session, then run /plugin marketplace add <owner>/<repo>"
  note "               to install through the marketplace entry instead of copying files."
fi
if [ "$TARGET" = "agents" ] || [ "$TARGET" = "all" ]; then
  note "  Codex and compatible clients pick up $AGENTS_ROOT automatically."
fi
note "  Personal layer: profiles apply in this repository. Run scripts/use-profile.sh <name>"
note "                  before installing if you want a profile other than the default."
note "  Verify:         node scripts/lint.mjs && python3 evals/run.py --self-test"
