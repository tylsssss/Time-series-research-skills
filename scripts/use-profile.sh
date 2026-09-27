#!/usr/bin/env bash
# Manage the personal layer: the six personal-*.md slots that the skills read.
#
# A profile is a complete replacement for all six slots. Swapping is reversible:
# the current slot contents are copied to profiles/.backup/<timestamp>/ first.
#
# Usage:
#   scripts/use-profile.sh --list            list profiles and the active one
#   scripts/use-profile.sh --check           exit 1 if the slots differ from profiles/default
#   scripts/use-profile.sh --backup          snapshot the current slots only
#   scripts/use-profile.sh <name> [--dry-run] apply <name> to the live slots

set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILES_DIR="$REPO_ROOT/profiles"
ACTIVE_FILE="$PROFILES_DIR/.active"

IDEATION="$REPO_ROOT/skills/time-series-model-ideation/references"
IMPL="$REPO_ROOT/skills/time-series-code-implementation/references"

# The six slots, as "<source-file-in-profile>:<live-path>".
SLOT_TARGETS=(
  "personal-research-priors.md:$IDEATION/personal-research-priors.md"
  "personal-pattern-index.md:$IDEATION/personal-pattern-index.md"
  "personal-pattern-card-a.md:$IDEATION/personal-pattern-card-a.md"
  "personal-pattern-card-b.md:$IDEATION/personal-pattern-card-b.md"
  "personal-pattern-card-c.md:$IDEATION/personal-pattern-card-c.md"
  "personal-code-style.md:$IMPL/personal-code-style.md"
)

die() { printf 'error: %s\n' "$1" >&2; exit 2; }
exists_profile() { [ -d "$PROFILES_DIR/$1" ]; }

list_profiles() {
  printf 'available profiles:\n'
  for d in "$PROFILES_DIR"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    [ "$name" = ".backup" ] && continue
    marker=""
    [ -f "$ACTIVE_FILE" ] && [ "$(cat "$ACTIVE_FILE")" = "$name" ] && marker=" (active)"
    first_line="$(grep -m1 -E '^[A-Za-z].*' "$d/personal-research-priors.md" 2>/dev/null | cut -c1-72 || true)"
    printf '  %-12s%s\n' "$name" "$marker"
    [ -n "$first_line" ] && printf '               %s\n' "$first_line"
  done
  if [ ! -f "$ACTIVE_FILE" ]; then
    printf '\nno profile recorded in profiles/.active; the slots hold whatever is committed.\n'
  fi
}

validate_profile() { # $1 = profile name
  local name="$1" dir="$PROFILES_DIR/$1" missing=() extra=()
  for slot in "${SLOT_TARGETS[@]}"; do
    [ -f "$dir/${slot%%:*}" ] || missing+=("${slot%%:*}")
  done
  for f in "$dir"/*; do
    [ -f "$f" ] || continue
    local base; base="$(basename "$f")"
    local known=0
    for slot in "${SLOT_TARGETS[@]}"; do [ "${slot%%:*}" = "$base" ] && known=1; done
    [ "$known" -eq 0 ] && extra+=("$base")
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    printf 'error: profile "%s" is incomplete; missing:\n' "$name" >&2
    printf '  %s\n' "${missing[@]}" >&2
    printf 'A profile must replace all six slots; a half-swapped layer contradicts itself.\n' >&2
    return 1
  fi
  if [ "${#extra[@]}" -gt 0 ]; then
    printf 'note: profile "%s" contains files that are not slots (ignored):\n' "$name" >&2
    printf '  %s\n' "${extra[@]}" >&2
  fi
  return 0
}

backup_slots() { # $1 = label
  local label="${1:-manual}" stamp dir
  stamp="$(date +%Y%m%d-%H%M%S)"
  dir="$PROFILES_DIR/.backup/$stamp-$label"
  mkdir -p "$dir"
  for slot in "${SLOT_TARGETS[@]}"; do
    local live="${slot#*:}"
    [ -f "$live" ] && cp "$live" "$dir/${slot%%:*}"
  done
  printf 'backed up current slots to %s\n' "${dir#"$REPO_ROOT"/}"
}

check_sync() {
  local drift=0
  if [ ! -d "$PROFILES_DIR/default" ]; then
    printf 'error: profiles/default is missing\n' >&2
    return 1
  fi
  for slot in "${SLOT_TARGETS[@]}"; do
    local src="$PROFILES_DIR/default/${slot%%:*}" live="${slot#*:}"
    if [ ! -f "$live" ]; then
      printf 'error: live slot missing: %s\n' "${live#"$REPO_ROOT"/}" >&2; drift=1; continue
    fi
    if ! cmp -s "$src" "$live"; then
      printf 'warning: %s differs from profiles/default (%s)\n' \
        "${live#"$REPO_ROOT"/}" "${slot%%:*}" >&2
      drift=1
    fi
  done
  if [ "$drift" -eq 0 ]; then
    printf 'personal layer matches profiles/default\n'
    return 0
  fi
  printf 'If this is your own profile, do not commit it. Restore with: scripts/use-profile.sh default\n' >&2
  return 1
}

apply_profile() { # $1 = name, $2 = dry-run
  local name="$1" dry="$2"
  exists_profile "$name" || die "no such profile: $name (try --list)"
  [ "$name" = ".backup" ] && die "'.backup' is not a profile"
  validate_profile "$name" || exit 2
  if [ "$dry" -eq 0 ]; then backup_slots "before-$name"; fi
  for slot in "${SLOT_TARGETS[@]}"; do
    local src="$PROFILES_DIR/$name/${slot%%:*}" live="${slot#*:}"
    if [ "$dry" -eq 1 ]; then
      printf '  [dry-run] %s -> %s\n' "${src#"$REPO_ROOT"/}" "${live#"$REPO_ROOT"/}"
    else
      cp "$src" "$live"
    fi
  done
  if [ "$dry" -eq 0 ]; then
    printf '%s' "$name" > "$ACTIVE_FILE"
    printf 'applied profile "%s" to the six slots\n' "$name"
    printf 'installed copies are not updated automatically; re-run scripts/install.sh to push this profile out.\n'
  else
    printf 'dry run: profile "%s" not applied\n' "$name"
  fi
}

case "${1:-}" in
  ""|-h|--help) sed -n '2,12p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  --list)   list_profiles ;;
  --check)  check_sync ;;
  --backup) backup_slots "manual" ;;
  --dry-run)
    [ -n "${2:-}" ] || die "--dry-run needs a profile name"
    apply_profile "$2" 1 ;;
  *)
    name="$1"; shift || true
    dry=0
    while [ $# -gt 0 ]; do
      case "$1" in --dry-run) dry=1; shift ;; *) die "unknown argument: $1" ;; esac
    done
    apply_profile "$name" "$dry" ;;
esac
