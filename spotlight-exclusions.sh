#!/usr/bin/env bash

set -u

if [[ -z "${HOME:-}" ]]; then
  echo "HOME is not set" >&2
  exit 1
fi

directories=(
  "$HOME/github"
  "$HOME/freelance"
  "$HOME/tmp"
  "$HOME/esp"
  "$HOME/Library/Developer"
  "$HOME/Library/Application Support/Zed"
  "$HOME/Library/Application Support/Claude"
  "$HOME/Library/Containers/com.docker.docker/Data"
)

for directory in "$HOME/Library/Group Containers/"*.orbstack/data; do
  [[ -d "$directory" ]] && directories+=("$directory")
done

added=0
existing=0
skipped=0
failed=0

for directory in "${directories[@]}"; do
  marker="$directory/.metadata_never_index"

  if [[ ! -d "$directory" ]]; then
    printf 'skipped: %s does not exist\n' "$directory"
    skipped=$((skipped + 1))
  elif [[ -e "$marker" || -L "$marker" ]]; then
    printf 'already excluded: %s\n' "$directory"
    existing=$((existing + 1))
  elif touch "$marker"; then
    printf 'added: %s\n' "$directory"
    added=$((added + 1))
  else
    printf 'failed: %s\n' "$directory" >&2
    failed=$((failed + 1))
  fi
done

printf '\nAdded: %d, already excluded: %d, skipped: %d, failed: %d\n' \
  "$added" "$existing" "$skipped" "$failed"

[[ "$failed" -eq 0 ]]
