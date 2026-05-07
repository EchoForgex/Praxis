#!/bin/bash
set -euo pipefail

if [ -z "${1:-}" ]; then
  echo "Usage: $0 <skill-name>"
  echo "Example: $0 status"
  echo ""
  echo "Available skills:"
  ls skills/*.md 2>/dev/null | sed 's|skills/||;s|\.md||' | sed 's/^/  /'
  exit 1
fi

SKILL="$1"
SRC="skills/${SKILL}.md"
DEST="${HOME}/.claude/skills/${SKILL}.md"

if [ ! -f "$SRC" ]; then
  echo "Error: ${SRC} does not exist"
  exit 1
fi

mkdir -p "${HOME}/.claude/skills"

cp "$SRC" "$DEST"

SRC_SUM=$(md5 -q "$SRC" 2>/dev/null || md5sum "$SRC" | awk '{print $1}')
DEST_SUM=$(md5 -q "$DEST" 2>/dev/null || md5sum "$DEST" | awk '{print $1}')

if [ "$SRC_SUM" != "$DEST_SUM" ]; then
  echo "Error: checksum mismatch after copy"
  exit 1
fi

echo "Promoted ${SKILL} → ${DEST}"
echo "Checksum: ${SRC_SUM}"
