#!/usr/bin/env bash
# Copied from Alterna-Dev-Studio/you-thon fbc5ee32283b2e9a34147c5e2d05fce1819a0dd1 scripts/taiga-comment.sh (consumer-owned helper).
# Since changed: works through Pangolin via taiga-session and keeps credentials and the
# comment body out of argv.
# ABOUTME: Post a comment on a Taiga issue or user story using the REST API directly.
# ABOUTME: PATCHes the user story/issue item endpoint with the `comment` field (and current version).

set -euo pipefail

TMPDIR_SCRIPT=$(mktemp -d)
chmod 700 "$TMPDIR_SCRIPT"
trap 'rm -rf "$TMPDIR_SCRIPT"' EXIT

usage() {
    echo "Usage: $0 <item-id> <comment> [--issue]"
    echo "  item-id    Taiga internal ID (not ref number)"
    echo "  comment    Comment text (markdown supported)"
    echo "  --issue    Comment on an issue (default: user story)"
    echo ""
    echo "Env vars required: TAIGA_API_URL, TAIGA_USERNAME, TAIGA_PASSWORD"
    echo "Behind Pangolin, also the PANGOLIN_* settings read by taiga-session."
    echo ""
    echo "Output: Human-readable message including HTTP status code (200 = success)"
    exit 1
}

ITEM_ID="${1:-}"
COMMENT="${2:-}"
ITEM_TYPE="userstories"

for arg in "$@"; do
    if [[ "$arg" == "--issue" ]]; then
        ITEM_TYPE="issues"
    fi
done

[[ -z "$ITEM_ID" ]] && usage
[[ -z "$COMMENT" ]] && usage

: "${TAIGA_API_URL:?TAIGA_API_URL is required}"
: "${TAIGA_USERNAME:?TAIGA_USERNAME is required}"
: "${TAIGA_PASSWORD:?TAIGA_PASSWORD is required}"

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
        echo "An empty 401 is Pangolin refusing the request; check the PANGOLIN_* settings or run pangolin-login" >&2
    exit 1
fi
# The bearer token reaches curl through a file descriptor, never argv.
python3 -c 'import json, sys; print("Authorization: Bearer " + json.load(open(sys.argv[1]))["auth_token"])' \
    "$TMPDIR_SCRIPT/auth.json" > "$TMPDIR_SCRIPT/auth-header"

# Get current version (required for PATCH)
HTTP_CODE=$(taiga_curl "item" -o "$TMPDIR_SCRIPT/item.json" -w "%{http_code}" \
    "${TAIGA_API_URL}/api/v1/${ITEM_TYPE}/${ITEM_ID}" \
    -H "@$TMPDIR_SCRIPT/auth-header") || exit 1

if [[ "$HTTP_CODE" -ne 200 ]]; then
    echo "Failed to fetch item: HTTP $HTTP_CODE" >&2
    exit 1
fi

# Build the JSON payload with the comment from the environment and send it on stdin.
HTTP_CODE=$(COMMENT="$COMMENT" python3 -c '
import json, os, sys
version = json.load(open(sys.argv[1]))["version"]
print(json.dumps({"comment": os.environ["COMMENT"], "version": version}))
' "$TMPDIR_SCRIPT/item.json" |
    taiga_curl "comment" -o "$TMPDIR_SCRIPT/response.json" -w "%{http_code}" \
        -X PATCH "${TAIGA_API_URL}/api/v1/${ITEM_TYPE}/${ITEM_ID}" \
        -H "@$TMPDIR_SCRIPT/auth-header" \
        -H "Content-Type: application/json" \
        --data-binary @-) || exit 1

if [[ "$HTTP_CODE" -ne 200 ]]; then
    echo "Failed to post comment: HTTP $HTTP_CODE" >&2
    cat "$TMPDIR_SCRIPT/response.json" >&2
    exit 1
fi

echo "Comment posted successfully (HTTP $HTTP_CODE)"
