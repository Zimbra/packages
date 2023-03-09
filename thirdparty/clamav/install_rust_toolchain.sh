#Script to install Rust toolchain. Starting with ClamAV v0.105, the Rust toolchain is required to compile ClamAV.
is_rust_install=0
is_rust_present() {
	for cmd in cargo rustc rustup rust-gdb rust-lldb rustdoc rustfmt; do
		if ! command -v $cmd >/dev/null 2>&1; then
			is_rust_install=1
		fi
	done
}
install_rust() {
	if [[ "$is_rust_install" == 1 ]]; then
		echo "Rust toolchain not found"
		echo "Installaing Rust toolchain...."
		curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
		if [ $? -eq 0 ]; then
			echo "Rust toolchain installed"
			source $HOME/.cargo/env
		else
			echo "Failed to install rust toolchain"
			echo "Rust toolchain is required to compile ClamAV v0.105"
			return 1
		fi
	else
		echo "Rust toolchain is present"
	fi
}
is_rust_present
install_rust
