#!/usr/bin/env bash
# Source from ~/.bashrc. Never prints secret values or writes plaintext files.
_dev_env_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if _dev_env_exports="$("$_dev_env_root/scripts/envtool" export profile)"; then
  eval "$_dev_env_exports"
else
  printf 'dev-env: could not load encrypted profile\n' >&2
fi
unset _dev_env_root _dev_env_exports
