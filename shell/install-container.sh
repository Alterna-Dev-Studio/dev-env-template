#!/usr/bin/env bash
# Install only the mounted shell fragments in an explicitly opted-in devcontainer.
set -euo pipefail

shell_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
block=$(cat <<EOF
# >>> dev-env shell (managed by install-container.sh) >>>
if [ -f "$shell_dir/paths.sh" ]; then . "$shell_dir/paths.sh"; fi
case \$- in *i*) [ -f "$shell_dir/aliases.sh" ] && . "$shell_dir/aliases.sh" ;; esac
# <<< dev-env shell <<<
EOF
)

install_block() {
  local rc=$1 placement=$2 temp
  touch "$rc"
  if grep -Fq '# >>> dev-env shell (managed by install-container.sh) >>>' "$rc"; then
    return 0
  fi
  temp=$(mktemp "${rc}.dev-env.XXXXXX")
  if [[ $placement == first ]]; then
    printf '%s\n' "$block" > "$temp"
    cat "$rc" >> "$temp"
  else
    cat "$rc" > "$temp"
    printf '\n%s\n' "$block" >> "$temp"
  fi
  chmod --reference="$rc" "$temp"
  mv -- "$temp" "$rc"
}

# Ubuntu's .bashrc returns early in non-interactive shells; place this first.
install_block "$HOME/.bashrc" first
install_block "$HOME/.profile" last
printf 'Installed dev-env shell fragments for %s\n' "$HOME"
