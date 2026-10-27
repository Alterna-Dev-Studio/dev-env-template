# Taiga Listing Pagination

Taiga's list endpoints paginate at 30 rows and return page 1 silently. The `list_*` MCP tools (`list_user_stories`, `list_epics`, `list_issues`, `list_tasks`) expose no header control and give no marker that more pages exist. Once a collection exceeds 30 rows, any client-side filter over a single call runs over page 1 only and silently under-selects.

**Rule: NEVER filter a Taiga listing client-side without either a server-side filter covering the condition or a full page loop.**

## Option 1: Server-side filter (preferred)

Push the condition into `filters` so Taiga does the narrowing. Filter keys are endpoint-specific:

| MCP tool | Server-side filter keys |
|---|---|
| `list_epics` | `status`, `status__is_closed`, `tags`, `assigned_to` |
| `list_user_stories` | `epic`, `milestone`, `status`, `status__is_closed`, `tags`, `assigned_to` |
| `list_tasks` | `user_story`, `milestone`, `status`, `status__is_closed`, `tags`, `assigned_to` |
| `list_issues` | `status`, `status__is_closed`, `type`, `severity`, `priority`, `tags`, `assigned_to` |

`project` is always applied via the tool's `project_id` argument. Use `status__is_closed: false` to select "everything still open" — do NOT pick a single `status` ID for that, since open items usually span several statuses.

```
list_user_stories(project_id=<verified-project-id>, filters={"epic": <epic_internal_id>, "status": <verified-status-id>, "tags": "llm-analyzed"})
list_epics(project_id=<verified-project-id>, filters={"status__is_closed": false})
list_tasks(project_id=<verified-project-id>, filters={"user_story": <story_id>, "tags": ["design"]})
```

A filter key Taiga does not honour is ignored silently rather than erroring, so always re-check the same conditions client-side on whatever comes back. If the result count is exactly 30, you MUST still page (Option 2) — a server-side filter narrows the collection but does not disable pagination.

## Option 2: Page loop

1. Make the first call with your filters. Keep the results.
2. If the call returned exactly 30 rows, repeat with `filters={..., "page": N}` starting at `N = 2`, appending each page's rows.
3. Stop when either:
   - a page returns fewer than 30 rows, **or**
   - the call fails with `API Error 404: Page is not 'last'`. **This 404 means "no more pages", not a broken call** — use what you have. Do not retry and do not abort the skill.

## Raw REST callers

Scripts calling the REST API directly (curl, `scripts/*.py`) can send the `x-disable-pagination: True` header to receive the full collection in one response, or follow the `x-pagination-next` response header page by page.

## Summary

- `list_*` MCP tools silently return only page 1 (30 rows)
- Prefer server-side filters, then re-check client-side
- Exactly 30 rows returned means page again, never proceed
- `API Error 404: Page is not 'last'` is end-of-data, not an error
