#!/usr/bin/env bash
# Source in Bash login and interactive shells, including opted-in devcontainers.

_dev_env_prepend_path() {
  local entry=$1 part
  local -a current=() remaining=()
  [[ -d $entry ]] || return 0
  IFS=: read -r -a current <<< "${PATH-}"
  for part in "${current[@]}"; do
    [[ $part == "$entry" ]] || remaining+=("$part")
  done
  PATH=$entry
  for part in "${remaining[@]}"; do PATH+=":$part"; done
  export PATH
}

export VOLTA_HOME="${VOLTA_HOME:-$HOME/.volta}"
export VOLTA_FEATURE_PNPM="${VOLTA_FEATURE_PNPM:-1}"
export PNPM_HOME="${PNPM_HOME:-$HOME/.local/share/pnpm}"
export FLYCTL_INSTALL="${FLYCTL_INSTALL:-$HOME/.fly}"

# Add in reverse order so user scripts in ~/.local/bin win, including Herdr and Collie.
_dev_env_prepend_path /go/bin
_dev_env_prepend_path /usr/local/go/bin
_dev_env_prepend_path "$HOME/.dotnet/tools"
_dev_env_prepend_path "$HOME/go/bin"
_dev_env_prepend_path "$FLYCTL_INSTALL/bin"
_dev_env_prepend_path "$PNPM_HOME"
_dev_env_prepend_path "$VOLTA_HOME/bin"
_dev_env_prepend_path "$HOME/bin"
_dev_env_prepend_path "$HOME/.local/bin"
unset -f _dev_env_prepend_path
