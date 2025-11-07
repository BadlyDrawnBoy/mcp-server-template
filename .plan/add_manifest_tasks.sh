#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  cat <<'USAGE'
Usage: .plan/add_manifest_tasks.sh TASK_ID "Task title" [after_id[,after_id...]]

Appends a task entry to .plan/tasks.manifest.json (creating the file if necessary).
Pass a comma-separated list of task IDs as the optional third argument to express ordering dependencies.
USAGE
  exit 1
fi

mf=".plan/tasks.manifest.json"
tmp="$mf.tmp"

mkdir -p "$(dirname "$mf")"
[[ -f "$mf" ]] || echo '[]' >"$mf"

id="$1"
title="$2"
after_csv="${3:-}"

after=$(jq -Rc '
  if length == 0 then []
  else split(",")
    | map(gsub("^\\s+|\\s+$"; ""))
    | map(select(length > 0))
  end
' <<<"$after_csv")

jq --arg id "$id" --arg title "$title" --argjson after "$after" '
  if any(.[]; .id == $id) then .
  else . + [{ "id": $id, "title": $title, "after": $after }]
  end
' "$mf" >"$tmp" && mv "$tmp" "$mf"

echo "Added $id to $mf"

