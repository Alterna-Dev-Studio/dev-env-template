#!/usr/bin/env bash
# Copied from Alterna-Dev-Studio/you-thon fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1 scripts/taiga-story.sh (consumer-owned helper); project default changed to 4.
# Since changed: works through Pangolin via taiga-session, keeps credentials out of argv, and
# writes only to a private temporary directory.
# ABOUTME: Fetch a Taiga item (user story, issue, or epic) by ref number using the REST API directly.
# ABOUTME: Uses /by_ref endpoint for O(1) lookup — no pagination needed.

set -euo pipefail

usage() {
    echo "Usage: $0 <ref> [project_id] [--issue] [--epic] [--with-tasks]"
    echo "  ref          Item ref number (as shown in Taiga UI)"
    echo "  project_id   Taiga project ID (default: 4)"
    echo "  --issue      Look up an issue instead of a user story"
    echo "  --epic       Look up an epic instead of a user story"
    echo "  --with-tasks Also fetch and include the task list (user stories only)"
    echo ""
    echo "Env vars required: TAIGA_API_URL, TAIGA_USERNAME, TAIGA_PASSWORD"
    echo "Behind Pangolin, also the PANGOLIN_* settings read by taiga-session."
    echo ""
    echo "Output: compact JSON with id, ref, subject, description, status, status_extra_info, milestone, milestone_name, milestone_slug, tags, is_closed"
    echo "        (plus 'tasks' array when --with-tasks is used)"
    echo ""
    echo "Exit codes: 0 success, 44 item not found (404), 1 any other error"
    exit 1
}

REF="${1:-}"
# Only a numeric second argument is a project ID; a flag in that position keeps the default.
if [[ "${2:-}" =~ ^[0-9]+$ ]]; then
    PROJECT_ID="$2"
else
    PROJECT_ID=4
fi
ITEM_TYPE="userstories"
WITH_TASKS=false

for arg in "$@"; do
    if [[ "$arg" == "--issue" ]]; then
        ITEM_TYPE="issues"
    elif [[ "$arg" == "--epic" ]]; then
        ITEM_TYPE="epics"
    elif [[ "$arg" == "--with-tasks" ]]; then
        WITH_TASKS=true
    fi
done

[[ -z "$REF" ]] && usage

: "${TAIGA_API_URL:?TAIGA_API_URL is required}"
: "${TAIGA_USERNAME:?TAIGA_USERNAME is required}"
: "${TAIGA_PASSWORD:?TAIGA_PASSWORD is required}"

TMPDIR_SCRIPT=$(mktemp -d)
chmod 700 "$TMPDIR_SCRIPT"
trap 'rm -rf "$TMPDIR_SCRIPT"' EXIT

# Pangolin session cookies (an empty jar when Taiga is reached directly). The dev-env copy
# finds taiga-session beside it; a project copy uses $DEV_ENV_HOME's.
COOKIES="$TMPDIR_SCRIPT/cookies.txt"
SESSION_HELPER="$(dirname -- "${BASH_SOURCE[0]}")/taiga-session"
[[ -x "$SESSION_HELPER" ]] || SESSION_HELPER="${DEV_ENV_HOME:-}/scripts/taiga-session"
if [[ -x "$SESSION_HELPER" ]]; then
    "$SESSION_HELPER" --cookie-jar "$COOKIES" || exit 1
elif [[ -n "${PANGOLIN_SESSION_TOKEN:-}${PANGOLIN_RESOURCE_TOKEN:-}" ]]; then
    echo "Pangolin is configured but taiga-session was not found; set DEV_ENV_HOME or run dv update" >&2
    exit 1
else
    printf '# Netscape HTTP Cookie File\n' > "$COOKIES"
fi

# Run curl with the session cookies; no HTTP response at all (DNS, refused, timeout) exits 1.
taiga_curl() {
    local label="$1" rc=0
    shift
    curl -sS -b "$COOKIES" "$@" || rc=$?
    if [[ "$rc" -ne 0 ]]; then
        echo "Taiga $label request failed (curl exit $rc)" >&2
        exit 1
    fi
}

