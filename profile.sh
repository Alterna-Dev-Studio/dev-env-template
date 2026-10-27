#!/usr/bin/env bash
# Source from ~/.bashrc or ~/.profile. Never prints secret values or writes plaintext files.
_dev_env_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$_dev_env_root/shell/paths.sh"
if [[ $- == *i* ]]; then
  source "$_dev_env_root/shell/aliases.sh"
fi
if [[ ${_DEV_ENV_PROFILE_LOADED-} != "$_dev_env_root" ]]; then
  if _dev_env_exports="$("$_dev_env_root/scripts/envtool" export profile)"; then
    eval "$_dev_env_exports"
    _DEV_ENV_PROFILE_LOADED=$_dev_env_root
  else
    printf 'dev-env: could not load encrypted profile\n' >&2
  fi
fi
# Set after the profile so a stored DEV_ENV_HOME cannot redirect it.
export DEV_ENV_HOME="$_dev_env_root"
unset _dev_env_root _dev_env_exports
