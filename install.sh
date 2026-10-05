#!/usr/bin/env bash
# Installs every skill in skills/ of this repository into a Claude Code skills folder.
#
# Usage:
#   ./install.sh                  Installs globally, into ~/.claude/skills
#   ./install.sh /path/to/project Installs scoped to one project, into
#                                  /path/to/project/.claude/skills
#
# Safe to re-run: each skill folder is overwritten with the version in
# this bundle, so re-running after pulling an updated version brings an
# existing install up to date.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"

if [ "${1:-}" != "" ]; then
  DEST="${1%/}/.claude/skills"
  SCOPE="project ($1)"
else
  DEST="$HOME/.claude/skills"
  SCOPE="global (all projects)"
fi

mkdir -p "$DEST"

echo "Installing skills from: $SCRIPT_DIR"
echo "Installing into:        $DEST"
echo "Scope:                  $SCOPE"
echo

installed=0
skipped=0

for dir in "$SCRIPT_DIR"/*/; do
  name="$(basename "$dir")"

  # Only treat it as a skill if it has a SKILL.md — this future-proofs
  # the script against any non-skill folders added to the bundle later.
  if [ ! -f "${dir}SKILL.md" ]; then
    skipped=$((skipped + 1))
    continue
  fi

  rm -rf "${DEST:?}/${name:?}"
  cp -R "$dir" "$DEST/$name"
  echo "  + $name"
  installed=$((installed + 1))
done

echo
echo "Done: $installed skill(s) installed, $skipped non-skill folder(s) skipped."
echo "Restart Claude Code (or start a new session) to pick them up."
