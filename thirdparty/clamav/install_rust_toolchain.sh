#!/usr/bin/env bash
set -euo pipefail

case ":$PATH:" in
	*":$HOME/.cargo/bin:"*) ;;
	*) export PATH="$HOME/.cargo/bin:$PATH" ;;
esac

if command -v cargo >/dev/null 2>&1 && command -v rustc >/dev/null 2>&1; then
	echo "Rust toolchain already installed"
	exit 0
fi

echo "Installing Rust toolchain..."
install_log="$(mktemp)"
trap 'rm -f "$install_log"' EXIT
if ! curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
	2>"$install_log" \
	| sh -s -- -y --profile minimal --default-toolchain stable >>"$install_log" 2>&1; then
	cat "$install_log" >&2
	echo "ERROR: Rust toolchain installation failed." >&2
	exit 1
fi

if ! command -v cargo >/dev/null 2>&1 || ! command -v rustc >/dev/null 2>&1; then
	echo "ERROR: Rust installation completed, but cargo or rustc is unavailable." >&2
	exit 1
fi

echo "Rust toolchain ready: $(rustc --version)"