# Authenticate. The password travels on stdin, never in argv.
HTTP_CODE=$(python3 -c 'import json, os; print(json.dumps({"type": "normal", "username": os.environ["TAIGA_USERNAME"], "password": os.environ["TAIGA_PASSWORD"]}))' |
    taiga_curl "auth" -o "$TMPDIR_SCRIPT/auth.json" -w "%{http_code}" -X POST "${TAIGA_API_URL}/api/v1/auth" \
        -H "Content-Type: application/json" --data-binary @-) || exit 1
if [[ "$HTTP_CODE" -ne 200 ]]; then
    echo "Taiga auth failed: HTTP $HTTP_CODE" >&2
    [[ "$HTTP_CODE" -eq 401 && ! -s "$TMPDIR_SCRIPT/auth.json" ]] &&
        echo "An empty 401 is Pangolin refusing the request; check the PANGOLIN_* settings or run dv taiga-login" >&2
    exit 1
fi
# The bearer token reaches curl through a file descriptor, never argv.
python3 -c 'import json, sys; print("Authorization: Bearer " + json.load(open(sys.argv[1]))["auth_token"])' \
    "$TMPDIR_SCRIPT/auth.json" > "$TMPDIR_SCRIPT/auth-header"

# Fetch item by ref using dedicated by_ref endpoint (O(1), no pagination)
HTTP_CODE=$(taiga_curl "item" -o "$TMPDIR_SCRIPT/item.json" -w "%{http_code}" \
    "${TAIGA_API_URL}/api/v1/${ITEM_TYPE}/by_ref?project=${PROJECT_ID}&ref=${REF}" \
    -H "@$TMPDIR_SCRIPT/auth-header") || exit 1

if [[ "$HTTP_CODE" -eq 404 ]]; then
    ITEM_LABEL="user story"
    [[ "$ITEM_TYPE" == "issues" ]] && ITEM_LABEL="issue"
    [[ "$ITEM_TYPE" == "epics" ]] && ITEM_LABEL="epic"
    echo "No ${ITEM_LABEL} found with ref #${REF} in project ${PROJECT_ID}" >&2
    exit 44
fi

if [[ "$HTTP_CODE" -ne 200 ]]; then
    echo "Taiga API error: HTTP $HTTP_CODE" >&2
    cat "$TMPDIR_SCRIPT/item.json" >&2
    exit 1
fi

STORY_ID=$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["id"])' "$TMPDIR_SCRIPT/item.json")

# Optionally fetch tasks (user stories only)
echo "null" > "$TMPDIR_SCRIPT/tasks_compact.json"
if [[ "$WITH_TASKS" == true && "$ITEM_TYPE" == "userstories" ]]; then
    HTTP_CODE=$(taiga_curl "tasks" -o "$TMPDIR_SCRIPT/tasks.json" -w "%{http_code}" \
        "${TAIGA_API_URL}/api/v1/tasks?project=${PROJECT_ID}&user_story=${STORY_ID}" \
        -H "@$TMPDIR_SCRIPT/auth-header") || exit 1
    if [[ "$HTTP_CODE" -ne 200 ]]; then
        echo "Taiga API error fetching tasks: HTTP $HTTP_CODE" >&2
        exit 1
    fi
    python3 -c "
import json, sys
tasks = json.load(open(sys.argv[1]))
compact = [{
    'id': t['id'],
    'ref': t['ref'],
    'subject': t['subject'],
    'status': t['status'],
    'status_extra_info': t['status_extra_info'],
    'is_closed': t['is_closed'],
} for t in tasks]
open(sys.argv[2], 'w').write(json.dumps(compact))
" "$TMPDIR_SCRIPT/tasks.json" "$TMPDIR_SCRIPT/tasks_compact.json"
fi

python3 -c "
import json, sys
d = json.load(open(sys.argv[1]))
tasks = json.load(open(sys.argv[2]))
out = {
    'id': d.get('id'),
    'ref': d.get('ref'),
    'subject': d.get('subject'),
    'description': d.get('description'),
    'status': d.get('status'),
    'status_extra_info': d.get('status_extra_info'),
    'milestone': d.get('milestone'),
    'milestone_name': d.get('milestone_name'),
    'milestone_slug': d.get('milestone_slug'),
    'tags': d.get('tags'),
    'is_closed': d.get('is_closed'),
}
if tasks is not None:
    out['tasks'] = tasks
print(json.dumps(out, indent=2))
" "$TMPDIR_SCRIPT/item.json" "$TMPDIR_SCRIPT/tasks_compact.json"
