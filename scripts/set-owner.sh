#!/usr/bin/env bash
# Rename the project's published identity everywhere it self-references.
#
# Two names identify this project, both declared in
# `.claude-plugin/marketplace.json`:
#
#   owner.name  the GitHub account   -> self-referencing URLs, CODE_OF_CONDUCT
#   name        the repository name  -> URLs, README title, CITATION, NOTICE, LICENSE
#
# Either one appears in roughly twenty places across ten files, including
# extensionless files (LICENSE, NOTICE, Makefile). A partial rename produces 404
# links and a wrong attribution, and it stays invisible until someone clicks. So
# both renames are atomic here, and `scripts/lint.mjs` checks the result: L15 for
# the owner, L18 for the repository name against the git remote.
#
# Usage:
#   scripts/set-owner.sh --show                  owner handle and every occurrence
#   scripts/set-owner.sh <github-handle>         rename the owner
#   scripts/set-owner.sh --slug --show           repository name and occurrences
#   scripts/set-owner.sh --slug <repo-name>      rename the repository name
#
# Options: --dry-run, --no-verify

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$REPO_ROOT/.claude-plugin/marketplace.json"

die() { printf 'error: %s\n' "$1" >&2; exit 2; }

declared() { # $1 = owner | name
  python3 - "$MANIFEST" "$1" <<'PY'
import json, sys
manifest = json.load(open(sys.argv[1]))
print(manifest["owner"]["name"] if sys.argv[2] == "owner" else manifest["name"])
PY
}

# Rewrite one literal string across every text file of the project. The file list
# comes from git when available, so ignored paths (profiles/private, dist) are
# never touched; otherwise fall back to a filtered walk.
rewrite() { # $1 = old, $2 = new, $3 = dry(0|1)
  python3 - "$REPO_ROOT" "$1" "$2" "$3" <<'PY'
import os, subprocess, sys
root, old, new, dry = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == "1"
extensionless = {"LICENSE", "NOTICE", "Makefile"}
exts = (".md", ".json", ".cff", ".yml", ".yaml", ".mjs", ".sh", ".py", ".txt")

def candidates():
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True,
                             text=True, check=True).stdout.split()
        if out:
            return out, True
    except Exception:
        pass
    skip = {"dist", ".git", "node_modules", ".backup", "private", "__pycache__"}
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            found.append(os.path.relpath(os.path.join(dirpath, name), root))
    return found, False

changed = []
files, from_git = candidates()
for rel in files:
    base = os.path.basename(rel)
    if not (rel.endswith(exts) or base in extensionless):
        continue
    path = os.path.join(root, rel)
    try:
        text = open(path, encoding="utf-8").read()
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        continue
    count = text.count(old)
    if not count:
        continue
    changed.append((rel, count))
    if not dry:
        open(path, "w", encoding="utf-8").write(text.replace(old, new))
for rel, count in sorted(changed):
    print(f"  {'would rewrite' if dry else 'rewrote'}  {rel}  ({count})")
print(f"{'would change' if dry else 'changed'} {len(changed)} file(s), "
      f"{sum(c for _, c in changed)} occurrence(s) "
      f"[file list from {'git' if from_git else 'filesystem walk'}]")
PY
}

show() { # $1 = owner | name
  local kind="$1" value
  value="$(declared "$kind")"
  if [ "$kind" = "owner" ]; then printf 'declared owner:  %s\n' "$value"
  else printf 'declared repo:   %s\n' "$value"; fi
  if git -C "$REPO_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
    printf 'git remote:      %s\n' "$(git -C "$REPO_ROOT" config --get remote.origin.url 2>/dev/null || echo '(none configured)')"
  fi
  printf 'occurrences (counted per occurrence, matching the rewrite):\n'
  ( cd "$REPO_ROOT" && grep -ro "$value" . \
      --include='*.md' --include='*.json' --include='*.cff' --include='*.yml' --include='*.yaml' \
      --include='LICENSE' --include='NOTICE' --include='Makefile' \
      --exclude-dir=dist --exclude-dir=.git --exclude-dir=private --exclude-dir=.backup \
      | sed 's|^\./||' | awk -F: '{count[$1]++} END {for (f in count) printf "  %-52s %d\n", f, count[f]}' | sort ) || true
}

KIND=owner
if [ "${1:-}" = "--slug" ]; then KIND=name; shift; fi

if [ $# -eq 0 ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,21p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 0
fi
if [ "$1" = "--show" ]; then show "$KIND"; exit 0; fi

NEW="$1"; shift
DRY=0; VERIFY=1
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)   DRY=1; shift ;;
    --no-verify) VERIFY=0; shift ;;
    *) die "unknown argument: $1" ;;
  esac
done

if [ "$KIND" = "owner" ]; then
  # GitHub usernames: alphanumerics and single hyphens, no leading or trailing hyphen.
  case "$NEW" in *[!A-Za-z0-9-]*|"") die "not a valid GitHub handle: '$NEW'" ;; esac
  case "$NEW" in -*|*-) die "handle may not start or end with a hyphen: '$NEW'" ;; esac
else
  # Repository names also allow dots and underscores.
  case "$NEW" in *[!A-Za-z0-9._-]*|"") die "not a valid repository name: '$NEW'" ;; esac
fi

OLD="$(declared "$KIND")"
if [ "$OLD" = "$NEW" ]; then
  printf '%s is already "%s"; nothing to do\n' "$KIND" "$NEW"
  exit 0
fi

printf 'renaming %s: %s -> %s\n' "$KIND" "$OLD" "$NEW"
[ "$DRY" -eq 1 ] && printf '(dry run: no file will be written)\n'
rewrite "$OLD" "$NEW" "$DRY"

if [ "$DRY" -eq 0 ] && [ "$VERIFY" -eq 1 ]; then
  printf '\nverifying:\n'
  node "$REPO_ROOT/scripts/lint.mjs" | tail -3
  printf '\nnext: review the diff, rename the repository on GitHub as well, then\n'
  printf 'confirm with: bash scripts/set-owner.sh %s--show\n' "$([ "$KIND" = name ] && echo '--slug ' || true)"
fi
