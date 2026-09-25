#!/usr/bin/env bash
# Starting with ClamAV v0.105, the Rust toolchain is required to compile ClamAV.
set -euo pipefail

if command -v cargo >/dev/null 2>&1 && command -v rustc >/dev/null 2>&1; then
	echo "Rust toolchain is present: $(rustc --version)"
	exit 0
fi

echo "Installing minimal Rust toolchain"
install_log="$(mktemp)"
trap 'rm -f "$install_log"' EXIT

if curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
	| sh -s -- -y --profile minimal --no-modify-path >"$install_log" 2>&1; then
	source "$HOME/.cargo/env"
	echo "Rust toolchain installed: $(rustc --version)"
else
	cat "$install_log" >&2
	echo "Failed to install the Rust toolchain required to compile ClamAV" >&2
	exit 1
fi
